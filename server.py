import vk_api.vk_api
from random import shuffle
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api import VkUpload
from os import getcwd, listdir
from os.path import isfile, join

my_path = getcwd() + '' #TODO Даня, измени путь файла
all_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]


class Server:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id, wait=20)
        self.vk_api = self.vk.get_api()
        self.upload = VkUpload(self.vk)
        self.users = {}
        self.titles = [
            'Ero-memes', 'Fire Force', 'Hotel Transylvania', 'Genshin Impact',
            'KonoSuba', 'Overwatch', 'Demon Slayer', 'Evangelion', 'Nagatoro',
            'Furry', 'Hero Academia', 'Helltaker', 'Incredibles',
            'Love is War', 'Mimes', "Foster's home", 'Gravity Falls',
            'Meru the Succubus', 'Adventure Time', 'Lola Bunny', 'Teen Titans',
            'Samsung', 'Chainsaw man', 'NieR: Automata', 'Kill la Kill',
            'Re:Zero', 'Uzaki-chan', 'Hatsune miku', 'Teenage Robot', 'Naruto',
            'Gawr Gura', 'TenSura', 'Doki Doki', 'Kim Possible', 'Avatar',
            'Star vs Evil', 'Shield Hero', 'Samurai Jack', 'Gwen Stacy',
            'Total drama', "Steven's Universe", 'Ben 10', 'Rick and Morty',
            'Dragon Maid', 'Darling in the Franxx', 'Sword Art Online',
            'Bioshock Infinite', 'Pokemon', 'Other', 'Loli', 'Milfs', '3D',
            'Creampie', 'Cumshot', 'Posing', 'Lesbo', 'Hetero', 'Masturbation',
            'Bondages'
        ]

    def start(self):
        print('Началось')
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message["from_id"] not in self.users:
                    self.users[event.object.message["from_id"]] = User()
                if '16+' in event.object.message["text"]:
                    self.users[event.object.message["from_id"]].x = False
                    self.send_message(
                        event.object.message["peer_id"],
                        "Вы решили посмотреть эротические арты, доступные арты представлены в клавиатуре",
                        "1keyboard.json")
                if '18+' in event.object.message["text"]:
                    self.users[event.object.message["from_id"]].x = True
                    self.send_message(
                        event.object.message["peer_id"],
                        "Вы решили посмотреть хентай арты, доступные арты представлены в клавиатуре",
                        "1keyboard.json")
                if 'Начать' in event.object.message["text"]:
                    self.send_message(
                        event.object.message["peer_id"],
                        "Данный бот выводит картинки эротического содержания, выберите возраст получаемых картинок",
                        "start_keyboard.json")
                if 'Влево' in event.object.message["text"] or 'Вправо' in event.object.message["text"]:
                  self.users[event.object.message["from_id"]].num_keyboard(event.object.message["text"])
                  if not self.users[event.object.message["from_id"]].x:
                        self.send_message(event.object.message["peer_id"], self.users[event.object.message["from_id"]].number_of_keyboard, f'{self.users[event.object.message["from_id"]].number_of_keyboard}keyboard.json')
                  else:
                        self.send_message(event.object.message["peer_id"], self.users[event.object.message["from_id"]].number_of_keyboard_x, f'{self.users[event.object.message["from_id"].number_of_keyboard_x]}keyboard.json')
                if event.object.message["text"] in self.titles:
                  picture = self.send_picture(self.users[event.object.message["from_id"]].find_picture(event.object.message["text"]))
                  if picture:
                      self.send_message(
                      event.object.message["peer_id"],
                      '\t',
                      attachment=picture)
                  else:
                    self.users[event.object.message["from_id"]].shuffle_files()
                    self.send_message(event.object.message["peer_id"], 'Картинки кончились, но мы их сейчас перемешаем...', keyboard=f"{self.users[event.object.message['from_id']].number_of_keyboard}keyboard.json")

    def send_message(self,
                     peer_id,
                     message,
                     keyboard="1keyboard.json",
                     attachment=None):
        self.vk_api.messages.send(peer_id=peer_id,
                                  message=message,
                                  random_id=0,
                                  keyboard=open(keyboard).read(),
                                  attachment=attachment)

    def send_picture(self, pictures):
        if 'картинок' in pictures:
            return None
        photos = self.upload.photo_messages(pictures)
        attachment = ','.join('photo{owner_id}_{id}'.format(**item)
                              for item in photos)
        return attachment


