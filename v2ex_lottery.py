import os
import sys
import random
import requests
import time
from functools import lru_cache
import getpass
from datetime import datetime


# 请求限制配置
REQUEST_INTERVAL = 0.2  # 每次请求间隔 0.2 秒，限制每秒不超过 5 次请求
_last_request_time = 0

def rate_limited_request():
    global _last_request_time
    current_time = time.time()
    elapsed_time = current_time - _last_request_time
    if elapsed_time < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed_time)
    _last_request_time = time.time()

def install_dependencies():
    """安装所需的 Python 模块"""
    os.system("pip install --upgrade pysocks requests[socks]")
    print("所需的 Python 模块已安装！")

def get_lottery_numbers(date=None):
    """
    获取指定日期的排列五开奖号码，如果不指定日期则获取最近一期的开奖号码

    :param date: 日期格式为 YYYYMMDD
    :return: 开奖号码列表
    """
    base_url = "https://api.huiniao.top/interface/home/lotteryHistory?type=plw&limit=1"
    response = requests.get(base_url)
    if response.status_code != 200:
        raise ValueError(f"请求失败，状态码: {response.status_code}, 内容: {response.text}")
    
    data = response.json()
    if data["code"] != 1:
        raise ValueError(f"请求失败，消息: {data['info']}")
    
    last_draw = data["data"]["last"]
 
    # 获取指定日期的开奖结果
    first_draw_date = last_draw["day"].replace("-", "")
    target_draw_date = date
    
    if not date:
        target_draw_date = first_draw_date
        date = first_draw_date
    
    # 计算日期差
    first_draw_date = datetime.strptime(first_draw_date, "%Y%m%d")
    target_draw_date = datetime.strptime(target_draw_date, "%Y%m%d")
    days_difference = (first_draw_date - target_draw_date).days
    
    if days_difference < 0:
        raise ValueError(f"指定日期 {date} 在最近一期之后，无法获取开奖结果")
    
    page = days_difference + 1
    
    url = f"https://api.huiniao.top/interface/home/lotteryHistory?type=plw&page={page}&limit=1"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"请求失败，状态码: {response.status_code}, 内容: {response.text}")
    
    data = response.json()
    if data["code"] != 1:
        raise ValueError(f"请求失败，消息: {data['info']}")
    
    draw = data["data"]["data"]["list"][0]
    if not draw:
        raise ValueError(f"获取指定日期 {date} 的开奖结果失败，无法找到对应的开奖结果")
    open_time = draw["open_time"]
    numbers = [draw["one"], draw["two"], draw["three"], draw["four"], draw["five"]]
    numbers = int("".join(numbers))
    print(f"{open_time} 的开奖结果为：{numbers}")
    return numbers

def get_json_with_bearer_auth(url, token):
    """
    使用 Bearer Token 认证方式获取指定 URL 的 JSON 数据

    :param url: 请求的 API 地址
    :param token: Bearer Token
    :return: 返回解析后的 JSON 数据
    """
    rate_limited_request()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None
    response = requests.get(url, headers=headers, proxies=proxies)

    if response.status_code != 200:
        raise ValueError(f"请求失败，状态码: {response.status_code}, 内容: {response.text}")

    try:
        return response.json()
    except ValueError:
        raise ValueError("响应内容不是有效的 JSON 格式")
@lru_cache(maxsize=128)
def get_topic_info(topic_id, token):
    """
    获取主题信息

    :param topic_id: 主题 ID
    :param token: Bearer Token
    :return: 返回主题的结构体
    """
    url = f"https://www.v2ex.com/api/v2/topics/{topic_id}"
    return get_json_with_bearer_auth(url, token)
@lru_cache(maxsize=128)
def get_topic_replies(topic_id, token, p=1):
    """
    获取主题的指定页回复

    :param topic_id: 主题 ID
    :param token: Bearer Token
    :param p: 页数，默认为 1
    :return: 返回主题回复的列表
    """
    url = f"https://www.v2ex.com/api/v2/topics/{topic_id}/replies?p={p}"
    print(url)
    return get_json_with_bearer_auth(url, token)

def floor_lottery(total_floors, num_winners, seed=None):
    """
    随机抽取幸运楼层

    :param total_floors: 总楼层数
    :param num_winners: 中奖人数
    :param seed: 随机种子
    :return: 抽中的楼层号列表
    """
    if num_winners > total_floors:
        raise ValueError("中奖人数不能超过总楼层数")
    
    if seed is not None:
        random.seed(seed) 

    return sorted(random.sample(range(1, total_floors + 1), num_winners))

