import warnings

warnings.filterwarnings("ignore", category=UserWarning)  # Игнорируем UserWarning

from langchain_ollama import OllamaLLM as Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS  # Заменяем DocArrayInMemorySearch на FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from sys import argv
import os

# 1. Создание модели и эмбеддингов
llm = Ollama(model='deepseek-r1:32b')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("Эмбеддинги успешно загружены!")

# 2. Загрузка PDF-файлов
if len(argv) < 2:
    raise ValueError("Укажите хотя бы один путь к PDF-файлу!")

pdf_paths = argv[1:]  # Все аргументы после имени скрипта — это пути к PDF-файлам
all_pages = []

for pdf_path in pdf_paths:
    if not os.path.exists(pdf_path):
        print(f"Файл не найден: {pdf_path}")
        continue

    print(f"Загрузка файла: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    all_pages.extend(pages)

print(f"Загружено страниц: {len(all_pages)}")

# Проверка наличия данных
if not all_pages:
    print("Нет данных для обработки. Убедитесь, что PDF-файлы загружены корректно.")
    exit(1)

# 3. Создание или загрузка векторного хранилища
vector_store_path = "vector_store"

if os.path.exists(vector_store_path):
    print("Загрузка существующего векторного хранилища...")
    store = FAISS.load_local(vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)
else:
    print("Создание нового векторного хранилища...")

    # Извлечение текстов из документов
    texts = [doc.page_content for doc in all_pages]

    # Генерация эмбеддингов
    print("Генерация эмбеддингов...")
    embeddings_vectors = embeddings.embed_documents(texts)

    # Создание FAISS индекса
    store = FAISS.from_embeddings(
        [(text, embedding) for text, embedding in zip(texts, embeddings_vectors)],
        embedding=embeddings,
        metadatas=[doc.metadata for doc in all_pages]
    )
    store.save_local(vector_store_path)

retriever = store.as_retriever()


# Функция для исправления вывода ретривера
def fix_retriever_output(docs):
    if isinstance(docs, dict):  # Если retriever вернул словарь
        return [Document(page_content=str(content)) for content in docs.values()]
    elif isinstance(docs, list):  # Если это список
        fixed_docs = []
        seen_ids = set()  # Для отслеживания уникальных документов
        for doc in docs:
            if isinstance(doc, str):  # Если элемент — строка
                fixed_docs.append(Document(page_content=doc))
            elif isinstance(doc, dict):  # Если элемент — словарь
                fixed_docs.append(Document(page_content=str(doc.get("text", ""))))
            elif hasattr(doc, "page_content"):  # Если это уже документ
                if doc.metadata.get("id") not in seen_ids:  # Проверяем уникальность
                    fixed_docs.append(doc)
                    seen_ids.add(doc.metadata.get("id"))
            else:
                raise ValueError(f"Unexpected document format: {doc}")
        return fixed_docs
    else:
        raise ValueError(f"Unexpected retriever output type: {type(docs)}")


# Функция для форматирования документов
def format_docs(docs):
    if not isinstance(docs, list):
        raise ValueError(f"Expected a list of documents, but got {type(docs)}")

    formatted_content = []
    seen_texts = set()  # Для отслеживания уникальных текстов
    for doc in docs:
        if not hasattr(doc, "page_content"):
            raise ValueError(f"Documents must have 'page_content' attribute. Got: {doc}")
        if doc.page_content not in seen_texts:  # Проверяем уникальность текста
            formatted_content.append(doc.page_content)
            seen_texts.add(doc.page_content)

    return "\n\n".join(formatted_content)


# 4. Создание шаблона запроса
template = """
You are an expert in interpreting technical documentation. Answer the question based ONLY on the context provided below.
If the context does not contain sufficient information to answer the question, reply with "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""
prompt = PromptTemplate.from_template(template)


# Функция для очистки ответа
def clean_response(response):
    # Удаляем всё до первого вхождения "Answer:"
    if "Answer:" in response:
        response = response.split("Answer:")[1].strip()

    # Удаляем теги <think> и </think>
    response = response.replace("<think>", "").replace("</think>", "")

    return response


# 5. Цикл вопросов
print("\nГотово к вопросам!")
while True:
    question = input('What do you want to learn from the document? (Type "exit" to quit)\n')
    if question.lower() == "exit":
        break

    try:
        # Этап 1: Ретривер
        relevant_docs = retriever.invoke(question)
        print("Retriever output:", relevant_docs)

        # Этап 2: Исправление вывода ретривера
        fixed_docs = fix_retriever_output(relevant_docs)
        print("Fixed retriever output:", fixed_docs)

        # Этап 3: Форматирование документов
        formatted_context = format_docs(fixed_docs)
        print("Formatted context:", formatted_context)

        # Проверка контекста
        if not formatted_context.strip():
            print("No relevant information found in the document.")
            continue

        # Этап 4: Шаблон запроса
        full_prompt = prompt.format(context=formatted_context, question=question)
        print("Full prompt:", full_prompt)

        # Этап 5: Модель LLM
        response = llm.invoke(full_prompt)
        print("LLM response:", response)

        # Постобработка ответа
        cleaned_response = clean_response(response)
        print(cleaned_response)
    except Exception as e:
        print(f"An error occurred: {e}")