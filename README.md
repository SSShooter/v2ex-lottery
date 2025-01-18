# V2EX 抽奖小工具
V2EX 抽奖小程序 was initiated by [@bfhyqy](https://www.v2ex.com/member/bfhyqy)

## 由来
第一次在 V2EX 做抽奖活动 [送 giffgaff](https://www.v2ex.com/t/1103737) ，遇到很多问题，好在顺利结束。TG群 [eSIM Card 交流群](https://t.me/esim_card_fans) 的 July 讲 V2EX 是有 [API](https://www.v2ex.com/help/personal-access-token) 的，于是心血来潮把抽奖的过程整理成 python 脚本。
真心希望能帮助到大家。

权且就自吹自擂叫它 V2EX 抽奖小程序，希望可以抛转引玉，大家不要见笑。

## 主要功能

目前实现了以下主要功能：
- 配置和重新配置 Token ，用于获取主题和回复，并写到配置文件
- 启用和停止代理，如http、https、socks、socks5、socks5h 等
- 省流，按需请求、缓存请求结果、限制访问 API 频率
- 排除楼主获奖的情况，排除其它用户重复获奖的情况
- 显示获奖用户名并 At 该用户；显示获奖用户地址，方便用户提交获奖截图凭据；显示定位到楼层的地址，方便用户提交获奖截图凭据
- 同时输出获奖用户的 markdown 表格

## 测试环境

欢迎大家提交PR，欢迎大家适配其它的环境。

- Windows 11
- python 3.12.8

## 部分运行结果展示

| Created | Floor | UserName | Main page | Reply | Avatar |
|----------|------|--------|----------|----------|------|
| 2025-01-09 14:13:26 | 234 楼 | @C0dEr | [C0dEr](https://www.v2ex.com/member/C0dEr) | [参与一下](https://v2ex.com/t/1103737#r_15775882) | <img src="https://cdn.v2ex.com/avatar/65f9/a4fe/160006_xxlarge.png?m=1715389329" width="48px" height="48px"> |
| 2025-01-13 14:32:18 | 354 楼 | @HaoBaiCai | [HaoBaiCai](https://www.v2ex.com/member/HaoBaiCai) | [参加一下](https://v2ex.com/t/1103737#r_15789345) | <img src="https://cdn.v2ex.com/avatar/a8bb/5fe6/589184_xxxlarge.png?m=1721140523" width="48px" height="48px"> |


## 运行过程展示

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

> python.exe .\v2ex_lottery.py 
使用的 Token: 9--------------4
使用的代理: socks5h://127.0.0.1:1080
请输入主题 URL: https://v2ex.com/t/1103737  
主题: T 楼 1.99 元 30 张英国 giffgaff， TG 群抽奖同步送 30 张，总计 60 张，为 giffgaff 中国的普及做贡献
楼层总数: 357
请输入抽奖楼层数 (默认 357): 
请输入中奖人数 (默认 1): 2
https://www.v2ex.com/api/v2/topics/1103737/replies?p=12
https://www.v2ex.com/api/v2/topics/1103737/replies?p=18

抽奖结果（2025-01-18 21:12:47）:
2025-01-09 14:13:26 第 234 楼： @C0dEr
2025-01-13 14:32:18 第 354 楼： @HaoBaiCai

Markdown 抽奖结果（2025-01-18 21:12:47）:

| Created | Floor | UserName | Main page | Reply | Avatar |
|----------|------|--------|----------|----------|------|
| 2025-01-09 14:13:26 | 234 楼 | @C0dEr | [C0dEr](https://www.v2ex.com/member/C0dEr) | [参与一下](https://v2ex.com/t/1103737#r_15775882) | <img src="https://cdn.v2ex.com/avatar/65f9/a4fe/160006_xxlarge.png?m=1715389329" width="48px" height="48px"> |
| 2025-01-13 14:32:18 | 354 楼 | @HaoBaiCai | [HaoBaiCai](https://www.v2ex.com/member/HaoBaiCai) | [参加一下](https://v2ex.com/t/1103737#r_15789345) | <img src="https://cdn.v2ex.com/avatar/a8bb/5fe6/589184_xxxlarge.png?m=1721140523" width="48px" height="48px"> |
```
