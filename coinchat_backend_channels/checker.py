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

markets = binance.load_markets()
symbol_list = []

for i in markets:
    if "/USDT" in i:
        symbol_list.append(i)

random.shuffle(symbol_list)

triggered_dict = {}

for i in symbol_list:
    triggered_dict[i] = {
        "symbol": i,
        "triggered_time": time.time(),
        "change_rate": 0,
        "side": ""
    }

with open("/app/data/triggered_list.json", "r", encoding="utf-8") as f:
    triggered_list = json.load(f)

change_rate_per_time_dict = {
    "1h": [],
    "3h": [],
    "6h": [],
    "12h": [],
    "24h": []
}

rd = redis.StrictRedis(host='coinchat-redis', port=6379, db=0)
rd.set("triggered_list", json.dumps(triggered_list))
rd.set("change_rate_per_time_dict", json.dumps(change_rate_per_time_dict))

while 1:
    try:
        random.shuffle(symbol_list)

        change_rate_per_time_dict = {
            "1h": [],
            "3h": [],
            "6h": [],
            "12h": [],
            "24h": []
        }

        for i in symbol_list:
            if time.time() - 1800 > triggered_dict[i]["triggered_time"]:
                triggered_dict[i]["triggered_time"] = time.time()
                triggered_dict[i]["change_rate"] = 0
                triggered_dict[i]["side"] = ""

        for i in symbol_list:
            time.sleep(0.15)

            kline = binance.fetch_ohlcv(
                symbol=i,
                timeframe='1m',
                since=None,
                limit=1440)

            if len(kline) != 1440:
                continue

            ##############################################################################################

            if float(kline[-3][4]) < float(kline[-1][4]):
                side = "long"
            else:
                side = "short"

            price_list = []

            for j in range(1, 4):
                price_list.append(float(kline[-j][2]))
                price_list.append(float(kline[-j][3]))

            high = max(price_list)
            low = min(price_list)

            if side == "long":
                change_rate = abs(round((high / low) * 100 - 100, 2))
            else:
                change_rate = abs(round((low / high) * 100 - 100, 2))

            ##############################################################################################

            is_prev_triggered = False

            for j in [1, 2, 3]:
                triggered_target = "v" + str(j)

                if change_rate >= j:
                    if triggered_dict[i]["change_rate"] < change_rate or is_prev_triggered == True:
                        is_prev_triggered = True

                        triggered_dict[i]["side"] = side
                        triggered_dict[i]["change_rate"] = change_rate
                        triggered_dict[i]["triggered_time"] = time.time()
                
                        async_to_sync(channel_layer.group_send)("chat_group",
                        {
                            'type': 'send_func',
                            'send_name': 'checker_triggered',
                            'data': {
                                'triggered_data': triggered_dict[i],
                                'version': triggered_target
                            }
                        })

                        for j_index, j_value in enumerate(triggered_list[triggered_target]):
                            if j_value["symbol"] == i:
                                del triggered_list[triggered_target][j_index]

                                break

                        triggered_list[triggered_target].insert(0, {
                            "symbol": i,
                            "triggered_time": time.time(),
                            "change_rate": change_rate,
                            "side": side
                        })

                        triggered_list[triggered_target] = triggered_list[triggered_target][0:10]

                        rd.set("triggered_list", json.dumps(triggered_list))

            ##############################################################################################

            for j in [1380, 1260, 1080, 720, 0]:
                time_price_list = [float(kline[j][4]), float(kline[-1][4])]

                if float(kline[j][4]) < float(kline[-1][4]):
                    time_side = "long"
                    time_change_rate = abs(round((max(time_price_list) / min(time_price_list)) * 100 - 100, 2))
                else:
                    time_side = "short"
                    time_change_rate = abs(round((min(time_price_list) / max(time_price_list)) * 100 - 100, 2))

                time_str = ""

                if j == 1380:
                    time_str = "1h"
                elif j == 1260:
                    time_str = "3h"
                elif j == 1080:
                    time_str = "6h"
                elif j == 720:
                    time_str = "12h"
                elif j == 0:
                    time_str = "24h"

                change_rate_per_time_dict[time_str].append({
                    "symbol": i,
                    "side": time_side,
                    "change_rate": time_change_rate
                })

        ############################################################################################

        for i in ["1h", "3h", "6h", "12h", "24h"]:
            sorted_list = sorted(change_rate_per_time_dict[i], key=lambda x: x["change_rate"])
            sorted_list.reverse()
            change_rate_per_time_dict[i] = sorted_list[0:10]

            for j in range(10):
                change_rate_per_time_dict[i][j]["index"] = j + 1

        rd.set("change_rate_per_time_dict", json.dumps(change_rate_per_time_dict))

        """
        여기서 redis에 change_rate_per_time_dict 저장
        group_send는 tech처리하는곳에서 할거임.
        """

    except Exception as e:
        print("에러발생")
        print(e)

        time.sleep(60)

        print("루프 재시작")