@lru_cache(maxsize=128)
def get_user_data_from_reply(topic_id, token, floor):
    """
    根据楼层号获取对应的用户数据

    :param topic_id: 主题 ID
    :param token: Bearer Token
    :param floor: 楼层号
    :return: 包含用户ID、回复内容和头像URL的字典
    """
    replies_per_page = 20
    page = (floor - 1) // replies_per_page + 1
    replies = get_topic_replies(topic_id, token, p=page)

    if not replies.get("success", False):
        raise ValueError("主题回复获取失败，请检查您的 Bearer Token 或主题 URL 是否正确")

    replies = replies.get("result", {})
    index_in_page = (floor - 1) % replies_per_page
    if index_in_page >= len(replies):
        raise ValueError(f"楼层 {floor} 超出当前页的回复范围")

    reply = replies[index_in_page]
    reply_id = reply.get("id", "未知回复")
    username = reply.get("member", {}).get("username", "未知用户")
    content = reply.get("content", "无内容")
    created = reply.get("created", "未知时间")
    member_url = reply.get("member", {}).get("url", "")
    avatar_url = reply.get("member", {}).get("avatar", "无头像")
    # 时间戳转换为可读格式
    created = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created))
    return {
        "page": page,
        "created": created,
        "reply_id": reply_id,
        "floor": floor,
        "username": username,
        "member_url": member_url,
        "content": content,
        "avatar_url": f"https:{avatar_url}" if avatar_url.startswith("//") else avatar_url
    }

def initialize_config():
    """初始化配置"""
    print("初始化配置中...")
    token = getpass.getpass("请输入您的 Bearer Token（请参考 https://www.v2ex.com/help/personal-access-token 访问 https://www.v2ex.com/settings/tokens 生成，安全起见输入后不会显示）: ")
    proxy = input("请输入代理地址 (如 socks5h://127.0.0.1:1080，留空表示不使用代理): ").strip() or None
    use_lottery_seed = input("是否使用排列五（每天 21:25 开奖）开奖结果作为种子 (Yes/No): ").strip().upper() or "No"

    # 保存到配置文件
    with open("config.txt", "w") as f:
        f.write(f"TOKEN={token}\n")
        f.write(f"PROXY={proxy}\n")
        f.write(f"USE_LOTTERY_SEED={use_lottery_seed}\n")

    print("配置完成！")

