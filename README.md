# mow
运行 Leek 项目的套利程序

## 仅供学习交流用,由买币与程序等造成的损失,概不负责!

* Bootstrap 项目: https://github.com/mangege/mow
* 套利业务逻辑: https://github.com/mangege/leek
* WebSocket 抓取深度数据: https://github.com/mangege/ccxtws

```sh
git submodule init
git submodule update

pip install -r ccxtws/requirements.txt
pip install -r leek/requirements.txt
```

### 环境变量配置

```
# 需要自己申请一个 Airbrake 帐号并创建项目,当交易时出异常时,会暂停交易并发送异常通知.
export AIRBRAKE_PROJECT_ID='111'
export AIRBRAKE_API_KEY='aaa'
export AIRBRAKE_ENVIRONMENT='development'

# 交易的 api key 配置,需要把变量名改成对应的交易所的
export GATEIO_API_KEY='KEY'
export GATEIO_SECRET='SEC'

# APP_LOG_PATH 日志目录的配置
```

### 修改套利交易对配置

修改 bin/move.py 文件即可,参数配置请看 https://github.com/mangege/leek/blob/master/base.py

### 运行

支持单进程运行多个交易对,只需要改 bin/move.py 文件,配置多个交易对即可.

多进程时运行,需要为每个进程设置不同的 APP_LOG_PATH 变量,否则多个进程写同一日志文件,会导致日志异常.

```
# 运行搬砖
# 因 ccxtws 与 leek 库是放在项目目录,所以需要修改 PYTHONPATH 变量.
# 同时你也可以自己编译 ccxt ,把 python 相关文件复制进来即可,这样方便添加自己的 ccxt 对接.
PYTHONPATH=.:$PYTHONPATH python bin/move.py
```

### ccxt 与 ws

理论上 ccxt 支持的交易所都支持,但 ws 只对接了几个,不支持的 ws ,需要自己改 ccxtws 库去对接.

### 运行数据采集

从程序的简单性(懒)考虑,运行相关的数据都是直接写到日志文件,需要自己配置 Telegraf 采集数据到 InfluxDB 之类的数据库,然后再用 Grafana 展示出来.

```
# Telegraf logparser 的两个 patterns 值

# 利润
    patterns = ["DEBUG - %{NOTSPACE:pair:tag} low buy ask_exchange %{NOTSPACE:ask_exchange:tag}, sell high bid_exchange %{NOTSPACE:bid_exchange:tag}, 交易成功,name %{NOTSPACE:name:tag} buy_num %{NUMBER:buy_num:float} 纯利润率 %{NUMBER:pure_rate:float} 大概利润 %{NUMBER:profit:float}"]

# 溢价
    patterns = ["DEBUG - %{NOTSPACE:pair:tag} low buy ask_exchange %{NOTSPACE:ask_exchange:tag}, sell high bid_exchange %{NOTSPACE:bid_exchange:tag}, - 卖价 %{NUMBER:ask_price:float} 数量 %{NUMBER:ask_num:float} - 买价 %{NUMBER:bid_price:float} 数量 %{NUMBER:bid_num:float} - 溢价 %{NUMBER:premium_rate:float} | 有溢价存在"]
```
