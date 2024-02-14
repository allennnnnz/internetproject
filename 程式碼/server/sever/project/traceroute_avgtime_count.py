import json

# 指定JSON文件的路径
json_file_path_traceroute = "E:/project/web/data/traceroute_log_webpage.json"
json_file_path_avg = "E:/project/web/data/traceroute_avg.json"

def read_json_file(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            # 从文件中加载JSON数据
            data = json.load(json_file)
            print("成功从文件中读取JSON数据")
            return data
    except FileNotFoundError:
        print(f"找不到文件: {json_file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"解析JSON数据时出错：{str(e)}")
        return []
    except Exception as e:
        print(f"发生了未知错误：{str(e)}")
        return []

def write_json_file(json_file_path, data):
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            # 将数据写回JSON文件
            json.dump(data, json_file, indent=4)  # 使用缩进美化输出
            print("成功将数据写入文件")
    except Exception as e:
        print(f"写入文件时出错：{str(e)}")

# 读取traceroute数据
traceroute_data = read_json_file(json_file_path_traceroute)

# 初始化平均数据字典
average_data = {}

# 计算平均traceroute数据
for traceroute_entry in traceroute_data:
    
    traceroute_results = traceroute_entry["traceroute"]

    hop_counter = {}  # 用于跟踪每个hop的计数

    for hop_entry in traceroute_results:
        hop = hop_entry["hop"]
        host = hop_entry["host"]
        latency = hop_entry["latency"]

        # 创建唯一标识符，结合hop和host
        hop_key = hop

        if hop_key in hop_counter:
            hop_counter[hop_key] += 1
            hop_key = f"{hop}_{hop_counter[hop_key]}"  # 在hop后添加计数
        else:
            hop_counter[hop_key] = 1  # 如果是第一次出现的hop，计数设为1

        # 检查是否需要进一步细分host
        if hop_key in average_data:
            existing_host = average_data[hop_key]["host"]
            if existing_host != host:
                if hop_key in hop_counter:
                    hop_counter[hop_key] += 1
                    hop_key = f"{hop}_{hop_counter[hop_key]}"  # 如果host不同，添加额外的计数
                else:
                    hop_counter[hop_key] = 1

        # 将字符串中的 " ms" 删除，并将结果转换为浮点数
        latency_values = [float(lat.replace(" ms", "")) for lat in latency]
        latency_sum = len(latency_values)  # 计算每次的latency有多少个数

        if hop_key not in average_data:
            average_data[hop_key] = {
                "host": host,
                "latency": latency_values,
                "latency_sum": latency_sum,
                "count": 1
            }
        else:
            # 如果跳已经在字典中，更新延迟时间总和和计数
            average_data[hop_key]["latency"] = [
                sum(x) for x in zip(average_data[hop_key]["latency"], latency_values)
            ]
            average_data[hop_key]["latency_sum"] += latency_sum
            average_data[hop_key]["count"] += 1

# 计算平均延迟时间（先相加，然后再平均）
for hop, data in average_data.items():
    total_latency = sum(data["latency"])
    latency_sum = data["latency_sum"]
    data["latency"] = round(total_latency / latency_sum, 3)

# 将平均数据写入JSON文件
write_json_file(json_file_path_avg, average_data)




