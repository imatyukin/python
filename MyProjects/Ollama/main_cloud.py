import sys
import os
import hashlib
import requests
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QLabel,
    QFileDialog, QWidget, QLineEdit, QMessageBox, QProgressBar, QDialog, QComboBox
)
from langchain_ollama import OllamaLLM as Ollama
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Настройки модели и API
llm = Ollama(model='deepseek-r1:32b')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

vector_store_path = "vector_store"
history_files = {
    "Локальный": "local_history.txt",
    "Qwen": "qwen_history.txt",
    "Deepseek": "deepseek_history.txt"
}

API_CONFIG = {
    "Qwen": {
        "url": "https://dashscope.aliyuncs.com/api/v1/services/qwen/generate",
        "key": "YOUR_QWEN_API_KEY"
    },
    "Deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "key": "YOUR_DEEPSEEK_API_KEY"
    }
}

def get_loader_for_file(file_path):
    if file_path.endswith(".pdf"):
        return PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        return TextLoader(file_path)
    elif file_path.endswith(".docx"):
        return Docx2txtLoader(file_path)
    raise ValueError(f"Неподдерживаемый формат файла: {file_path}")

def get_file_hash(file_path):
    """Вычисляет MD5 хэш файла."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def load_or_create_vector_store(file_paths):
    """Загружает или создаёт векторное хранилище."""
    global store
    if os.path.exists(vector_store_path):
        store = FAISS.load_local(vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)
        existing_hashes = {doc.metadata.get("hash") for doc in store.docstore._dict.values()}
    else:
        store, existing_hashes = None, set()

    new_texts, new_metadatas = [], []
    for file_path in file_paths:
        file_hash = get_file_hash(file_path)
        if file_hash in existing_hashes:
            print(f"Файл уже в хранилище: {file_path}")
            continue

        print(f"Добавление файла: {file_path}")
        loader = get_loader_for_file(file_path)
        pages = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_documents(pages)

        new_texts.extend(texts)
        new_metadatas.extend([{"source": file_path, "hash": file_hash}] * len(texts))

    if new_texts:
        if store:
            store.add_documents(new_texts, metadatas=new_metadatas)
        else:
            store = FAISS.from_texts([t.page_content for t in new_texts], embedding=embeddings, metadatas=new_metadatas)
        store.save_local(vector_store_path)

def get_answer_local(question):
    """Получает ответ с локальной модели."""
    retriever = store.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    prompt = PromptTemplate.from_template("""
        Answer the question based ONLY on the context below. If not enough info, reply "I don't know."
        Context:
        {context}
        Question: {question}
        Answer:
    """).format(context=context, question=question)

    return llm.invoke(prompt).replace("<think>", "").replace("</think>", "")

def get_answer_api(api_name, question, text):
    """Получает ответ с API Qwen или Deepseek."""
    config = API_CONFIG[api_name]
    response = requests.post(
        config["url"],
        headers={"Authorization": f"Bearer {config['key']}", "Content-Type": "application/json"},
        json={
            "model": api_name.lower(),
            "prompt": f"{text}\n\nQuestion: {question}",
            "max_tokens": 100
        }
    )
    return response.json().get("output", {}).get("text", "Ошибка при получении ответа.")

def save_to_history(mode, question, answer):
    """Сохраняет историю запросов."""
    with open(history_files[mode], "a", encoding="utf-8") as f:
        f.write(f"Вопрос: {question}\nОтвет: {answer}\n{'-'*30}\n")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document QA System")
        self.setGeometry(100, 100, 800, 600)
        self.selected_files = []

        layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(history_files.keys())
        layout.addWidget(QLabel("Выберите режим:"))
        layout.addWidget(self.mode_combo)

        self.file_button = QPushButton("Выбрать файлы")
        self.file_button.clicked.connect(self.select_files)
        layout.addWidget(self.file_button)

        self.selected_files_label = QLabel("Выбранные файлы: Нет")
        layout.addWidget(self.selected_files_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.question_input = QLineEdit()
        layout.addWidget(QLabel("Введите ваш вопрос:"))
        layout.addWidget(self.question_input)

        self.ask_button = QPushButton("Получить ответ")
        self.ask_button.clicked.connect(self.get_answer)
        layout.addWidget(self.ask_button)

        self.answer_output = QTextEdit()
        self.answer_output.setReadOnly(True)
        layout.addWidget(QLabel("Ответ:"))
        layout.addWidget(self.answer_output)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "Документы (*.pdf *.txt *.docx)")
        if files:
            self.selected_files = files
            self.selected_files_label.setText(f"Выбранные файлы: {', '.join(os.path.basename(f) for f in files)}")
            self.progress_bar.setValue(0)

            threading.Thread(target=self.load_files, daemon=True).start()

    def load_files(self):
        load_or_create_vector_store(self.selected_files)
        self.progress_bar.setValue(100)

    def get_answer(self):
        question = self.question_input.text().strip()
        if not question:
            QMessageBox.warning(self, "Ошибка", "Введите вопрос!")
            return

        mode = self.mode_combo.currentText()
        self.ask_button.setText("Поиск ответа...")
        self.answer_output.setText("")

        threading.Thread(target=self.process_answer, args=(mode, question), daemon=True).start()

    def process_answer(self, mode, question):
        answer = get_answer_local(question) if mode == "Локальный" else get_answer_api(mode, question, "")
        self.answer_output.setText(answer)
        save_to_history(mode, question, answer)
        self.ask_button.setText("Получить ответ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())