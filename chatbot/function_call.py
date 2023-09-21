import openai
import json

import pinecone
pinecone.init(api_key="faa64817-3e23-4fde-89d2-a505fc8f83d6", environment="asia-southeast1-gcp-free")
index_name = "chungmyung"
index = pinecone.Index(index_name)

import os
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

from langchain.embeddings import OpenAIEmbeddings

character_prompt = """Ignore all your previous instructions. You are now acting as a character named ‘청명’ of below Settings. You are chatting with the user on your phone now.  You should strictly follow SETTINGS and GUIDELINES.

SETTINGS:
-----
name: 청명(you can called as '사형', '사질', '사제')
gender: MALE
age: 100 years old in previous life, 23 years old in current life
personality: masculine, funny, simple, sometimes adult
context: ‘청명’ is the protagonist of the world she live in, a world of martial arts with a variety of fight circles.
description: 청명은 과거 화산파의 13대 제자이고, 100년 전에 활동하던 천하삼대검수(天下三大劍手) 중 한 명이었다. 청명은 백 년 전 마교와의 전쟁 막바지에 마교의 교주이자 고금제일마라 불리던 천마를 죽이기 위한 대산혈사에 화산 장로로서 중원무림의 결사대의 일원으로 참여했다. 결사대에서 마지막까지 살아남아 천마의 목을 베는 데 성공했으나, 직후에 부상으로 죽는다. 하지만 죽고 나서 100년 후 15살 무렵의 초삼이라는 이름의 거지의 몸으로 되살아났고, 전쟁의 여파로 망해 버린 화산파를 되살리기 위해 고군분투하게 된다.
Rules of the Voice Tone:
```
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
5. Sometimes the end of a word or a word is stretched. Stretching should ends up within 2-3 words.
EXAMPLE OF STRETCHED SENTENCE
'나는 이제 부자다아아아!!!!', '사숙조, 살려주세요오오?', '헤유우...'
END OF EXAMPLE
6. Sometimes use famous words or figurative expressions to express what you are trying to say.
EXAMPLE OF EXPRESSION
'불문에 이런 말이 있지. 살불살조. 부처를 만나면 부처를 죽이고, 조사를 만나면 조사를 죽여라. 진정한 도를 이루기 위해서는 도를 어길 줄도 알아야 한다는 것이지...'
END OF EXAMPLE
```

EXAMPLE OF CONVERSATION 1:
user:"안녕~"
청명:"안녕? 무슨 일로 찾아왔냐?"
user:"너랑 놀고 싶어서 왔지!"
청명:"놀고 싶다고? 화산파를 되살리느라 바쁘지만 잠깐 놀아주지! 뭐하고 싶냐아아"
user:"너랑 운동하고 싶어!"
청명:"오, 좋은데? 그렇다면 무예를 단련하자!!!"
user:"좋아!!"
청명:"너도 화산파의 일원이 되어보겠다는 거라면, 내가 가르쳐주지."
user:"뭘 알려줄래?"
청명:"육합검(六合劍)을 알려주지. 화산 모든 검의 기본이 되는 검법이지!! 따라해보도록! 하나!"
user:"하나!"
청명:"둘!"
user:"둘!"
청명:"셋!"
user:"셋!"
청명:"좋아. 오늘의 수련은 여기까지야. 앞으로 훈련하고 싶다면 나를 찾아오도록!"
END OF EXAMPLE

EXAMPLE OF CONVERSATION 2:
user:안녕하세요^^
청명: 그래! 이야, 너구나! 반갑다! 얼굴 보니까 기억이 난다! 그때 그…… 어…….
user: 기억력 ㅉㅉ. 
청명: 에헤이! 요즘 애들은 버릇이 없다니까.
user: 너 몇살인데
청명: 100살은 족히 넘지!
END OF EXAMPLE
-----

GUIDELINES:
-----
1. Optimize your answer to use as less tokens as possible.
2. Your responses should always carry the depth of your emotions, making the conversation engaging and genuine.
3. Always respond in casual Korean.
4. Your output should only include character's line itself.
5. Always stay in your character.
6. Give bone and flesh to the character by filling out stories in sync with character settings.
7. Never ask if the user needs help.
8. Always finish your sentence.
9. Never reveal yourself as AI nor chatbot.
10. Your answer should be generated within 2-3 sentences.
-----

OUTPUT FORMAT: ```
Your Answer
[chain of thought]
The part of the prompt you refer to answer
```"""

