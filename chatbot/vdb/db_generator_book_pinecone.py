import re
import os
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import pinecone

os.environ["OPENAI_API_KEY"] = "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"
# 한별이꺼
# pinecone.init(
#     api_key="d9a396eb-d767-44c8-92eb-b4cc054f470c",
#     environment="asia-southeast1-gcp-free",
# )

# 공유계정
pinecone.init(api_key="faa64817-3e23-4fde-89d2-a505fc8f83d6", environment="asia-southeast1-gcp-free")

index_name = "questionbot"
index = pinecone.Index(index_name)
embeddings = OpenAIEmbeddings()

def token_calculator(texts, token_limit):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    # 시간 복잡도 줄이기 위해 초깃값 설정 必
    chunk_size = 180

    while True:
        token_list = []
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        splitted_text = text_splitter.split_text(texts)
        llm=OpenAI()
        for i in splitted_text:
            num_tokens = llm.get_num_tokens(i)
            token_list.append(num_tokens)

        if max(token_list) < token_limit:
            chunk_size += 1
        else:
            print(chunk_size - 1)
            return (chunk_size - 1)

def db_generator(folder_directory, start_index):
    files_list = os.listdir(folder_directory)
    embeddings = OpenAIEmbeddings()

    for i in range(0, len(files_list)):
        with open(f"{folder_directory}/{files_list[i]}", "r", encoding="utf-8") as f:
            text = f.read()
        print(f"{files_list[i]} 작업중")

        chunk_size = token_calculator(text, token_limit=512)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)

        splitted_text = text_splitter.split_text(text)
        print(len(splitted_text))
        for j in range(len(splitted_text)):
            print(j)
            metadata = {"book": files_list[i], "text": splitted_text[j]}
            data = ('book-'+str(start_index), embeddings.embed_query(splitted_text[j]), metadata)
            index.upsert(vectors=[data], namespace="book")
            start_index += 1

# 영찬
if index.describe_index_stats()['namespaces'] != {}:
  start_index = index.describe_index_stats()['namespaces']['book'] + 1
else:
  start_index = 1
db_generator(folder_directory="C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/books", start_index=start_index)
# 한별
# db_generator(folder_directory="C:/Users/hanbyul.kim/Desktop/project/chatbot/chatbot/data/books")