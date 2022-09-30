import os
import openpyxl 

from gaode_api import Gaode


def read_key():
    """  持久化key,便于读取 """
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_key')
    print(key_path)
    with open(key_path, 'r', encoding='utf-8') as f:
        key = f.read()
    return key


def load_source_list():
    # 读取excel表格（修改此处可打开不同的表格）
    w= openpyxl.load_workbook('两城市间公里数.xlsx', read_only=True)
    ws = w['Sheet1']
    source = []
    flag = 1
    for cell in ws:
        if flag:
            flag = 0
            continue
        elif cell[0].value is None:
            break
        else:
            source.append(cell[0].value)
    
    return source
def load_target_list():
    """自己可以自定义策略，我这里直接返回需要的目的地"""
    return ['荣成','临沂']

def save_file(source,target,location):
    loc = iter(location)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['出发城市','目标城市','公里数'])
    for s in source:
        for t in target:
            ws.append([s,t,next(loc)])
    wb.save('结果.xlsx')


# 读取用户私钥
key = read_key()
# 读取开始城市
sources = load_source_list()
# 读取目的地城市
targets= load_target_list()

sources_loc = []
targets_loc = []

gaode = Gaode(key=key)
# 计算出发城市Locs
for s in sources:
    location = gaode.get_city_location(s)
    sources_loc.append(location)
print("出发城市位置计算成功")
# 计算目的地城市locs
for t in targets:
    location = gaode.get_city_location(t)
    targets_loc.append(location)
print("目的城市位置计算成功")

# 计算两城市距离
loc = []
for s in sources_loc:
    for t in targets_loc:
        dis = gaode.get_distance(s,t)
        loc.append(dis)
print("两地位置计算成功")

# 保存Excel文件
save_file(sources,targets,loc)
print("执行完毕")



