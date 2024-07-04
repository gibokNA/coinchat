# web_socket/consumers.py
import json, time, redis, os, subprocess
from channels.generic.websocket import AsyncWebsocketConsumer

os.chdir('/app')

subprocess.Popen('python3 /app/checker.py', shell=True)
subprocess.Popen('python3 /app/redis_to_ssd.py', shell=True)
subprocess.Popen('python3 /app/trade_checker.py', shell=True)

time.sleep(15)
#도커 실행 대기

rd = redis.StrictRedis(host='coinchat-redis', port=6379, db=0)
rd.set("live_connections", 0)

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "chat_group"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        try:
            triggered_list = json.loads(rd.get("triggered_list"))
        except:
            with open("/app/data/triggered_list.json", "r", encoding="utf-8") as f:
                triggered_list = json.load(f)

            rd.set("triggered_list", json.dumps(triggered_list, ensure_ascii=False).encode('utf-8'))

            triggered_list = json.loads(rd.get("triggered_list"))

        try:
            prev_message_list = json.loads(rd.get("prev_message_list").decode("utf-8"))
        except:
            with open("/app/data/prev_message_list.json", "r", encoding="utf-8") as f:
                prev_message_list = json.load(f)

            rd.set("prev_message_list", json.dumps(prev_message_list, ensure_ascii=False).encode('utf-8'))

            prev_message_list = json.loads(rd.get("prev_message_list").decode("utf-8"))

        try:
            change_rate_per_time_dict = json.loads(rd.get("change_rate_per_time_dict"))
        except:
            change_rate_per_time_dict = {
                "1h": [],
                "3h": [],
                "6h": [],
                "12h": [],
                "24h": []
            }

            rd.set("change_rate_per_time_dict", json.dumps(change_rate_per_time_dict))

            change_rate_per_time_dict = json.loads(rd.get("change_rate_per_time_dict"))

        try:
            trade_list = json.loads(rd.get("trade_list"))
        except:
            rd.set("trade_list", json.dumps([]))

            trade_list = json.loads(rd.get("trade_list"))

        await self.send(text_data=json.dumps({
            'send_name': "connect",
            'data': {
                'triggered_list': triggered_list,
                'prev_message_list': prev_message_list,
                'change_rate_per_time_dict': change_rate_per_time_dict,
                'trade_list': trade_list
            }
        }))

        try:
            live_connections = rd.get("live_connections").decode()
        except:
            rd.set("live_connections", 0)

            live_connections = rd.get("live_connections").decode()

        if int(live_connections) < 0:
            rd.set("live_connections", 0)

        try:
            rd.incr("live_connections")

            live_connections = rd.get("live_connections").decode()
        except:
            rd.set("live_connections", 0)

            rd.incr("live_connections")

            live_connections = rd.get("live_connections").decode()

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_func',
            'send_name': 'get_live_connections',
            'data': {
                "live_connections": live_connections
            }
        })

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        try:
            rd.decr("live_connections")

            live_connections = rd.get("live_connections").decode()
        except:
            rd.set("live_connections", 0)

            rd.decr("live_connections")

            live_connections = rd.get("live_connections").decode()

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_func',
            'send_name': 'get_live_connections',
            'data': {
                "live_connections": live_connections
            }
        })

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        nickname = text_data_json['nickname']
        message = text_data_json['message']
        ip_address = text_data_json['ip_address']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_func',
                'send_name': 'chat_message',
                'data': {
                    'text_data': {
                        'nickname': nickname,
                        'message': message,
                        'ip_address': ip_address
                    }
                }
            }
        )

        prev_message_list = json.loads(rd.get("prev_message_list").decode("utf-8"))

        prev_message_list.append({'nickname': nickname,'message': message,'ip_address': ip_address})

        rd.set("prev_message_list", json.dumps(prev_message_list, ensure_ascii=False).encode('utf-8'))

    async def send_func(self, event):
        await self.send(text_data=json.dumps({
            'send_name': event['send_name'],
            'data': event['data']
        }))
