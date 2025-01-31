Документация к скрипту
Описание программы
Программа предназначена для анализа PDF-документов с помощью векторного поиска и языковой модели (LLM).
Она позволяет задавать вопросы по содержимому документов и получать ответы на основе релевантных фрагментов текста.

Основные возможности
Загрузка PDF-файлов:
Программа загружает PDF-документы и разбивает их на страницы.
Создание векторного хранилища:
Тексты из документов преобразуются в эмбеддинги (векторные представления) с помощью модели
sentence-transformers/all-MiniLM-L12-v2.
Эмбеддинги сохраняются в локальное хранилище (FAISS).
Поиск релевантных фрагментов:
На основе вопроса пользователя программа использует векторный поиск для извлечения релевантных фрагментов текста.
Генерация ответа:
Релевантные фрагменты передаются языковой модели (например, deepseek-r1:32b), которая генерирует ответ на вопрос.

Установка и запуск
Требования
Python 3.8 или выше.
Установленные библиотеки:
pip install langchain langchain_community langchain_core sentence-transformers faiss-cpu
Запуск программы
Сохраните программу в файл, например, main.py.
Запустите программу, указав путь к PDF-файлам:
python main.py file1.pdf file2.pdf
Введите вопрос в консоль. Например:
What do you want to learn from the document? (Type "exit" to quit)
How to configure BGP on Nokia routers?

Как работает программа
1. Инициализация модели и эмбеддингов
llm = Ollama(model='deepseek-r1:32b')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
Модель LLM: Используется модель deepseek-r1:32b для генерации ответов.
Эмбеддинги: Модель sentence-transformers/all-MiniLM-L12-v2 преобразует тексты в векторы для векторного поиска.

2. Загрузка PDF-файлов
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()
all_pages.extend(pages)
PyPDFLoader : Разбивает PDF-документ на страницы.
Каждая страница преобразуется в объект типа Document, содержащий текст (page_content) и метаданные (metadata).

3. Разбиение текста на чанки
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)
texts = text_splitter.split_documents(all_pages)
RecursiveCharacterTextSplitter : Разбивает текст на небольшие фрагменты (чанки) для более точного поиска.
Параметры:
chunk_size: Размер каждого чанка (500 символов).
chunk_overlap: Перекрытие между чанками (100 символов).
separators: Символы, по которым происходит разбиение текста.

4. Создание векторного хранилища
store = FAISS.from_documents(texts, embedding=embeddings)
store.save_local(vector_store_path)
FAISS: Библиотека для быстрого векторного поиска.
Тексты и их эмбеддинги сохраняются в локальном хранилище (vector_store).
Если хранилище уже существует, программа загружает его:
store = FAISS.load_local(vector_store_path, embeddings=embeddings, allow_dangerous_deserialization=True)

5. Поиск релевантных фрагментов
retriever = store.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.invoke(question)
Ретривер: Находит до 3 самых релевантных фрагментов текста на основе вопроса пользователя.
Результат — список объектов типа Document.

6. Генерация ответа
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
response = llm.invoke(full_prompt)
Шаблон запроса : Формирует полный запрос для модели LLM.
Модель LLM : Генерирует ответ на основе предоставленного контекста.

7. Обработка изменений в файлах
def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
Хэширование: Вычисляет MD5-хэш файла для проверки изменений.
Если файл был изменён, его эмбеддинги обновляются в хранилище.

8. Постобработка ответа
def clean_response(response):
    if "Answer:" in response:
        response = response.split("Answer:")[1].strip()
    response = response.replace("<think>", "").replace("</think>", "")
    return response
Удаляет лишние теги (<think>, </think>) и форматирует ответ.

Инструкции по использованию
1. Первый запуск
Если вы запускаете программу впервые:

Укажите пути к PDF-файлам:
python main.py file1.pdf file2.pdf
Программа создаст векторное хранилище и добавит файлы в него.

2. Повторный запуск
Если хранилище уже существует:

Укажите новые файлы, если нужно добавить их:
python main.py new_file.pdf
Программа проверит, какие файлы уже добавлены, и добавит только новые или изменённые.

3. Задавайте вопросы
Введите вопрос в консоль. Например:
What do you want to learn from the document? (Type "exit" to quit)
How to configure OSPF on Huawei routers?

Рекомендации
Оптимизация контекста:
Если контекст слишком длинный, можно увеличить параметр k для ретривера:
retriever = store.as_retriever(search_kwargs={"k": 5})  # Вернуть 5 документов
Добавление новых файлов:
Просто укажите их пути при запуске программы:
python main.py file1.pdf file2.pdf
Обновление хранилища:
Если файл был изменён, программа автоматически обновит его эмбеддинги благодаря хэшированию.