def load_config():
    """加载配置"""
    if not os.path.exists("config.txt"):
        raise ValueError("配置文件不存在，请先运行 `python v2ex_lottery.py init` 初始化配置！")

    config = {}
    with open("config.txt", "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            config[key] = value

    return config

def validate_and_refine_lottery_result(lucky_floors, topic_creator_id, seen_users, topic_id, token, total_floors, num_winners):
    """
    检查并递归调整抽奖结果，排除楼主和重复用户。
    
    :param lucky_floors: 当前抽取的楼层列表
    :param topic_creator_id: 楼主的用户ID
    :param seen_users: 已中奖的用户ID集合
    :param topic_id: 主题ID
    :param token: Bearer Token
    :param total_floors: 总楼层数
    :param num_winners: 中奖人数
    :return: 修正后的中奖楼层列表
    """
    valid_lucky_floors = []
    
    for floor in lucky_floors:
        user_data = get_user_data_from_reply(topic_id, token, floor)
        if not user_data:
            continue
        
        username = user_data["username"]
        if username == topic_creator_id or username in seen_users:
            continue  # 跳过楼主和重复用户
        
        valid_lucky_floors.append(floor)
        seen_users.add(username)
    
    # 计算还需补充的楼层数量
    remaining_count = num_winners - len(valid_lucky_floors)
    if remaining_count > 0:
        # 递归补充抽取剩余楼层
        additional_floors = floor_lottery(total_floors=total_floors, num_winners=remaining_count, seed=seed)
        valid_lucky_floors += validate_and_refine_lottery_result(
            additional_floors, topic_creator_id, seen_users, topic_id, token, total_floors, remaining_count
        )
    return valid_lucky_floors

def generate_markdown_table(lucky_floors_info):
    # 表格头
    table = [
        "| Created | Floor | UserName | Main page | Reply | Avatar |",
        "|----------|------|--------|----------|----------|------|"
    ]
    
    for floor_info in lucky_floors_info:
        created = floor_info['created']
        floor = floor_info['floor']
        username = floor_info['username']
        member_url = floor_info['member_url']
        reply_url = floor_info['reply_url']
        avatar_url = floor_info['avatar_url']
        content = floor_info['content']

        # 如果内容超过5个字符，则截取前5个字符并添加省略号
        if len(content) > 5:
            content = content[:5] + "..."
        
        # 添加表格行
        table.append(f"| {created} | {floor:03} 楼 | @{username} | [{username}]({member_url}) | [{content}]({reply_url}) | <img src=\"{avatar_url}\" width=\"48px\" height=\"48px\"> |")
    
    return "\n".join(table)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        # 初始化模式
        install_dependencies()
        initialize_config()
    else:
        # 主程序
        try:
            # 加载配置
            config = load_config()
            token = config["TOKEN"]
            proxy = config.get("PROXY")
            use_lottery_seed = config.get("USE_LOTTERY_SEED", "NO").upper()
            
            # 用户展示抽奖的时间
            draw_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 隐藏中间部分 token
            hidden_token = f"{token[:1]}-{'-' * 12}-{token[-1:]}"
            print(f"使用的 Token: {hidden_token}")
            print(f"使用的代理: {proxy or '无'}")

            # 输入主题 URL
            topic_url = input("请输入主题 URL: ").strip()
            topic_id = topic_url.split("t/")[-1].split("#")[0]

            # 获取主题信息
            topic_info = get_topic_info(topic_id, token)
            if not topic_info.get("success", False):
                print(f"错误: {topic_info["message"]}")
                raise ValueError("主题信息获取失败！请检查您的 Bearer Token 或主题 URL 是否正确")

            topic_info = topic_info.get("result", {})
            total_floors = topic_info.get("replies", 0)
            topic_title = topic_info.get("title", "未知主题")
            
            # 获取主题创建者 ID
            topic_creator_username = topic_info.get("member", {}).get("username", "未知用户")

            print(f"主题: {topic_title}")
            print(f"楼层总数: {total_floors}")

            # 用户输入抽奖参数
            max_floor = input(f"请输入抽奖楼层数 (默认 {total_floors}): ").strip()
            max_floor = int(max_floor) if max_floor else total_floors

            num_winners = input("请输入中奖人数 (默认 1): ").strip()
            num_winners = int(num_winners) if num_winners else 1
            
            # 询问是否使用最近一期的开奖结果作为种子
            if use_lottery_seed.upper() in ["Y", "YES"]:
                seed_choice = input("是否使用最近一期（每天 21:25 开奖）的排列五开奖结果作为随机数种子？(Yes/No/指定日期，如 20250101): ").strip().upper()
                if seed_choice.upper() in ["Y", "YES"]:
                    seed = get_lottery_numbers()
                elif seed_choice.upper() in ["N", "NO"]:
                    seed = None
                else:
                    seed = get_lottery_numbers(seed_choice)
            else:
                seed = None

            # 初次抽奖
            initial_lucky_floors = floor_lottery(total_floors=max_floor, num_winners=num_winners, seed=seed)

            # 递归调整抽奖结果
            seen_users = set()
            lucky_floors = validate_and_refine_lottery_result(
                initial_lucky_floors, topic_creator_username, seen_users, topic_id, token, total_floors, num_winners
            )
            
            print(f"\n抽奖结果（{draw_time}）:")

            lucky_floors_info = []
            for floor in lucky_floors:
                user_data = get_user_data_from_reply(topic_id, token, floor)
                reply_id = user_data["reply_id"]
                reply_url = f"{topic_url}#r_{reply_id}"
                lucky_floors_info.append({
                    **user_data,
                    "reply_url": reply_url
                })

            # 输出文本结果
            for floor_info in lucky_floors_info:
                print(f"{floor_info["created"]} 第 {floor_info['floor']:03} 楼： @{floor_info['username']}")
            
            
            print(f"\n如何验证抽奖结果（需要有python环境）：")
            print(f"1 访问 https://github.com/360card/v2ex-lottery 下载 v2ex-lottery") 
            print(f"2 执行命令：python v2ex-lottery.py init 初始化配置")
            print(f"3 执行命令：python v2ex-lottery.py 输入相同参数，重复执行抽奖程序")
            
            print(f"\nMarkdown 抽奖结果（{draw_time}）:\n")
            # 输出 markdown 结果
            markdown_table = generate_markdown_table(lucky_floors_info)
            print(markdown_table)
        except Exception as e:
            print(f"发生异常: {e}")
