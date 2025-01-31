import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QFileDialog, QWidget, QLineEdit, QMessageBox
)
from langchain_ollama import OllamaLLM as Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import hashlib

# 1. Создание модели и эмбеддингов
llm = Ollama(model='deepseek-r1:32b')  # Используем deepseek-r1:32b
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

# 2. Векторное хранилище
vector_store_path = "vector_store"
store = None


def get_file_hash(file_path):
    """Вычисляет хэш файла для проверки изменений."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def load_or_create_vector_store(pdf_paths):
    global store
    if os.path.exists(vector_store_path):
        print("Загрузка существующего векторного хранилища...")
        store = FAISS.load_local(vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)

        # Проверка и добавление новых файлов
        for pdf_path in pdf_paths:
            file_hash = get_file_hash(pdf_path)

            existing_hashes = set()
            for doc_id, doc in store.docstore._dict.items():
                existing_hashes.add(doc.metadata.get("hash"))

            if file_hash in existing_hashes:
                print(f"Файл уже добавлен в хранилище: {pdf_path}")
                continue

            print(f"Добавление нового файла в хранилище: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            pages = loader.load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100,
                separators=["\n\n", "\n", ".", " ", ""]
            )
            texts = text_splitter.split_documents(pages)
            metadatas = [{"source": pdf_path, "hash": file_hash} for _ in texts]
            store.add_documents(texts, metadatas=metadatas)
            store.save_local(vector_store_path)
    else:
        print("Создание нового векторного хранилища...")
        all_pages = []
        for pdf_path in pdf_paths:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load_and_split()
            all_pages.extend(pages)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        texts = text_splitter.split_documents(all_pages)

        metadatas = []
        for pdf_path in pdf_paths:
            file_hash = get_file_hash(pdf_path)
            for _ in range(len(texts)):
                metadatas.append({"source": pdf_path, "hash": file_hash})

        store = FAISS.from_texts(
            [doc.page_content for doc in texts],
            embedding=embeddings,
            metadatas=metadatas
        )
        store.save_local(vector_store_path)


def answer_question(question):
    retriever = store.as_retriever(search_kwargs={"k": 3})

    template = """
    Answer the question based ONLY on the context provided below. 
    If the context does not contain sufficient information to answer the question, reply with "I don't know."

    Context:
    {context}

    Question:
    {question}

    Instructions:
    - Focus only on the most relevant parts of the context.
    - Provide a concise and clear answer.
    - If the question requires multiple steps, explain them step by step.
    - Ignore any irrelevant or repetitive information in the context.

    Answer:
    """
    prompt = PromptTemplate.from_template(template)
    relevant_docs = retriever.invoke(question)
    formatted_context = "\n".join([doc.page_content for doc in relevant_docs])
    full_prompt = prompt.format(context=formatted_context, question=question)
    response = llm.invoke(full_prompt)
    return response.replace("<think>", "").replace("</think>", "")


# 4. Графический интерфейс
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document QA System")
        self.setGeometry(100, 100, 800, 600)

        # Главный виджет и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Выбор файлов
        self.file_label = QLabel("Выберите PDF-файлы:")
        self.layout.addWidget(self.file_label)

        self.file_button = QPushButton("Выбрать файлы")
        self.file_button.clicked.connect(self.select_files)
        self.layout.addWidget(self.file_button)

        # Поле для вопроса
        self.question_label = QLabel("Введите ваш вопрос:")
        self.layout.addWidget(self.question_label)

        self.question_input = QLineEdit()
        self.layout.addWidget(self.question_input)

        self.ask_button = QPushButton("Получить ответ")
        self.ask_button.clicked.connect(self.get_answer)
        self.layout.addWidget(self.ask_button)

        # Поле для ответа
        self.answer_label = QLabel("Ответ:")
        self.layout.addWidget(self.answer_label)

        self.answer_output = QTextEdit()
        self.answer_output.setReadOnly(True)
        self.layout.addWidget(self.answer_output)

        # Список выбранных файлов
        self.selected_files = []

    def select_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Выберите PDF-файлы", "", "PDF Files (*.pdf)", options=options
        )
        if files:
            self.selected_files = files
            QMessageBox.information(self, "Файлы выбраны", f"Выбрано файлов: {len(files)}")
            load_or_create_vector_store(self.selected_files)

    def get_answer(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите PDF-файлы!")
            return

        question = self.question_input.text().strip()
        if not question:
            QMessageBox.warning(self, "Ошибка", "Введите вопрос!")
            return

        try:
            answer = answer_question(question)
            self.answer_output.setText(answer)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())