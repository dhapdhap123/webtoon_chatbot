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
    embeddings = OpenAIEmbeddings()

    for i in range(0, len(files_list)):
        with open(f"{folder_directory}/{files_list[i]}", "r", encoding="utf-8") as f:
            text = f.read()
        print(f"{files_list[i]} 작업중")
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
                metadata = {"name": names[j], "text": k}
                data = (str(start_index), embeddings.embed_query(k), metadata)
                index.upsert(vectors=[data], namespace=filename_extension)
                start_index += 1

# 영찬
# if index.describe_index_stats()['namespaces'] != {}:
#   start_index = index.describe_index_stats()['namespaces']['book'] + 1
# else:
start_index = 1
db_generator(folder_directory="C:/Users/dhapd/OneDrive/바탕 화면/chatbot_/chatbot/data/chungmyung", start_index=start_index)