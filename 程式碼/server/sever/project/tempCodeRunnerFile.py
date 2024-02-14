import json

# 指定JSON文件的路径
json_file_path_traceroute = "E:/project/data/traceroute_log"
json_file_path_avg = "E:\project\data\traceroute_avg"
dashboard_path = "E:\project\data\dashboard.json"

# 函数：从JSON文件中读取数据
def read_json_file(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            # 从文件中加载JSON数据
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        return {}
    except Exception as e:
        return {}

# 函数：将数据写入JSON文件
def write_json_file(json_file_path, data):
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            # 将数据写入JSON文件
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"写入JSON文件时出错: {str(e)}")

# 读取最新的traceroute数据
latest_traceroute_data_list = read_json_file(json_file_path_traceroute)
if not latest_traceroute_data_list:
    print("无法读取最新的traceroute数据")
    exit()

traceorute_record = latest_traceroute_data_list[-1]
last_hop = traceorute_record['traceroute'][-1]['latency']
print(last_hop)
