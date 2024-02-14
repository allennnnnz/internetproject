import json

# 指定JSON文件的路径
json_file_path_webloading = "E:/project/web/data/webloading_history_webpage.json"
json_file_path_avg = "E:/project/web/data/webloading_avg_webpage.json"
dashboard_path = "E:\project\web\data\dashboard.json"

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
latest_traceroute_data_list = read_json_file(json_file_path_webloading)
if not latest_traceroute_data_list:
    print("无法读取最新的traceroute数据")
    exit()

# 从列表中获取第一个对象
for latest_traceroute_data in latest_traceroute_data_list:
    # 提取每个对象中的 'loading_time' 字段值
    new_loading_times = [entry['loading_time'] for entry in latest_traceroute_data['data']]

new_average = sum(new_loading_times) / len(new_loading_times)

# 读取avg_traceroute数据
avg_traceroute_data_list = read_json_file(json_file_path_avg)
if not avg_traceroute_data_list:
    print("无法读取avg_traceroute数据")
    exit()

# 从列表中获取第一个对象
for avg_traceroute_data in avg_traceroute_data_list:
    # 提取每个对象中的 'load_time_seconds' 字段值
    old_loading_times = [entry['load_time_seconds'] for entry in avg_traceroute_data_list.values()]

dashboard_data = read_json_file(dashboard_path)
old_average = sum(old_loading_times) / len(old_loading_times)

print(new_average)
print(old_average)

# 计算 exceed 值并转换为整数
exceed = int((new_average - old_average) / old_average * 100)

if exceed > 0:
    # 更新dashboard_data中的 'exceed' 字段
    dashboard_data[next(iter(dashboard_data.keys()))]['webloading'][0]['exceed'] = exceed
    write_json_file(dashboard_path, dashboard_data)
else:
    dashboard_data[next(iter(dashboard_data.keys()))]['webloading'][0]['exceed'] = 0
    write_json_file(dashboard_path, dashboard_data)


print(f"平均載入時間增長比例: {exceed:.2f}%")

# 暂时先读第一笔数据
count = int(next(iter(dashboard_data.values()))['webloading'][0]['count'])

print(dashboard_data[next(iter(dashboard_data.keys()))]['webloading'][0]['count'])
if exceed > 200:
    # 在if条件满足时，更新count字段
    dashboard_data[next(iter(dashboard_data.keys()))]['webloading'][0]['count'] = count + 1
    write_json_file(dashboard_path, dashboard_data)
