Документация программы
Описание программы
Программа предназначена для анализа PDF-документов с помощью векторного поиска и языковой модели (LLM).
Она позволяет задавать вопросы по содержимому документа и получать ответы на основе релевантных фрагментов текста.

Основные функции
1. Загрузка PDF-файлов:
Программа загружает PDF-документы и разбивает их на страницы.
2. Создание векторного хранилища:
Тексты из документов преобразуются в эмбеддинги (векторные представления) с помощью модели
sentence-transformers/all-MiniLM-L6-v2.
Эмбеддинги сохраняются в локальное хранилище (FAISS).
3. Поиск релевантных фрагментов:
На основе вопроса пользователя программа использует векторный поиск для извлечения релевантных фрагментов текста.
4. Генерация ответа:
Релевантные фрагменты передаются языковой модели (например, deepseek-r1:32b), которая генерирует ответ на вопрос.

Установка и запуск
Требования
1. Python 3.8 или выше.
2. Установленные библиотеки:

pip install langchain langchain_community langchain_core sentence-transformers faiss-cpu

Запуск программы
Сохраните программу в файл, например, main.py.
Запустите программу, указав путь к PDF-файлу:
python main.py Quality_of_Service_Guide_24.7.R1.pdf
Введите вопрос в консоль. Например:
What do you want to learn from the document? (Type "exit" to quit)
what is queue-group?

Как работает программа
1. Инициализация модели и эмбеддингов

llm = Ollama(model='deepseek-r1:32b')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

Модель LLM : Используется модель deepseek-r1:32b для генерации ответов.
Эмбеддинги : Модель sentence-transformers/all-MiniLM-L6-v2 преобразует тексты в векторы для векторного поиска.

2. Загрузка PDF-файлов

loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()
all_pages.extend(pages)

PyPDFLoader : Разбивает PDF-документ на страницы.
Каждая страница преобразуется в объект типа Document, содержащий текст (page_content) и метаданные (metadata).

3. Создание векторного хранилища

store = FAISS.from_embeddings(
    [(text, embedding) for text, embedding in zip(texts, embeddings_vectors)],
    embedding=embeddings,
    metadatas=[doc.metadata for doc in all_pages]
)
store.save_local(vector_store_path)

FAISS : Библиотека для быстрого векторного поиска.
Тексты и их эмбеддинги сохраняются в локальном хранилище (vector_store).

4. Поиск релевантных фрагментов

retriever = store.as_retriever()
relevant_docs = retriever.invoke(question)

Ретривер: Находит документы, наиболее релевантные вопросу пользователя.
Результат — список объектов типа Document.

5. Обработка данных
a) Исправление вывода ретривера

def fix_retriever_output(docs):
    ...

Преобразует данные, возвращаемые ретривером, в список объектов типа Document.
Удаляет дубликаты документов.

b) Форматирование контекста

def format_docs(docs):
    ...

Объединяет тексты документов в одну строку.
Удаляет дубликаты текстов.

6. Генерация ответа

template = """
You are an expert in interpreting technical documentation. Answer the question based ONLY on the context provided below.
If the context does not contain sufficient information to answer the question, reply with "I don't know."

Context:
{context}

Question:
{question}
"""
prompt = PromptTemplate.from_template(template)
response = llm.invoke(full_prompt)

Шаблон запроса: Формирует полный запрос для модели LLM.
Модель LLM: Генерирует ответ на основе предоставленного контекста.

Отладочный вывод
Программа выводит отладочную информацию для каждого этапа:

Retriever output:
Документы, найденные ретривером.
Fixed retriever output:
Исправленные документы после обработки функцией fix_retriever_output.
Formatted context:
Контекст, передаваемый модели LLM.
Full prompt:
Полный запрос, отправляемый модели.
LLM response:
Ответ, сгенерированный моделью.

Обработка ошибок
Программа обрабатывает следующие случаи:

Если файл не найден:

Файл не найден: <file_path>

Если контекст пуст:

No relevant information found in the document.

Если возникает ошибка:

An error occurred: <error_message>

Добавление новых PDF-файлов:

Просто укажите их пути при запуске программы:

python main.py file1.pdf file2.pdf