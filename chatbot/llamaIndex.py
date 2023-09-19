from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader('C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/novels').load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("낙화검이 뭐야")
print(response)