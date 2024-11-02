import re
import os
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import pinecone

os.environ["OPENAI_API_KEY"] = "my-openai-api-key"

# 공유계정
pinecone.init(api_key="my-pinecone-api-key", environment="asia-southeast1-gcp-free")

index_name = "chungmyung"
index = pinecone.Index(index_name)
embeddings = OpenAIEmbeddings()

def token_calculator(texts, token_limit):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    # 시간 복잡도 줄이기 위해 초깃값 설정 必
    chunk_size = 180

    while True:
        token_list = []
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
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

    for i in range(0, len(files_list)):
        with open(f"{folder_directory}/{files_list[i]}", "r", encoding="utf-8") as f:
            text = f.read()
        print(f"{files_list[i]} 작업중")
        # words
        namespace = re.findall(r".+/(.+)", folder_directory)[0]
        # animal, place, skill...
        filename_extension = files_list[i].split('.')[0]
    
        splitted_text = text.split('- ')[1:]
        
        pattern = r"- (.*?) : (.*?)\n\n"
        matches = re.findall(pattern, text, re.DOTALL)
        names = [match[0].strip() for match in matches]
        # contents = [match[1].strip() for match in matches]

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        for j in range(len(splitted_text)):
            splitted_text_by_chunk = text_splitter.split_text(splitted_text[j])
        
            for k in splitted_text_by_chunk:
                metadata = {"category": filename_extension, "name": names[j], "text": k}
                data = (str(start_index), embeddings.embed_query(k), metadata)
                index.upsert(vectors=[data], namespace=namespace)
                start_index += 1
    return start_index

def keywords_db_generator(file_directory, start_index):
    with open(file_directory, "r", encoding="utf-8") as f:
        text = f.read()
    splitted_text = text.split(',')
    stripped_text = [i.strip() for i in splitted_text]

    namespace = re.findall(r".+/(.+).txt", file_directory)[0]

    for i in stripped_text:
        metadata = {"name": i}
        data = (str(start_index), embeddings.embed_query(i), metadata)
        index.upsert(vectors=[data], namespace=namespace)
        start_index += 1
    return start_index

start_index = index.describe_index_stats()['total_vector_count'] + 1

# conversation, words가능
# start_index = keywords_db_generator(file_directory='C:/Users/dhapd/OneDrive/바탕 화면/chatbot_/chatbot/data/chungmyung/keywords/keywords.txt', start_index=start_index)
# start_index = db_generator(folder_directory="C:/Users/dhapd/OneDrive/바탕 화면/chatbot_/chatbot/data/chungmyung/words", start_index=start_index)
# db_generator(folder_directory="C:/Users/dhapd/OneDrive/바탕 화면/chatbot_/chatbot/data/chungmyung/conversation", start_index=start_index)
vdb_res = index.query(vector=embeddings.embed_query("교룡 귀엽지 않니 ㅎㅎ"), top_k=3, include_metadata=True, namespace='keywords')
print(vdb_res)