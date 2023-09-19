import re
import os
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "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"
import pinecone
pinecone.init(api_key="faa64817-3e23-4fde-89d2-a505fc8f83d6", environment="asia-southeast1-gcp-free")

def split_text_by_pattern(text, pattern):
    splitted_text = [i for i in re.split(pattern, text)[1:] if i is not None]
    
    title_list = []
    content_list = []
    for i in range(len(splitted_text)):
        if i % 2 == 0:
            title_list.append(splitted_text[i])
        else:
            if splitted_text[i] == '':
                content_list.append(re.findall(r'삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>', splitted_text[i-1])[0])
            else:
                content_list.append(splitted_text[i])

    return title_list, content_list

# part:편, chapter:장, section:절, article:조
def whole_text_list_generator(file_directory, file_name):
    whole_text_list = []
    with open(f'{file_directory}', 'r', encoding='utf-8') as f:
        text = f.read()
    match text[:3]:
        case '제1편':
            part_list, part_content_list = split_text_by_pattern(text, r"(제\d+편[^제]+)")
            
            for i in range(len(part_content_list)):
                # 몇 편인지 정보 저장
                part = re.findall(r'(y6제\d+편)', part_list[i])[0][0]

                chapter_list, chapter_content_list = split_text_by_pattern(part_content_list[i], r"(제\d+장[^제]+)|(제\d+장삭제 <\d{4}\.\d{1,2}\.\d{1,2}>)")

                for j in range(len(chapter_content_list)):
                    # 몇 장인지 정보 저장
                    chapter = re.findall(r'(제(\d+장)(의\d+)?)', chapter_list[j])[0][0]

                    # 장에 절이 있는지 검사
                    if re.findall(r'제\d+절', chapter_content_list[j]):
                        section_list, section_content_list = split_text_by_pattern(chapter_content_list[j], r"(제\d+절(?:의\d+)?[^제]+)|(제\d+절(?:의\d+)?삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

                        for k in range(len(section_list)):
                            section = re.findall(r'(제(\d+절)(의\d+)?)', section_list[k])[0][0]
                            
                            article_list, article_content_list = split_text_by_pattern(section_content_list[k], r"(제\d+조(?!\(변경\w{2} 사항만 해당한다\))(?:의\d+)?\(.*?\)|제\d+조(?:의\d+)?삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

                            for l in range(len(article_content_list)):
                                article = re.findall(r'(제(\d+조)(의\d+)?)', article_list[l])[0][0]
                                whole_text_list.append({
                                    'values': article_content_list[l],
                                    # 'values': embeddings.embed_query(j),
                                    'metadata': {'title': file_name[:-4], 'article': article, 'text': article_content_list[l]}
                                }) 
                    # 절이 없다면 바로 조로 나눔
                    else:
                        article_list, article_content_list = split_text_by_pattern(chapter_content_list[j], r"(제\d+조(?!\(변경\w{2} 사항만 해당한다\))(?:의\d+)?\(.*?\)|제\d+조(?:의\d+)?삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

                        for k in range(len(article_content_list)):
                            article = re.findall(r'(제(\d+조)(의\d+)?)', article_list[k])[0][0]
                            whole_text_list.append({
                                'values': article_content_list[k],
                                # 'values': embeddings.embed_query(j),
                                'metadata': {'title': file_name[:-4], 'article': article, 'text': article_content_list[k]}
                            })
        case '제1장':
            chapter_list, chapter_content_list = split_text_by_pattern(text, r"(제\d+장[^제]+)|(제\d+장삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

            for j in range(len(chapter_content_list)):
                # 몇 장인지 정보 저장
                chapter = re.findall(r'(제(\d+장)(의\d+)?)', chapter_list[j])[0][0]

                # 장에 절이 있는지 검사
                if re.findall(r'제\d+절', chapter_content_list[j]):
                    section_list, section_content_list = split_text_by_pattern(chapter_content_list[j], r"(제\d+절(?:의\d+)?[^제]+)|(제\d+절(?:의\d+)?삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

                    for k in range(len(section_list)):
                        section = re.findall(r'(제(\d+절)(의\d+)?)', section_list[k])[0][0]
                        
                        article_list, article_content_list = split_text_by_pattern(section_content_list[k], r"(제\d+조(?!\(변경\w{2} 사항만 해당한다\))(?:의\d+)?\(.*?\)|제\d+조(?:의\d+)?삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

                        for l in range(len(article_content_list)):
                            article = re.findall(r'(제(\d+조)(의\d+)?)', article_list[l])[0][0]
                            whole_text_list.append({
                                'values': article_content_list[l],
                                # 'values': embeddings.embed_query(j),
                                'metadata': {'title': file_name[:-4], 'article': article, 'text': article_content_list[l]}
                            })
                # 절이 없다면 바로 조로 나눔
                else:
                    article_list, article_content_list = split_text_by_pattern(chapter_content_list[j], r"(제\d+조(?!\(변경\w{2} 사항만 해당한다\))(?:의\d+)?\(.*?\)|제\d+조(?:의\d+)?삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

                    for k in range(len(article_content_list)):
                        article = re.findall(r'(제(\d+조)(의\d+)?)', article_list[k])[0][0]
                        whole_text_list.append({
                            'values': article_content_list[k],
                            # 'values': embeddings.embed_query(j),
                            'metadata': {'title': file_name[:-4], 'article': article, 'text': article_content_list[k]}
                        })
        case '제1조':
            article_list, article_content_list = split_text_by_pattern(text, r"(제\d+조(?!\(변경\w{2} 사항만 해당한다\))(?:의\d+)?\(.*?\)|제\d+조(?:의\d+)?삭제\s<\d{4}\.\d{1,2}\.\d{1,2}>)")

            for k in range(len(article_content_list)):
                article = re.findall(r'(제(\d+조)(의\d+)?)', article_list[k])[0][0]
                whole_text_list.append({
                    'values': article_content_list[k],
                    # 'values': embeddings.embed_query(j),
                    'metadata': {'title': file_name[:-4], 'article': article, 'text': article_content_list[k]}
                })
    
    return whole_text_list
# 엑셀 파일로 내보내기
# import csv
# f = open('C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/laws/laws.csv','w', newline='')
# wr = csv.writer(f)
# num = 1
# for i in whole_text_list:
#     wr.writerow([num, i['values'], i['metadata']])
#     num += 1
# f.close()

# 텍스트를 token_limit 이하로 자를 수 있는 chunk_size 반환
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
            return (chunk_size - 1)
        
def embedding_list_generator(whole_text_list, start_index):
    import uuid
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    llm = OpenAI()
    embeddings = OpenAIEmbeddings()

    whole_embed_list = []
    token_limit = 512
    for i in range(len(whole_text_list)):
        print(i)
        article = whole_text_list[i]
        token = llm.get_num_tokens(article['values'])
        text = article['values']
        if token > token_limit:
            # 해당 텍스트를 token_limit 이하로 자를 수 있는 chunk_size 반환
            chunk_size = token_calculator(texts=text, token_limit=token_limit)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
            splitted_text = text_splitter.split_text(text)
            for j in splitted_text:
                whole_embed_list.append((
                    'law-'+str(start_index),
                    embeddings.embed_query(j),
                    article['metadata']
                ))
                start_index += 1
        else:
            whole_embed_list.append((
                'law-'+str(start_index),
                embeddings.embed_query(text),
                article['metadata']
            ))
            start_index += 1

    return whole_embed_list
    # 엑셀 파일로 내보내기
    # import csv
    # f = open('C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/laws/laws.csv','w', newline='')
    # wr = csv.writer(f)
    # for i in whole_embed_list:
    #     wr.writerow([i['id'], i['values'], i['metadata']])
    # f.close()

# 실행되나?

# pinecone index 생성
def create_pinecone_index(index_name):
    import time

    if index_name in pinecone.list_indexes():
        pinecone.delete_index(index_name)

    # we create a new index
    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=1536  # 1536 dim of text-embedding-ada-002
    )

    # wait for index to be initialized
    while not pinecone.describe_index(index_name).status['ready']:
        time.sleep(1)

index_name = 'questionbot'
index = pinecone.Index(index_name)

file_directory = 'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/laws/content'
file_lists = os.listdir(file_directory)
# file = '공인중개사법.txt'
# print(file, '작업중')
# whole_text_list = whole_text_list_generator(file_directory=f'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/laws/content/{file}', file_name=file)
# print(len(whole_text_list))

# whole_embed_list = embedding_list_generator(whole_text_list)

# for i in whole_embed_list:
#     index.upsert(vectors=[i], namespace='law')

# print(index.describe_index_stats())

if index.describe_index_stats()['namespaces'] != {}:
  start_index = index.describe_index_stats()['namespaces']['law'] + 1
else:
  start_index = 1

for file in file_lists:
    print(file, '작업중')
    whole_text_list = whole_text_list_generator(file_directory=f'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/data/laws/content/{file}', file_name=file)
    print(len(whole_text_list))

    whole_embed_list = embedding_list_generator(whole_text_list, start_index)

    for i in whole_embed_list:
        index.upsert(vectors=[i], namespace='law')

    print(index.describe_index_stats())
