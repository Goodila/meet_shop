import json
from dataclasses import dataclass


@dataclass
class Config:
    token: str
    admins: list
    bot_id: int



def get_config(flag=None):
    if flag:
        config = json.load(open("config.txt", "r",encoding='utf-8'))
        return config['TOPICS']
    else:
        config = json.load(open("config.txt", "r", encoding='utf-8'))
        return Config(token=config['TOKEN'], admins=config['ADMIN_ID'], bot_id=config['BOT_ID'])



    
class Client:
    def __init__(self, id: str):
        self.id = str(id)
    
    def check(self):
        with open('clients.json', 'r+', encoding='utf-8') as f:
            clients = json.load(f)
            return self.id in clients.keys()

    def record(self, value):
        with open('clients.json', 'r', encoding='utf-8') as f:
            clients = json.load(f)
            clients[self.id] = value
        with open('clients.json', 'w', encoding='utf-8') as f:
            json.dump(clients, f, indent=4)
    
    
    def record_stuff(self, key, value):
        with open('clients.json', 'r', encoding='utf-8') as f:
            clients = json.load(f)
            clients[self.id][key] = value
        with open('clients.json', 'w', encoding='utf-8') as f:
            json.dump(clients, f, indent=4)


    def get(self):
        with open('clients.json', 'r', encoding='utf-8') as f:
            blogers = json.load(f)
            return blogers[self.id]
        

    def get_stuff(self, key):
        with open('clients.json', 'r', encoding='utf-8') as f:
            blogers = json.load(f)
            return blogers[self.id][key]
        





        
# async def events_fomer(events_data: list):
#     '''формирует список мероприятий в текст'''
#     res = ''
#     for event in events_data:
#         text = f'''{event[0]}. {event[1]}
# Тема: {event[2]}
# Место: {event[3]}
# Время: {event[4]}
# Дата: {event[5]}
# Программа: {event[6]}

# '''     
#         res += text
#     res += 'Чтобы начать регистрацию на мероприятие, нажмите на него здесь 👇'
#     return res 