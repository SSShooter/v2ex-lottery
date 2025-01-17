# V2EX  抽奖小工具

## 已实现部分
- 支持（重新）配置 Token ，用于获取主题和回复，并写到配置文件
- 支持启用、停止代理，如http、https、socks、socks5、socks5h 等
- 支持省流，按需请求、缓存请求结果、限制访问 API 频率
- 排除楼主获奖的情况，排除其它用户重复获奖的情况
- 显示获奖用户名并 At 该用户
- 显示获奖用户地址，方便用户提交获奖截图凭据 
- 显示定位到楼层的地址，方便用户提交获奖截图凭据

## 计划实现
- 直接输出 markdown 语法
- 展示头像

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
请输入您的 Bearer Token（请参考 https://www.v2ex.com/help/personal-access-token 访问 https://www.v2ex.com/settings/tokens 生成，安全起见输入后不会显示）:
请输入代理地址 (如 socks5h://127.0.0.1:1080，留空表示不使用代理): socks5h://127.0.0.1:1080
配置完成！

> python .\v2ex_lottery.py 
使用的 Token: 9--------------4
使用的代理: socks5h://127.0.0.1:1080
请输入主题 URL: https://v2ex.com/t/1103737
主题: T 楼 1.99 元 30 张英国 giffgaff， TG 群抽奖同步送 30 张，总计 60 张，为 giffgaff 中国的普及做贡献
楼层总数: 357
请输入抽奖楼层数 (默认 357):
请输入中奖人数 (默认 1): 2
https://www.v2ex.com/api/v2/topics/1103737/replies?p=6
https://www.v2ex.com/api/v2/topics/1103737/replies?p=13

抽奖结果:
2025-01-09 10:17:01 第 117 楼： @mypchas6fans (https://www.v2ex.com/member/mypchas6fans) (https://v2ex.com/t/1103737#r_15774145)
2025-01-09 16:10:35 第 260 楼： @Trevor1 (https://www.v2ex.com/member/Trevor1) (https://v2ex.com/t/1103737#r_15776646)
```




