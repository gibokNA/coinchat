import json, redis, time, os, django
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

time.sleep(15)
#도커 실행 대기

os.chdir('/app')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coinchat_backend_channels.settings")
django.setup()
    
rd = redis.StrictRedis(host='coinchat-redis', port=6379, db=0)

with open("/app/data/prev_message_list.json", "r", encoding="utf-8") as f:
    prev_message_list = json.load(f)

rd.set("prev_message_list", json.dumps(prev_message_list, ensure_ascii=False).encode('utf-8'))

channel_layer = get_channel_layer()

while 1:
    try:
        time.sleep(60)

        # prev_message_list 의 메시지 개수가 100 넘으면 오래된 것 부터 지워주기.

        prev_message_list = json.loads(rd.get("prev_message_list").decode("utf-8"))

        all_count = len(prev_message_list)

        if all_count > 100:
            remove_count = all_count - 100

            for i in range(remove_count):
                del prev_message_list[0]

        with open('/app/data/prev_message_list.json', 'w', encoding="utf-8") as f:
            json.dump(prev_message_list, f, ensure_ascii=False, indent="\t")

        rd.set("prev_message_list", json.dumps(prev_message_list, ensure_ascii=False).encode('utf-8'))

        ####################################################################################################################

        triggered_list = json.loads(rd.get("triggered_list"))

        with open('/app/data/triggered_list.json', 'w', encoding="utf-8") as f:
            json.dump(triggered_list, f, ensure_ascii=False, indent="\t")

        ####################################################################################################################
        
        trade_list = json.loads(rd.get("trade_list"))

        with open('/app/data/trade_list.json', 'w', encoding="utf-8") as f:
            json.dump(trade_list, f, ensure_ascii=False, indent="\t")

        ####################################################################################################################

        # 60초에 한번 change_rate_per_time_dict 보내주기.

        async_to_sync(channel_layer.group_send)("chat_group",
        {
            'type': 'send_func',
            'send_name': 'get_change_rate_per_time_dict',
            'data': {
                'change_rate_per_time_dict': json.loads(rd.get("change_rate_per_time_dict"))
            }
        })

    except Exception as e:
        print("에러발생")
        print(e)
