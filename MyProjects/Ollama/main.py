import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # Игнорируем UserWarning

from langchain_ollama import OllamaLLM as Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from sys import argv
import time

# 1. Создание модели и эмбеддингов
llm = Ollama(model='deepseek-r1:32b')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("Эмбеддинги успешно загружены!")

# 2. Загрузка PDF-файла
if len(argv) < 2:
    raise ValueError("Путь к PDF-файлу не указан!")

loader = PyPDFLoader(argv[1])
pages = loader.load_and_split()
print(f"Загружено страниц: {len(pages)}")

# 3. Создание векторного хранилища
store = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
retriever = store.as_retriever()

# Функция для исправления вывода ретривера
def fix_retriever_output(docs):
    if isinstance(docs, dict):  # Если retriever вернул словарь
        return [Document(page_content=content) for content in docs.values()]
    elif isinstance(docs, list):  # Если это список
        fixed_docs = []
        for doc in docs:
            if isinstance(doc, str):  # Если элемент — строка
                fixed_docs.append(Document(page_content=doc))
            elif isinstance(doc, dict):  # Если элемент — словарь
                fixed_docs.append(Document(page_content=doc.get("text", "")))
            elif hasattr(doc, "page_content"):  # Если это уже документ
                fixed_docs.append(doc)
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
    for doc in docs:
        if not hasattr(doc, "page_content"):
            raise ValueError(f"Documents must have 'page_content' attribute. Got: {doc}")
        formatted_content.append(doc.page_content)

    return "\n\n".join(formatted_content)


# 4. Создание шаблона запроса
template = """
Answer the question based only on the context provided.
Context: {context}
Question: {question}
"""
prompt = PromptTemplate.from_template(template)

# 5. Создание цепочки обработки
chain = (
    {
        'context': retriever | RunnablePassthrough() | fix_retriever_output | format_docs,
        'question': RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 6. Цикл вопросов
print("\nГотово к вопросам!")
while True:
    question = input('What do you want to learn from the document? (Type "exit" to quit)\n')
    if question.lower() == "exit":
        break

    try:
        # Используем метод invoke вместо get_relevant_documents
        relevant_docs = retriever.invoke(question)
        fixed_docs = fix_retriever_output(relevant_docs)
        formatted_context = format_docs(fixed_docs)
        full_prompt = prompt.format(context=formatted_context, question=question)
        response = llm.invoke(full_prompt)
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")