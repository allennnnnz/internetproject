import json

# 指定JSON文件的路径
json_file_path_history = "E:/project/web/data/webloading_history_webpage.json"
json_file_path_avg = "E:/project/web/data/webloading_avg_webpage.json"

def read_json_file(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            # 从文件中加载JSON数据
            data = json.load(json_file)
            print("成功从文件中读取JSON数据")
            return data
    except FileNotFoundError:
        print(f"找不到文件: {json_file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"解析JSON数据时出错：{str(e)}")
        return {}
    except Exception as e:
        print(f"发生了未知错误：{str(e)}")
        return {}

def write_json_file(json_file_path, data):
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            # 将数据写回JSON文件
            json.dump(data, json_file, indent=4)  # 使用缩进美化输出
            print("成功将数据写入文件")
    except Exception as e:
        print(f"写入文件时出错：{str(e)}")

# 读取历史数据
loaded_data_history = read_json_file(json_file_path_history)

# 初始化平均数据字典
average_data = {}

# 计算历史平均加载时间
for entry in loaded_data_history:
    timestamp = entry["timestamp"]
    for website_data in entry["data"]:
        website_id = website_data["id"]
        loading_time = website_data["loading_time"]

        if website_id not in average_data:
            average_data[website_id] = {
                "load_time_seconds": loading_time,
                "url": website_data["url"],
                "count": 1
            }
        else:
            # 如果网站已经在字典中，更新加载时间总和和计数
            average_data[website_id]["load_time_seconds"] += loading_time
            average_data[website_id]["count"] += 1

# Calculate the average value and round to three decimal places
for website_id, data in average_data.items():
    data["load_time_seconds"] /= data["count"]
    data["load_time_seconds"] = round(data["load_time_seconds"], 3)
# 将平均数据写入JSON文件
write_json_file(json_file_path_avg, average_data)
