import asyncio
import hashlib
import datetime  # 匯入 datetime 模組
from pyppeteer import launch
from bs4 import BeautifulSoup
import os
import requests
from web_crawer_lib import web_crawer
from  chat_gpt_lib import chat_gpt
from line_notify_lib import notify

import openai

async def main():
    hash_value = None
    hash_value_new = None
    hash_path = r"E:\project\data\dcard_hash.txt"
    message_path = r"E:\project\data\dcard.txt"
    dcard_TOKEN = 'Bearer OPA5dwUiJABeVQsxCXVjty29XbhBLaUsXjG9m72mp0K'
    try:
        browser = await launch(headless=True)  # 啟動瀏覽器
        page = await browser.newPage() 
        await page.deleteCookie()
        await page.goto('https://www.dcard.tw/f/cgu?tab=latest')  # 讓瀏覽器分頁跳到指定網址
        await asyncio.sleep(1)
        content = await page.content()  # 獲取瀏覽器分頁現在顯示的網頁內容
        soup = BeautifulSoup(content, 'html.parser')  # 使用 BeautifulSoup 解析網頁內容
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    try:
        article = soup.find('article')  # 從解析後的網頁內容中找出 <article> 標籤

        if article:  # 如果找到了 <article> 標籤
            spans = article.find_all('span')  # 找出所有的 <span> 標籤
            span_text = ""  # 初始化一個空字串，用來存放所有 <span> 標籤的文字內容
            span_count = 0
            for span in spans:  # 對於每一個 <span> 標籤
                text = span.text.strip()  # 獲取 <span> 標籤的文字內容，去除前後的空白
                text = text.replace('\n', ' ')  # 將文字內容中的換行符號替換為空格
                span_text += text + " "  # 將處理過的文字內容加到 span_text 的後面
            
            print(span_text)
            # 使用 SHA-256 雜湊函數將字串轉換為雜湊值
            hash_value_new = web_crawer.generate_hash(span_text)
        
    except Exception as e:
        print(f"An error occurred while parsing the HTML: {str(e)}")  # 如果解析網頁內容時發生錯誤，則輸出一個訊息
    finally:
        await page.deleteCookie(*await page.cookies())
        await browser.close()  # 關閉瀏覽器
    span_text = "測試專題程式用 網路又斷線了，學校網路又連不上了"
    compare_result = web_crawer.compare_hashes(hash_value_new,hash_path)
    if not compare_result:  # 如果上一次和這一次爬到的文章相同
        web_crawer.update_hash_file(hash_path,hash_value_new)
        Chat_result = chat_gpt.chat_with_gpt(span_text)
        if(Chat_result):
            #當chatgpt判斷為網路問題時傳送通知
            with open(message_path, 'a', encoding='utf-8') as file:
                file.write(span_text)
            response = notify.send_line_notification(span_text,dcard_TOKEN)
            current_time = datetime.datetime.now()
            message = str(current_time) + "\n" + span_text + "\n" + "網路壞了救命"
            print(response)
        else:
            print("與網路無關")

asyncio.run(main())  # 執行上面定義的 main() 函數