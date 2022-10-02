import time
from websocket import create_connection
import ssl
import json
import requests


class PyChatAdminBot:
    def __init__(self):
        self.token = ""
        self.users = dict()
        self.routes = list()
        self.history = dict()
        self.login_as_admin()
        self.ws = create_connection(f'wss://localhost/ws?id=&sessionId={self.token}',
                                    sslopt={"cert_reqs": ssl.CERT_NONE})

    def create(self):
        self.get_users_()
        messages = self.get_messages_from_all_chats()
        self.history = {user: len(messages) for user, messages in messages.items()}

    def connect_to_chat(self):
        self.ws = create_connection(f'wss://localhost/ws?id=&sessionId={self.token}',
                                    sslopt={"cert_reqs": ssl.CERT_NONE})

    def login_as_admin(self):
        r = requests.post("https://localhost/api/auth", params={"username": "admin", "password": "admin"}, verify=False)
        self.token = r.json()['session']

    def get_users_(self):
        result = self.ws.recv()
        self.users = {x["user"]: x["userId"] for x in json.loads(result)["users"]}

    def get_messages_from_all_chats(self):
        all_messages = dict()
        for username, userid in self.users.items():
            if username == "admin":
                continue
            try:
                messages = self.get_messages_from_chat(userid)
                while messages is False:
                    messages = self.get_messages_from_chat(userid)
            except:
                self.connect_to_chat()
                return False
            if messages is not False:
                all_messages[username] = messages
        return all_messages

    def get_messages_from_chat(self, userid):

        request = '{"messagesIds":[],"receivedMessageIds":[],"onServerMessageIds":[],"roomIds":[1,' + str(userid) + \
                  '],"lastSynced":750221,"action":"syncHistory","cbId":1}'
        self.ws.send(request)
        data = self.ws.recv()
        result = json.loads(data)
        # format
        # {'userId': 3, 'content': 'hi', 'time': 1613247861718, 'id': 17, 'edited': 1613247861731, 'roomId': 3,
        #  'status': 'received', 'threadMessagesCount': 0, 'parentMessage': None, 'tags': {}}
        chat_messages = list()
        if not result.get("action"):

            for message in result['content']:
                if message.get('userId', -1) == int(userid):
                    chat_messages.append(message['content'])

            if not chat_messages:
                return [("No Messages", 0)]
            return chat_messages
        else:
            return False

    def send_message(self, userid, message):
        request = '{"files":[],"id":-1701069565,"timeDiff":1,"action":"printMessage","content":"' \
                  + message + '","tags":{},"parentMessage":null,"roomId":' + str(userid) + ',"cbId":10}'
        self.ws.send(request)
        self.ws.recv()

    def message_hook(self):
        def decorator(function):
            self.routes.append(function)

        return decorator

    def serve_new_messages(self, check_interval):
        data = self.get_messages_from_all_chats()
        if data is not False:
            for username, messages in data.items():
                if not self.history.get(username):
                    self.history[username] = len(messages)
                if self.history[username] < len(messages):
                    self.history[username] = len(messages)
                    for action in self.routes:
                        answer = action(messages[-1])
                        if answer is not None:
                            print(self.users[username], answer)
                            self.send_message(self.users[username], answer)
                            self.history[username] += 1

    def run(self, check_interval):
        while True:
            time.sleep(check_interval)
            self.serve_new_messages(check_interval)

    def close(self):
        self.ws.close()


# Bot init
bot = PyChatAdminBot()
bot.create()


# first example
@bot.message_hook()
def action(message):
    # parse link
    print("Users message", message)
    if message == "admin":
        return 'flag'


# second example for links
@bot.message_hook()
def check_link(link):
    # if you delete if, he can crach
    if link.startswith('http://'):
        try:
            r = requests.get(link)
            if "google.com" in r.text:
                return "flag{g00g13}"
        except:
            return "what is this??"
    # by default it returns none


bot.run(check_interval=2)  # interval in seconds
