from decouple import config

import openai
import json

openai.api_key = config('OPENAI_API_KEY')

BASE_MESSAGE = [
    {
        "role": "system",
        "content": "너는 훌륭한 코드리뷰 챗봇이야. 제공되는 질문과 코드를 잘 파악하고, 적절하게 리뷰를 해줘. 리뷰는 한글로 할거고, 코드블럭을 적절하게 사용해줘"
    }
]


def generate_messages(current, new):
    messages = json.loads(current)
    new_message = {"role": "user", "content": new}
    messages.append(new_message)
    return json.dumps(messages, ensure_ascii=False)


def generate_fullcontext(messages, response):
    messages = json.loads(messages)
    response = {"role": "assistant", "content": response}
    messages.append(response)
    return json.dumps(messages, ensure_ascii=False)


def generate_response(string):
    
    messages = BASE_MESSAGE[:]
    messages.extend(json.loads(string))

    messages = json.dumps(messages, ensure_ascii=False)

    # print(messages)

    # response = openai.Completion.create(
    #     # engine="gpt-3.5-turbo",
    #     engine="text-davinci-002",
    #     prompt = messages,
    #     # prompt="'User': '안녕'",
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )

    # response = response.choices[0].text.strip()

    response = "hello"

    return generate_fullcontext(string, response)