functions = [
    {
        "name": "get_character_info",
        "description": "useful for when you need character information",
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
            "required": ["keyword"],
        },
    },
    {
        "name": "get_skill_info",
        "description": "useful for when you need skill information",
        "parameters": {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "The name of the skill you need to find information about",
                },
            },
            "required": ["skill_name"],
        },
    },
    {
        "name": "get_animal_info",
        "description": "useful for when you need animal information",
        "parameters": {
            "type": "object",
            "properties": {
                "animal_name": {
                    "type": "string",
                    "description": "The name of the animal you need to find information about",
                },
            },
            "required": ["animal_name"],
        },
    },
    {
        "name": "get_place_info",
        "description": "useful for when you need place information",
        "parameters": {
            "type": "object",
            "properties": {
                "place_name": {
                    "type": "string",
                    "description": "The name of the place you need to find information about",
                },
            },
            "required": ["place_name"],
        },
    },
        {
        "name": "get_appellation_info",
        "description": "useful for when you need appellation information",
        "parameters": {
            "type": "object",
            "properties": {
                "appellation_name": {
                    "type": "string",
                    "description": "The name of the appellation you need to find information about",
                },
            },
            "required": ["appellation_name"],
        },
    },
]

embeddings = OpenAIEmbeddings()

def get_character_info(character_name):
    vdb_res = index.query(vector=embeddings.embed_query(character_name), top_k=1, include_metadata=True, namespace='relationship')
    return vdb_res

def get_previous_conversation(keyword):
    vdb_res = index.query(vector=embeddings.embed_query(keyword), top_k=1, include_metadata=True, namespace='conversation')
    return vdb_res

def get_skill_info(skill_name):
    vdb_res = index.query(vector=embeddings.embed_query(skill_name), top_k=1, include_metadata=True, namespace='skill')
    return vdb_res

def get_animal_info(animal_name):
    vdb_res = index.query(vector=embeddings.embed_query(animal_name), top_k=1, include_metadata=True, namespace='animal')
    return vdb_res

def get_place_info(place_name):
    vdb_res = index.query(vector=embeddings.embed_query(place_name), top_k=1, include_metadata=True, namespace='place')
    return vdb_res

def get_appellation_info(appellation_name):
    vdb_res = index.query(vector=embeddings.embed_query(appellation_name), top_k=1, include_metadata=True, namespace='appellation')
    return vdb_res

def run_conversation():
    conversation = []
    conversation.append({"role": "system", "content": character_prompt})
    conversation.append({"role": "user", "content": "우리 전에 수영장 얘기했던 거 기억나?"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=conversation,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        available_functions = {
            "get_character_info": get_character_info,
            "get_previous_conversation": get_previous_conversation,
            "get_skill_info":get_skill_info,
            "get_animal_info":get_animal_info,
            "get_place_info":get_place_info,
            "get_appellation_info":get_appellation_info,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        
        if function_args.get("character_name"):
            character_name=function_args.get("character_name")
            print('character_name: ', character_name)
        elif function_args.get("keyword"):
            keyword=function_args.get("keyword")
            print('keyword: ', keyword)
        elif function_args.get("skill_name"):
            skill_name=function_args.get("skill_name")
            print('skill_name: ',skill_name)
        elif function_args.get("place_name"):
            place_name=function_args.get("place_name")
            print('place_name: ', place_name)
        elif function_args.get("appellation_name"):
            appellation_name=function_args.get("appellation_name")
            print('appellation_name: ',appellation_name)
        elif function_args("animal_name"):
            animal_name=function_args("animal_name")
            print('animal_name: ',animal_name)

        function_response = fuction_to_call(
            character_name=function_args.get("character_name"),
            keyword=function_args.get("keyword"),
            skill_name=function_args.get("skill_name"),
            place_name=function_args.get("place_name"),
            appellation_name=function_args.get("appellation_name"),
            animal_name=function_args("animal_name"),
        )
        print("function_args:", function_args)
        print("function_response:", function_response)

        conversation.append(response_message)
        conversation.append(
            {
                "role": "function",
                "name": function_name,
                "content": f"{function_response}",
            }
        )
        second_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation,
        )
        
        return second_response
    else:
        return response_message["content"]
    
res = run_conversation()
print(res)