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
        

class Client:
    def __init__(self, id):
        self.id = id

    
    def check(self):
        with open("clients.json", "r+") as read_file:
            clients = json.load(read_file)
            print(clients, self.id, self.id in clients)
            if not str(self.id) in clients:  
                clients[self.id] = []
                self.record(clients)


    def record(self, data):
        with open("clients.json", "w") as read_file:
            json.dump(data, read_file, indent=4)

    
    @staticmethod
    def record_product(data, id):
        with open("clients.json", "r") as read_file:
            clients = json.load(read_file)
            try:
                clients[id].append(data)
            except:
                pass
        with open("clients.json", "w") as read_file:
            json.dump(clients, read_file, indent=4)
        

    @staticmethod
    def get_order(id):
        with open("clients.json", "r") as read_file:
            clients = json.load(read_file)
            order = clients[str(id)]
        return "\n".join(order)


    @staticmethod
    def del_product(data, id, in_order=False):
        if in_order == 'clear':
            with open("clients.json", "r") as read_file:
                clients = json.load(read_file)
                try:
                    clients[id] = []
                except IndexError:
                    return "Произошла ошибка ("
            with open("clients.json", "w") as read_file:
                json.dump(clients, read_file, indent=4)
        if in_order:
            with open("clients.json", "r") as read_file:
                clients = json.load(read_file)
                try:
                    s = clients[str(id)].remove(data)
                    text =  f"{data} удален"
                except IndexError:
                    return "Произошла ошибка ("
            with open("clients.json", "w") as read_file:
                json.dump(clients, read_file, indent=4)
                return text
            return f"продукт {s} успешно удален из заказа"
        else:
            with open("clients.json", "r") as read_file:
                clients = json.load(read_file)
                data = int(data[1:])
                try:
                    s = clients[str(id)].pop(data-1)
                except IndexError:
                    return "Произошла ошибка, возможно Вы ввели неверный номер продукта"
            with open("clients.json", "w") as read_file:
                json.dump(clients, read_file, indent=4)
            return f"продукт {s} успешно удален из заказа"


