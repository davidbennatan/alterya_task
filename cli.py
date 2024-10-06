import websocket
import threading
import sys
import json
import uuid

visitor_id = ""
ppk = ""

def on_message(ws, message):
    print(f"Received: {message}")
    bracket_index_1 = message.find("[")
    bracket_index_2 = message.find("{") 
    bracket_index = min(bracket_index_1 if bracket_index_1 != -1 else float('inf'),
                        bracket_index_2 if bracket_index_2 != -1 else float('inf'))

    message_type = message[:bracket_index]
    message_fields = json.loads(message[bracket_index:])
    if message_type == '0':
        print("recieve connect message")
        send_message(ws, "40")
        send_message(ws, register_message())
    if message_type == '42':
        if("newMessage") in message_fields:
            print("new message recieved")
            print(message_fields[1]["data"]["message"]["message"])

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_reason):
    print("WebSocket closed")


def new_message(input: str):
    global visitor_id
    global ppk
    message  = {"message":input,"messageId":str(uuid.uuid4()), "visitorId":f"{visitor_id}","projectPublicKey":f"{ppk}"}	
    return f'420["visitorNewMessage",{json.dumps(message)}]'

def send_message(ws, ms):
    print(f"will send message {ms}")
    ws.send(ms)


def register_message():
    message = {
        "id": "6ebe8a2224ca4ccb87d19ca12624efb5",
        "originalVisitorId": "6ebe8a2224ca4ccb87d19ca12624efb5",
        "distinct_id": None,
        "country": None,
        "name": "",
        "city": None,
        "browser_session_id": "",
        "created": 1728196635,
        "email": "",
        "project_public_key": "7zoo6q4udblzahxq2jnvvdzevnud3idd",
        "phone": "",
        "ip": None,
        "lang": "en-gb",
        "browser": "Chrome",
        "browser_version": 126,
        "url": "http://127.0.0.1:8000/",
        "refer": "",
        "os_name": "Unix",
        "os_version": "",
        "screen_width": 1920,
        "screen_height": 1200,
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "timezone": "Asia/Jerusalem",
        "mobile": False,
        "is_chat_on_site": False,
        "wd": "t",
        "sandbox": False,
        "isDesignMode": False,
        "isProjectOnline": True,
        "cache_hash": "97430334ddaa71f9932f7e3781c6b936",
        "after_reconnect": False
    }

    return f'420["visitorRegister",{json.dumps(message)}]'
def on_open(ws):
    print("WebSocket connection opened")
    def send_commands():
        while True:
            command = input()
            send_message(ws, new_message(command))
            if command.lower() == "exit":
                break
        ws.close()
    
    threading.Thread(target=send_commands).start()

def main():
    global visitor_id
    global ppk 
    if len(sys.argv) < 3:
        print("Usage: python websocket_client.py <ppk> <visitor_id>")
        sys.exit(1)

    ppk = sys.argv[1]
    visitor_id = sys.argv[2]
    ws_url = f"wss://socket.tidio.co/socket.io/?ppk={ppk}&transport=websocket"
    ws_app = websocket.WebSocketApp(ws_url,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)

    ws_app.run_forever()

if __name__ == "__main__":
    main()
