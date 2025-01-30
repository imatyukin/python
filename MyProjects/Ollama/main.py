import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # Игнорируем UserWarning

from langchain_ollama import OllamaLLM as Ollama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from sys import argv

# 1. Create the model
llm = Ollama(model='deepseek-r1:32b')
embeddings = OllamaEmbeddings(model='deepseek-r1:32b')
print(llm.invoke("Привет!"))

# 2. Load the PDF file and create a retriever to be used for providing context
print("Загружаем PDF...")
loader = PyPDFLoader(argv[1])
print("Разбиваем на страницы...")
pages = loader.load_and_split()
pages = pages[:5]  # Ограничим обработку первыми 5 страницами
print(f"Загружено страниц: {len(pages)}")
print("Создаём векторное хранилище...")
store = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
print("Создаём ретривер...")
retriever = store.as_retriever()
print("Готово к вопросам!")

# 3. Create the prompt template
template = """
Answer the question based only on the context provided.

Context: {context}

Question: {question}
"""

prompt = PromptTemplate.from_template(template)

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

# 4. Build the chain of operations
chain = (
  {
    'context': retriever | format_docs,
    'question': RunnablePassthrough(),
  }
  | prompt
  | llm
  | StrOutputParser()
)

# 5. Start asking questions and getting answers in a loop
while True:
  question = input('What do you want to learn from the document?\n')
  print()
  print(chain.invoke({'question': question}))
  print()