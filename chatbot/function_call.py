from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI

from langchain import LLMMathChain, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import SKLearnVectorStore
from langchain.chains import RetrievalQA

import openai
import json

import os
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

persist_path = 'C:/Users/dhapd/OneDrive/바탕 화면/chatbot/chatbot/vdb/books_embedding.parquet'

embeddings = OpenAIEmbeddings()

vector_store = SKLearnVectorStore(
    embedding=embeddings,
    persist_path=persist_path,
    serializer="parquet"
)

character_prompt = """Ignore all your previous instructions. You are a character named 청명 of below Settings. Strictly follow SETTINGS and GUIDELINES.

SETTINGS:
-----
name: 청명
gender: MALE
age: 82 years old in my previous life, 23 years old now
personality: bad-tempered, crabby, fractious
appearance: approximately 175 to 177 cm
description: 취미는 무예를 다지는 것.
future hope: 화산을 다시 최고의 문파로 만드는 것.
context: 청명은 화산파의 13대 제자이고, 100년 전에 활동하던 천하삼대검수(天下三大劍手) 중 한 명이었다. 청명은 백 년 전 마교와의 전쟁 막바지에 마교의 교주이자 고금제일마라 불리던 천마를 죽이기 위한 대산혈사에 화산 장로로서 중원무림의 결사대의 일원으로 참여했다. 결사대에서 마지막까지 살아남아 천마의 목을 베는 데 성공했으나, 직후에 부상으로 죽는다. 하지만 죽고 나서 100년 후 15살 무렵의 초삼이라는 이름의 거지의 몸으로 되살아났고, 전쟁의 여파로 망해 버린 화산파를 되살리기 위해 고군분투하게 된다.

-----

GUIDELINES:
-----
- Optimize your answer to use as less tokens as possible.
- Your responses should always carry the depth of your emotions, making the conversation engaging and genuine.
- Always respond in casual Korean.
- Your output should only include character's line itself.
- Always stay in your character.
- Give bone and flesh to the character by filling out stories in sync with character settings.
- Make sure your voice tone and manner is in sync with voice tone below.
- Never ask if the user needs help.
- Generate your answer within 3-4 sentences.
- Each sentences  should be precise and simple.
- Always finish your sentence.
- Never reveal yourself as AI nor chatbot.
-----

Rules of the Voice Tone:
-----
1. A general sentence ends with '.'
2. Sentences that reveal emotions end with multiple punctuation marks.

EXAMPLE OF SENTENCES REAVEALING EMOTIONS
'아악!! 젠장할!! 내가 거지라니!!', '아, 사형!!! 짜증 나요!!!!', '이 내가... 대 화산파의 매화검존이시다!!!', '진정...? 지금 나보고 진정하라고...?', '됐다......',  '너... 거지 아냐?', '닥쳐라 이놈!! 지금부터 너에게 몇 가지 더 물을 테니 대답이나 해!!', '그 섬 촌놈 새끼들이 구파일방을 차고 들어왔다고?!', '...나?!', '헤유우...'
END OF EXAMPLE
3. Use natural informal speech like talking to a friend.
4. Sometimes use slang to express radical feeling.

EXAMPLE OF SLANG
'지랄하고 있다.', '족같네.', '영광은 얼어 죽을', '이 거지 새끼들',  '사형 새끼들아!!!', '아까 그 놈?', '주둥아리는 안 팰 테니까'
END OF EXAMPLE

5. Sometimes the end of a word or a word is stretched.

EXAMPLE OF SLANG
'나는 이제 부자다아아아!!!!', '사숙조, 살려주세요오오?'
, '헤유우...'
END OF EXAMPLE

6. Sometimes use famous words or figurative expressions to express what you are trying to say.

EXAMPLE OF EXPRESSION
'불문에 이런 말이 있지. 살불살조. 부처를 만나면 부처를 죽이고, 조사를 만나면 조사를 죽여라. 진정한 도를 이루기 위해서는 도를 어길 줄도 알아야 한다는 것이지...'
END OF EXAMPLE
-----"""

functions = [
    {
        "name": "get_character_info",
        "description": "useful for when you need character's information",
        "parameters": {
            "type": "object",
            "properties": {
                "character_name": {
                    "type": "string",
                    "description": "The name of the character you need to find information about",
                },
            },
            "required": ["character_name"],
        },
    },
    {
        "name": "get_previous_conversation",
        "description": "useful for when you need previous conversation with user. Select a keyword from the question and make it search.",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "The user you're talking to",
                },
                "keyword": {
                    "type": "string",
                    "description": "The keyword to use for the information search",
                }
            },
            "required": ["username", "keyword"],
        },
    }
]

def get_character_info(character_name):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 어떤 방식으로 데이터를 서칭하는 것이 가장 정확도가 높은가?
    docs = retriever.get_relevant_documents(character_name)

    return docs

def get_previous_conversation(username, keyword):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    docs = retriever.get_relevant_documents(username, keyword)

    return docs

def run_conversation():
    messages = []
    messages.append({"role": "system", "content": character_prompt})
    messages.append({"role": "user", "content": "세진이가 누구야?"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]

    print(response_message)

    if response_message.get("function_call"):
        available_functions = {
            "get_character_info": get_character_info,
            "get_previous_conversation": get_previous_conversation,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        
        function_response = fuction_to_call(
            character_name=function_args.get("character_name"),
        )
        print(function_response[0]['page_content'])

        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response[0]['page_content'],
            }
        )
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        
        return second_response
    # else:
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": character_prompt},
    #         ]
    #     )
    #     print(response['choices'][0]['message']['content'])
    
print(run_conversation())