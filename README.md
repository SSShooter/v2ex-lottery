# V2EX  抽奖小工具

## 已实现部分
- 代理配置，如http、https、socks、socks5、socks5h 代理等
- 抽奖，配置主题、抽到哪一楼层、获奖人数
- 显示获奖用户名并 At 该用户
- 显示获奖用户地址，方便用户提交获奖截图凭据 
- 显示定位到楼层的地址，方便用户提交获奖截图凭据

## 测试环境
- Windows 11
- python 3.12.8

## 使用举例
```
> python .\v2ex_lottery.py init
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already satisfied: pysocks in f:\documents\vscode\giffgaff\.conda\lib\site-packages (1.7.1)
Requirement already satisfied: requests[socks] in f:\documents\vscode\giffgaff\.conda\lib\site-packages (2.32.3)
Requirement already satisfied: charset-normalizer<4,>=2 in f:\documents\vscode\giffgaff\.conda\lib\site-packages (from requests[socks]) (3.4.1)
Requirement already satisfied: idna<4,>=2.5 in f:\documents\vscode\giffgaff\.conda\lib\site-packages (from requests[socks]) (3.10)
Requirement already satisfied: urllib3<3,>=1.21.1 in f:\documents\vscode\giffgaff\.conda\lib\site-packages (from requests[socks]) (2.3.0)
Requirement already satisfied: certifi>=2017.4.17 in f:\documents\vscode\giffgaff\.conda\lib\site-packages (from requests[socks]) (2024.12.14)
初始化配置中...
请输入您的 Bearer Token（通过 https://www.v2ex.com/settings/tokens 生成，为了保护输入后不会显示）:
请输入代理地址 (如 socks5h://127.0.0.1:1080，留空表示不使用代理): socks5h://127.0.0.1:1080
配置完成！

> python .\v2ex_lottery.py      
使用的 Token: 9--------------4
使用的代理: socks5h://127.0.0.1:1080
请输入主题 URL: https://www.v2ex.com/t/1103737
主题: T 楼 1.99 元 30 张英国 giffgaff， TG 群抽奖同步送 30 张，总计 60 张，为 giffgaff 中国的普及做贡献
楼层总数: 357
请输入抽奖楼层数 (默认 357):
请输入中奖人数 (默认 1): 5

抽奖结果:
2025-01-09 09:02:13 第 034 楼： @dave4one (https://www.v2ex.com/member/dave4one) (https://www.v2ex.com/t/1103737#r_15773414)
2025-01-09 10:21:05 第 123 楼： @3andwich (https://www.v2ex.com/member/3andwich) (https://www.v2ex.com/t/1103737#r_15774185)
2025-01-09 11:02:26 第 159 楼： @acorngyl (https://www.v2ex.com/member/acorngyl) (https://www.v2ex.com/t/1103737#r_15774634)
2025-01-09 14:51:27 第 246 楼： @Les1ie (https://www.v2ex.com/member/Les1ie) (https://www.v2ex.com/t/1103737#r_15776133)
2025-01-09 15:26:20 第 251 楼： @wangqiKylin (https://www.v2ex.com/member/wangqiKylin) (https://www.v2ex.com/t/1103737#r_15776349)
```




