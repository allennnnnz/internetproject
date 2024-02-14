#取得網頁內文
import requests
from bs4 import BeautifulSoup
import hashlib
import openai

def get_and_parse_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("網頁訪問成功！")
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        return soup
    else:
        print("無法訪問網頁。HTTP回應狀態碼:", response.status_code)
        return None

def write_message(path,message):
    with open(path,'a', encoding='utf-8') as message_file:
                message_file.write(message) 

def update_hash_file(path,hash_value):
    with open(path, 'w', encoding='utf-8') as hash_file:
        hash_file.write(str(hash_value))
    print('Data updated.')

#產生hash string
def generate_hash(result):
    hash_value = hashlib.sha256(result.encode()).hexdigest()
    return hash_value

#比較hash相不相同
def compare_hashes(new_hash, hash_file_path):
    with open(hash_file_path, 'r', encoding='utf-8') as hash_file:
        hash_value_old = hash_file.read().strip()

    if hash_value_old == new_hash:
        print('Repeat data')
        return True  # 表示哈希值重複
    else:
        with open(hash_file_path, 'w', encoding='utf-8') as hash_file:
            hash_file.write(str(new_hash))
        return False  # 表示哈希值不重複

if __name__ == "__main__":
    main()
