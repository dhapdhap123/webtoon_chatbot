import os
os.environ["OPENAI_API_KEY"] = "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"

from llama_index import VectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader('C:/Users/dhapd/OneDrive/바탕 화면/chatbot_/chatbot/data/chungmyung').load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever()
# query_engine = index.as_query_engine()
# chat_engine = index.as_chat_engine()
print(retriever.retrieve("낙화검이 뭐야?"))