class User():
    def __init__(self):
        self.number_of_keyboard, self.number_of_keyboard_x = 0, 0
        self.reserve_files = all_files
        self.files_not_x = list(filter(lambda x: x[0] != 'x', self.reserve_files))
        shuffle(self.files_not_x)
        self.files = list(filter(lambda x: x.startswith('x'), self.reserve_files))
        shuffle(self.files)
        self.x = False
        self.all_titles = {
            'Fire Force': 'ff',
            'Gawr Gura': 'gg',
            'Hotel Transylvania': 'htr',
            'Genshin Impact': 'gi',
            'KonoSuba': 'ko',
            'Overwatch': 'ov',
            'Demon Slayer': 'ds',
            'Evangelion': 'ev',
            'Nagatoro': 'na',
            'Furry': 'fu',
            'Hero Academia': 'ha',
            'Helltaker': 'ht',
            'Incredibles': 'in',
            'Love is War': 'lw',
            'Mimes': 'mi',
            "Foster's Home": 'fh',
            'Gravity Falls': 'gf',
            'Meru the Succubus': 'ms',
            'Adventure Time': 'at',
            'Lola Bunny': 'lb',
            'Ben 10': 'be',
            'Teen Titans': 'tt',
            'Samsung': 'sa',
            'Dragon Maid': 'dm',
            'Chainsaw Man': 'cm',
            'Бесконечное лето': 'bl',
            'Kill la Kill': 'kk',
            'NieR: Automata': 'NA',
            'Re:Zero': 'rz',
            'Uzaki-chan': 'uz',
            'Naruto': 'Na',
            'TenSura': 'te',
            'Other': 'ot',
            'Loli': '1',
            'Milfs': '2',
            '3D': '3',
            'Creampie': '4',
            'Cumshot': '5',
            'Posing': '6',
            'Lesbo': '7',
            'Hetero': '8',
            'Masturbation': '9',
            'Bondages': '#'
        }

    def num_keyboard(self, message):
        if not self.x:
            if message.lower() == 'влево':
                self.number_of_keyboard = 1 +(self.number_of_keyboard + 1) % 3
            else:
                self.number_of_keyboard = 1 +(self.number_of_keyboard) % 3
            return self.number_of_keyboard
        else:
            if message.lower() == 'влево':
                self.number_of_keyboard_x = 1 +(self.number_of_keyboard_x + 1) % 3
            else:
                self.number_of_keyboard_x = 1 +(self.number_of_keyboard_x) % 3
            return self.number_of_keyboard_x

    def search_name(self, name: str):
        if self.x:
            file = self.files
        else:
            file = self.files_not_x
        for i in file:
            if name in i.split('(')[0]:
                yield i

    def find_picture(self, titles):
        tag = self.all_titles[titles]
        files = list(self.search_name(tag))
        try:
            if '@' in files[0]:
                return self.find_comics(files[0])
            if self.x:
                self.files.pop(self.files.index(files[0]))
            else:
                self.files_not_x.pop(self.files_not_x.index(files[0]))
            return files[0]
        except IndexError:
          return "Нет картинок по такому запросу"
        except ValueError:
          return "Такой картинки нет"
   
    def shuffle_files(self):
      if self.x:
            self.files = list(filter(lambda x: x.startswith('x'), self.reserve_files))
            shuffle(self.files)
      else:
            self.files_not_x = list(filter(lambda x: x[0] != 'x', self.reserve_files))
            shuffle(self.files_not_x)

    def find_comics(self, name):
        file_name = name.split('@')
        if len(file_name) == 1:
            return 0
        reserve_list = list(
            filter(lambda x: file_name[0] in x and file_name[1][1:] in x,
                   all_files))
        reserve_list.sort()
        for i in reserve_list:
            self.files.pop(self.files.index(i))
        return reserve_list
