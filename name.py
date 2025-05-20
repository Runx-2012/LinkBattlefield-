P_list = {}
P_list[1] = [5,45,3,1,0,"黑骑士",1,0]
P_list[2] = [1,39,1,5,0,"莫玄",1,0]
P_list[3] = [4,70,2,2,0,"冰雷",2,0]
P_list[4] = [5,48,3,4,0,"火毒",2,0]
P_list[5] = [8,100,2,7,0,"圣骑",1,0]
P_list[6] = [8,40,5,7,0,"队长",1,0]
P_list[7] = [3,58,2,5,0,"英雄",1,0]
P_list[8] = [4,135,1,1,0,"船长",2,0]
P_list[9] = [4,70,2,3,0,"神射",1,0]
P_list[10] = [8,200,1,7,0,"箭神",1,0]
P_list[11] = [5,87,2,2,0,"炎术士",2,0]
P_list[12] = [2,39,2,5,0,"夜行者",1,0]
P_list[13] = [5,48,3,4,0,"侠影",1,0]
P_list[14] = [1,39,1,5,0,"战神",1,0]
P_list[15] = [1,18,2,3,0,"幻影",2,0]
P_list[16] = [2,35,2,2,0,"唤灵",2,0]
P_list[17] = [4,59,2,4,0,"红毛",1,0]
P_list[18] = [8,200,1,7,0,"魂骑士",1,0]
P_list[19] = [5,44,5,8,0,"白毛",1,0]
P_list[20] = [2,33,2,9,0,"机械师",2,0]
P_list[21] = [3,23,1,11,0,"隐士",1,0]
P_list[22] = [2,67,1,9,0,"奇袭者",1,0]
P_list[23] = [6,60,3,10,0,"风灵",1,0]
P_list[24] = [3,55,2,8,0,"夜光",2,0]
P_list[25] = [3,25,4,9,0,"火炮",1,0]
P_list[26] = [5,111,2,8,0,"双刀",1,0]
P_list[27] = [3,19,2,4,0,"隐月",1,0]
P_list[28] = [6,60,3,10,0,"施亚",2,0]
P_list[29] = [4,29,3,11,0,"尖兵",1,0]
P_list[30] = [5,33,4,11,0,"龙神",2,0]
P_list[31] = [3,53,2,1,0,"双弩",1,0]
P_list[32] = [6,540,2,10,0,"主教",2,0]



X ={1: [1, 4, 26, 22, 14, 2, 15, 12, 16]}

T = {k:v for k,v in X.items() if v[0] not in []}
print(T)
# 转换后的结果字典
result = {}

# 遍历字典 X 的每个键值对
for key, num_list in T.items():
    # 初始化当前键对应的结果列表
    current_roles = []
    for num in num_list:
        # 从 P_list 中获取对应数字的角色名称（注意 P_list 的键是整数，需转换类型）
        if num in P_list:
            current_roles.append(P_list[num][5])  # P_list[num][5] 对应角色名称
        else:
            current_roles.append(f"未知角色（编号{num}）")  # 处理可能的缺失键
    # 将结果存入新字典
    result[key] = current_roles
first_five_results = {key:value[:5] for key,value in result.items()}
 ##打印结果（可选：如需输出到控制台可取消注释）

for key, roles in result.items():
    print(f"Key {key} 对应的角色列表：{roles}")

def deduplicate_dict(dictionary):
    seen_values = set()
    new_dict = {}
    for key, value in dictionary.items():
        # 把value转换为可哈希类型，这样才能放到set里
        try:
            hashable_value = tuple(value) if isinstance(value, list) else value
        except TypeError:
            # 要是value无法哈希，就转为字符串表示
            hashable_value = str(value)
        # 只保留首次出现的value
        if hashable_value not in seen_values:
            seen_values.add(hashable_value)
            new_dict[key] = value
    return new_dict

# 对X字典进行去重操作
X_deduplicated = deduplicate_dict(first_five_results)

# 输出去重后的结果
print("去重后的字典：")
for key, value in X_deduplicated.items():
    print(f"键 {key}: 值 {value}")


