import json, ccxt, random, time, os, django, redis
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

time.sleep(15)
#도커 실행 대기

os.chdir('/app')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coinchat_backend_channels.settings")
django.setup()

channel_layer = get_channel_layer()

binance = ccxt.binance(config={
    'apiKey': "",
    'secret': "",
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

with open("/app/data/trade_list.json", "r", encoding="utf-8") as f:
    trade_list = json.load(f)

rd = redis.StrictRedis(host='coinchat-redis', port=6379, db=0)
rd.set("trade_list", json.dumps(trade_list))

prev_timestamp = 0

dollar_won = 1350

while 1:
    try:
        time.sleep(1)

        trades = binance.fetchTrades("BTC/USDT", limit=1000)

        for i in trades:
            if i["timestamp"] < prev_timestamp:
                continue

            if i["cost"] * dollar_won >= 500000000:
                if i["side"] == "buy":
                    side = "long"
                else:
                    side = "short"

                is_duplicated = False

                for j in trade_list:
                    if j["id"] == i["id"]:
                        is_duplicated = True

                if is_duplicated == True:
                    continue

                async_to_sync(channel_layer.group_send)("chat_group",
                {
                    'type': 'send_func',
                    'send_name': 'trade_checker',
                    'data': {
                        'trade_checker_data': {
                            "side": side,
                            "price": i["price"],
                            "cost": i["cost"],
                            "won": str(round(i["cost"] * dollar_won / 100000000)) + "억",
                            "id": i["id"]
                        }
                    }
                })

                trade_list.insert(0, {
                    "side": side,
                    "price": i["price"],
                    "cost": i["cost"],
                    "won": str(round(i["cost"] * dollar_won / 100000000)) + "억",
                    "id": i["id"]
                })

                trade_list = trade_list[0:10]

                rd.set("trade_list", json.dumps(trade_list))

        prev_timestamp = trades[-1]["timestamp"]

    except Exception as e:
        print("에러발생")
        print(e)

        time.sleep(60)

        print("루프 재시작")
