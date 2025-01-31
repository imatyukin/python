import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QFileDialog, QWidget, QLineEdit, QMessageBox, QProgressBar, QDialog, QComboBox
)
from PyQt5.QtCore import QTimer
import requests
from langchain_ollama import OllamaLLM as Ollama
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import hashlib

# 1. Локальная модель
llm = Ollama(model='deepseek-r1:32b')  # Локальная модель
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

# 2. Путь к векторному хранилищу и истории
vector_store_path = "vector_store"
local_history_file = "local_history.txt"
qwen_history_file = "qwen_history.txt"

# 3. Конфигурация API Qwen
QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/qwen/generate"
QWEN_API_KEY = "YOUR_QWEN_API_KEY"  # Замените на ваш API ключ


def get_loader_for_file(file_path):
    """Выбирает загрузчик в зависимости от формата файла."""
    if file_path.endswith(".pdf"):
        return PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        return TextLoader(file_path)
    elif file_path.endswith(".docx"):
        return Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_path}")


def get_file_hash(file_path):
    """Вычисляет хэш файла для проверки изменений."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def load_or_create_vector_store(file_paths):
    """Загружает или создаёт векторное хранилище."""
    global store
    if os.path.exists(vector_store_path):
        print("Загрузка существующего векторного хранилища...")
        store = FAISS.load_local(vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)

        for file_path in file_paths:
            file_hash = get_file_hash(file_path)

            existing_hashes = set()
            for doc_id, doc in store.docstore._dict.items():
                existing_hashes.add(doc.metadata.get("hash"))

            if file_hash in existing_hashes:
                print(f"Файл уже добавлен в хранилище: {file_path}")
                continue

            print(f"Добавление нового файла в хранилище: {file_path}")
            loader = get_loader_for_file(file_path)
            pages = loader.load_and_split()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100,
                separators=["\n\n", "\n", ".", " ", ""]
            )
            texts = text_splitter.split_documents(pages)
            metadatas = [{"source": file_path, "hash": file_hash} for _ in texts]
            store.add_documents(texts, metadatas=metadatas)
            store.save_local(vector_store_path)
    else:
        print("Создание нового векторного хранилища...")

        all_pages = []
        for file_path in file_paths:
            loader = get_loader_for_file(file_path)
            pages = loader.load_and_split()
            all_pages.extend(pages)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        texts = text_splitter.split_documents(all_pages)

        metadatas = []
        for file_path in file_paths:
            file_hash = get_file_hash(file_path)
            for _ in range(len(texts)):
                metadatas.append({"source": file_path, "hash": file_hash})

        store = FAISS.from_texts(
            [doc.page_content for doc in texts],
            embedding=embeddings,
            metadatas=metadatas
        )
        store.save_local(vector_store_path)


def answer_question_local(question):
    """Ответ на вопрос с использованием локальной модели."""
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


def answer_question_qwen(question, text):
    """Ответ на вопрос с использованием API Qwen."""
    url = QWEN_API_URL
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen",
        "prompt": f"{text}\n\nQuestion: {question}",
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("output", {}).get("text", "Ошибка при получении ответа.")


def save_to_history(history_file, question, answer):
    """Сохраняет вопрос и ответ в файл истории."""
    try:
        with open(history_file, "a", encoding="utf-8") as f:
            f.write(f"Вопрос: {question}\n")
            f.write(f"Ответ: {answer}\n")
            f.write("-------------------------\n")
    except Exception as e:
        print(f"Ошибка при сохранении истории: {e}")


class HistoryDialog(QDialog):
    def __init__(self, history_text):
        super().__init__()
        self.setWindowTitle("История запросов")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(history_text)  # Устанавливаем текст истории
        self.text_edit.setReadOnly(True)  # Только для чтения
        layout.addWidget(self.text_edit)

        self.setLayout(layout)


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

        # Выбор режима работы
        self.mode_label = QLabel("Выберите режим работы:")
        self.layout.addWidget(self.mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Локальный", "Qwen"])
        self.layout.addWidget(self.mode_combo)

        # Выбор файлов
        self.file_label = QLabel("Выберите файлы:")
        self.layout.addWidget(self.file_label)

        self.file_button = QPushButton("Выбрать файлы")
        self.file_button.clicked.connect(self.select_files)
        self.layout.addWidget(self.file_button)

        # Отображение выбранных файлов
        self.selected_files_label = QLabel("Выбранные файлы: Нет")
        self.layout.addWidget(self.selected_files_label)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # Поле для вопроса
        self.question_label = QLabel("Введите ваш вопрос:")
        self.layout.addWidget(self.question_label)

        self.question_input = QLineEdit()
        self.layout.addWidget(self.question_input)

        # Кнопка "Получить ответ"
        self.ask_button = QPushButton("Получить ответ")
        self.ask_button.clicked.connect(self.get_answer)
        self.layout.addWidget(self.ask_button)

        # Статус выполнения
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # Поле для ответа
        self.answer_label = QLabel("Ответ:")
        self.layout.addWidget(self.answer_label)

        self.answer_output = QTextEdit()
        self.answer_output.setReadOnly(True)
        self.layout.addWidget(self.answer_output)

        # Кнопка "Показать историю"
        self.history_button = QPushButton("Показать историю")
        self.history_button.clicked.connect(self.show_history)
        self.layout.addWidget(self.history_button)

        # Кнопка "Очистить историю"
        self.clear_history_button = QPushButton("Очистить историю")
        self.clear_history_button.clicked.connect(self.clear_history)
        self.layout.addWidget(self.clear_history_button)

        # Список выбранных файлов
        self.selected_files = []

    def select_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Выберите файлы", "", "Поддерживаемые файлы (*.pdf *.txt *.docx);;Все файлы (*)", options=options
        )
        if files:
            self.selected_files = files
            self.selected_files_label.setText(f"Выбранные файлы: {', '.join([os.path.basename(f) for f in files])}")
            QMessageBox.information(self, "Файлы выбраны", f"Выбрано файлов: {len(files)}")

            # Загрузка файлов с прогрессом
            self.progress_bar.setValue(0)
            total_files = len(files)
            for i, file in enumerate(files):
                self.progress_bar.setValue(int((i + 1) / total_files * 100))
                QApplication.processEvents()  # Обновление GUI
                try:
                    load_or_create_vector_store([file])
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл {file}: {e}")
            self.progress_bar.setValue(100)

    def get_answer(self):
        mode = self.mode_combo.currentText()
        if not self.selected_files:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите файлы!")
            return

        question = self.question_input.text().strip()
        if not question:
            QMessageBox.warning(self, "Ошибка", "Введите вопрос!")
            return

        try:
            # Индикация работы
            self.ask_button.setText("Ищем ответ...")
            self.status_label.setText("Обработка запроса...")
            self.progress_bar.setRange(0, 0)  # Бесконечная анимация
            QApplication.processEvents()  # Обновление GUI

            # Получение текста из файлов
            text = ""
            for file in self.selected_files:
                loader = get_loader_for_file(file)
                pages = loader.load_and_split()
                text += "\n".join([page.page_content for page in pages])

            # Получение ответа
            if mode == "Локальный":
                answer = answer_question_local(question)
                history_file = local_history_file
            else:
                answer = answer_question_qwen(question, text)
                history_file = qwen_history_file

            self.answer_output.setText(answer)

            # Сохранение в историю
            save_to_history(history_file, question, answer)

            # Восстановление интерфейса
            self.ask_button.setText("Получить ответ")
            self.status_label.setText("")
            self.progress_bar.setRange(0, 100)  # Возвращаем нормальный прогресс
            self.progress_bar.setValue(100)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
            self.ask_button.setText("Получить ответ")
            self.status_label.setText("")
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)

    def show_history(self):
        # Определяем, какой файл истории использовать
        mode = self.mode_combo.currentText()
        history_file = local_history_file if mode == "Локальный" else qwen_history_file

        # Проверяем, существует ли файл
        if not os.path.exists(history_file):
            QMessageBox.information(self, "История", f"История запросов для режима '{mode}' пуста.")
            return

        try:
            # Читаем содержимое файла
            with open(history_file, "r", encoding="utf-8") as f:
                history_text = f.read()

            # Если файл пуст, показываем сообщение
            if not history_text.strip():
                QMessageBox.information(self, "История", f"История запросов для режима '{mode}' пуста.")
                return

            # Открываем диалоговое окно с историей
            dialog = HistoryDialog(history_text)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать историю: {e}")

    def clear_history(self):
        # Определяем, какой файл истории использовать
        mode = self.mode_combo.currentText()
        history_file = local_history_file if mode == "Локальный" else qwen_history_file

        # Проверяем, существует ли файл
        if os.path.exists(history_file):
            try:
                os.remove(history_file)
                QMessageBox.information(self, "История", f"История запросов для режима '{mode}' очищена.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось очистить историю: {e}")
        else:
            QMessageBox.information(self, "История", f"История запросов для режима '{mode}' уже пуста.")


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())