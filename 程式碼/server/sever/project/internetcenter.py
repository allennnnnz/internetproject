import requests
from bs4 import BeautifulSoup
import hashlib
from web_crawer_lib import web_crawer
from line_notify_lib import notify

if __name__ == "__main__":
    url = "https://portal.tyrc.edu.tw/TyrcPortal/index.php/bulletin?fromtyrc=y"
    soup = web_crawer.get_and_parse_html(url)
    if soup:
        first_topic = soup.find("td", valign="top")
        first_row = soup.find("tr", bgcolor="ffecf5")
        
        br_tags = first_row.find_all("br")
        topic_word = first_topic.find("font").get_text()
        print("topic" + topic_word)
        index_list = [1, 2, 5, 7]
        result = "\n"
        for index in index_list:
            if len(br_tags) > index:
                content = br_tags[index].next_sibling.strip()
                result += content + "\n"
        print(result)
        
        hash_value = web_crawer.generate_hash(result)
        hash_file_path = r"E:\project\data\internet_hash.txt"
        is_repeated = web_crawer.compare_hashes(hash_value, hash_file_path)

        if True:
            # 使用 Line Notify 進行通知
            with open(r"E:\project\data\internet_center.txt", 'a', encoding='utf-8') as output_file:
                output_file.write(result)
            TOKEN = 'Bearer rILWdUokK0Z9WLdIN6yluyOejzdtNKV8TfECvD7l9kA'
            message = "\n" + result
            keywords = ["資安訊息", "漏洞預警"]
            levels = ["影響等級 中", "影響等級 高"]
            notify_result = ""
            if any(keyword in topic_word for keyword in keywords):
                print("符合通知關鍵字\n")
                if any(level in message for level in levels):
                    notify_result += message
                    response = notify.send_line_notification(notify_result,TOKEN)
                    with open(r"E:\project\data\internet_center.txt", 'a', encoding='utf-8') as message_file:
                        message_file.write(message)
                        print("message"+message)
            else:
                print("不符合通知條件\n")