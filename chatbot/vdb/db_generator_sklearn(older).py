# -*- coding: utf-8 -*-

import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain.vectorstores import SKLearnVectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# 디렉토리에 있는 txt파일들 가져와 textsplit, embedding, vdb에 넣어줌.
def db_generator(folder_directory):
    # 디렉토리 안에 있는 file들 list로 받아옴
    files_list = os.listdir(folder_directory)

    # 각 txt 파일들 손질할 splitter 가져오기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    # embedding tool 가져오기
    embedding = OpenAIEmbeddings()
    # 저장 위치 지정
    persist_path = 'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/vdb/books_embedding'+".parquet"

    # 각 txt 파일마다 불러오고, 자르고, 임베딩 해 vdb에 저장(로컬 parquet 확장자)
    for i in range(0, len(files_list)):
        print(f'{i}번 문서 작업 중')
        loader = TextLoader(f'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/novels/{files_list[i]}', encoding='utf-8')
        documents = loader.load()
        texts = text_splitter.split_documents(documents)
        vector_store = SKLearnVectorStore.from_documents(
            documents=texts,
            embedding=embedding,
            persist_path=persist_path,
            serializer="parquet",
        )
        vector_store.persist()
        vector_store = None
        print(f'{i}번 문서 완료')

# db_generator('C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/novels')


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# embedding tool 가져오기
embedding = OpenAIEmbeddings()
# 저장 위치 지정
persist_path = 'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/vdb/books_embedding'+".parquet"

f = open('C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/novels/데못죽 등장인물, 단체.txt', 'r', encoding='utf-8')
texts = f.read()
splitted_texts = texts.split('\n\n')
texts = [i.replace('\n', '') for i in splitted_texts]
for i in texts:
    spliitted_texts = text_splitter.split_text(i)
    vector_store = SKLearnVectorStore.from_texts(
        texts=splitted_texts,
        embedding=embedding,
        persist_path=persist_path,
        serializer="parquet",
    )
    vector_store.persist()
    vector_store = None