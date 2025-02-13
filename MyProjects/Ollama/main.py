from langchain_ollama import OllamaLLM as Ollama
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sys import argv
import os
import hashlib

# 1. Создание модели и эмбеддингов
llm = Ollama(model='deepseek-r1:32b')  # Используем deepseek-r1:32b
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
print("Эмбеддинги успешно загружены!")

# 2. Загрузка PDF-файлов
if len(argv) < 2:
    raise ValueError("Укажите хотя бы один путь к файлу!")

file_paths = argv[1:]
all_pages = []


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


for file_path in file_paths:
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        continue

    print(f"Загрузка файла: {file_path}")
    loader = get_loader_for_file(file_path)
    pages = loader.load_and_split()
    all_pages.extend(pages)

print(f"Загружено страниц: {len(all_pages)}")

# 3. Разбиение текста на чанки
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)
texts = text_splitter.split_documents(all_pages)

# 4. Создание или загрузка векторного хранилища
vector_store_path = "vector_store"
history_file = "history.txt"


def get_file_hash(file_path):
    """Вычисляет хэш файла для проверки изменений."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


if os.path.exists(vector_store_path):
    print("Загрузка существующего векторного хранилища...")
    store = FAISS.load_local(vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)

    # Проверка и добавление новых файлов
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
        texts = text_splitter.split_documents(pages)
        metadatas = [{"source": file_path, "hash": file_hash} for _ in texts]
        store.add_documents(texts, metadatas=metadatas)
        store.save_local(vector_store_path)
else:
    print("Создание нового векторного хранилища...")

    metadatas = []
    for file_path in file_paths:
        file_hash = get_file_hash(file_path)
        loader = get_loader_for_file(file_path)
        pages = loader.load_and_split()
        texts_from_pdf = text_splitter.split_documents(pages)

        for doc in texts_from_pdf:
            metadatas.append({"source": file_path, "hash": file_hash})

    store = FAISS.from_texts(
        [doc.page_content for doc in texts],
        embedding=embeddings,
        metadatas=metadatas
    )
    store.save_local(vector_store_path)

retriever = store.as_retriever(search_kwargs={"k": 3})

# 5. Шаблон запроса
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


# 6. Функция для очистки ответа
def clean_response(response):
    if "Answer:" in response:
        response = response.split("Answer:")[1].strip()
    response = response.replace("<think>", "").replace("</think>", "")
    return response


# 7. Сохранение истории запросов
def save_to_history(question, answer):
    """Сохраняет вопрос и ответ в файл истории."""
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"Вопрос: {question}\n")
        f.write(f"Ответ: {answer}\n")
        f.write("-------------------------\n")


# 8. Цикл вопросов
print("\nГотово к вопросам!")
while True:
    question = input('What do you want to learn from the document? (Type "exit" to quit)\n')
    if question.lower() == "exit":
        break

    try:
        # Этап 1: Ретривер
        relevant_docs = retriever.invoke(question)

        # Этап 2: Форматирование контекста
        formatted_context = "\n".join([doc.page_content for doc in relevant_docs])

        # Этап 3: Шаблон запроса
        full_prompt = prompt.format(context=formatted_context, question=question)

        # Этап 4: Модель LLM
        response = llm.invoke(full_prompt)

        # Этап 5: Постобработка ответа
        cleaned_response = clean_response(response)
        print(cleaned_response)

        # Сохранение в историю
        save_to_history(question, cleaned_response)
    except Exception as e:
        print(f"An error occurred: {e}")