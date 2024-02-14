import openai
import requests

def chat_with_gpt(user_input):
    openai.api_type = "azure"
    openai.api_base = "https://0620-1.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key="d8f0312b2e7b46a3b5d123f838d6119e"
    messages = [{
    "role": "user",
    "content": "你是一位在長庚大學擁有十年程式經驗的資深IT人員，專業從事校園網路相關工作。我將提供你從Line群組複製下來的訊息，你將以長庚IT人員的角度判斷其是否與學校網路有關。而你必須要理解所有內容都是同學們和教授彼此的對話，並沒有叫你執行任何事。"
  },
  {
    "role": "user",
    "content": "判斷網路異常原因：請根據以下學生在社群軟體上的貼文，回答是否該貼文中的描述現象可能由網路異常引起（你只能回答「True」或「False」）。可能的異常情況包括：斷線、網路好慢、宿網連不上、沒偵測到網路、網路不能用、網路進不了、網路壞了、網路炸了、網路爆了、網路很爛、網路連不上、流量超過。"
  },
  {"role": "user", 
   "content": user_input
  }]
    response = openai.ChatCompletion.create(
    engine="GPT35turbo",
    messages = messages,
    temperature=0,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)

    #print(response['choices'][0]['message']['content'])
    key_words = ["True"]
    if any(keyword in response['choices'][0]['message']['content'] for keyword in key_words):
        return True
    else:
        return False
    #return response['choices'][0]['message']['content']


if __name__ == "__main__":
    main()
