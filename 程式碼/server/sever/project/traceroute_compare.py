import json
import re
# 指定JSON文件的路径
json_file_path_traceroute = "E:/project/web/data/traceroute_log_webpage.json"
json_file_path_avg = "E:/project/web/data/traceroute_avg.json"
dashboard_path = "E:\project\web\data\dashboard.json"

pattern = r'\d+\.\d+'
def extract_numbers(input_string):
    return re.findall(pattern, input_string)
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

target_host = "dns.hinet.net (168.95.1.1)"

latency_values = None

# 读取最新的traceroute数据
latest_traceroute_data_list = read_json_file(json_file_path_traceroute)


#print(latest_traceroute_data_list[-7]["traceroute"])
for hop_data in latest_traceroute_data_list[-1]["traceroute"]:
    if hop_data["host"] == target_host:
        latency_values = hop_data["latency"]
        
        break
if not latest_traceroute_data_list:
    print("无法读取最新的traceroute数据")
    exit()
latency_values = [float(re.search(r'([\d.]+)', latency).group()) for latency in latency_values]

# 计算平均值
new_average_latency = sum(latency_values) / len(latency_values)

print("平均延迟:", new_average_latency)

oldavg_traceroute_data_list = read_json_file(json_file_path_avg)
target_host_latency = oldavg_traceroute_data_list["13"].get("latency")

print(new_average_latency)
print(target_host_latency)

exceed = int((float(new_average_latency) - float(target_host_latency)) / float(target_host_latency) * 100)
print(new_average_latency)
print(target_host_latency)
print(exceed)

dashboard_data = read_json_file(dashboard_path)

if exceed > 0:
    # 更新dashboard_data中的 'exceed' 字段
    dashboard_data[next(iter(dashboard_data.keys()))]['traceroute'][0]['exceed'] = exceed
    write_json_file(dashboard_path, dashboard_data)
else:
    dashboard_data[next(iter(dashboard_data.keys()))]['traceroute'][0]['exceed'] = 0
    write_json_file(dashboard_path, dashboard_data)


print(f"平均載入時間增長比例: {exceed:.2f}%")

# 暂时先读第一笔数据
count = int(next(iter(dashboard_data.values()))['traceroute'][0]['count'])

print(dashboard_data[next(iter(dashboard_data.keys()))]['traceroute'][0]['count'])
if exceed > 200:
    # 在if条件满足时，更新count字段
    dashboard_data[next(iter(dashboard_data.keys()))]['traceroute'][0]['count'] = count + 1
    write_json_file(dashboard_path, dashboard_data)
