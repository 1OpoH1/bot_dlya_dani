import vk_api.vk_api
from random import shuffle
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api import VkUpload
from os import getcwd, listdir
from os.path import isfile, join

my_path = getcwd() + '\\NSFW'
all_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]


class Server:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id, wait=20)
        self.vk_api = self.vk.get_api()
        self.upload = VkUpload(self.vk)
        self.users = {}
        self.tags = ['Ero-memes', 'Fire Force', 'Hotel Transylvania', 'Genshin Impact', 'KonoSuba', 'Overwatch',
                     'Demon Slayer', 'Evangelion', 'Nagatoro', 'Furry', 'Hero Academia', 'Helltaker', 'Incredibles',
                     'Love is War', 'Mimes', "Foster's home", 'Gravity Falls', 'Meru the Succubus', 'Adventure Time',
                     'Lola Bunny', 'Teen Titans', 'Samsung', 'Chainsaw man', 'NieR: Automata', 'Kill la Kill',
                     'Re:Zero', 'Uzaki-chan', 'Hatsune miku', 'Teenage Robot', 'Naruto', 'Gawr Gura', 'TenSura',
                     'Doki Doki', 'Kim Posiible', 'Avatar', 'Star vs Evil', 'Shield Hero', 'Samurai Jack', 'Gwen Stacy',
                     'Total drama', "Steven's Universe", 'Ben 10', 'Rick and Morty', 'Dragon Maid',
                     'Darling in the Franxx', 'Sword Art Online', 'Bioshock Infinite', 'Pokemon', 'Other']

    def start(self):
        print('Началось')
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.message["from_id"] not in self.users:
                    self.users[event.object.message["from_id"]] = User()
                if 'Влево' in event.object.message["text"] or 'Вправо' in event.object.message["text"]:
                    self.users[event.object.message["from_id"]].num_keyboard(event.object.message["text"])
                if '16+' in event.object.message["text"]:
                    self.users[event.object.message["from_id"]].x = False
                    self.send_message(event.object.message["peer_id"],
                                      "Вы решили посмотреть эротические арты, доступные арты представлены в клавиатуре",
                                      "first_keyboard.json")
                if '18+' in event.object.message["text"]:
                    self.users[event.object.message["from_id"]].x = True
                    self.send_message(event.object.message["peer_id"],
                                      "Вы решили посмотреть хентай арты, доступные арты представлены в клавиатуре",
                                      "first_keyboard.json")
                if 'Начать' in event.object.message["text"]:
                    self.send_message(event.object.message["peer_id"],
                                      "Данный бот выводит картинки эротического содержания, выберите возраст получаемых картинок",
                                      "start_keyboard.json")
                if event.object.message["text"] in self.tags:
                    self.send_message(event.object.message["peer_id"], '', keyboard="keyboard.json",
                                      attachment=self.send_picture(self.users[event.object.message["from_id"]].find_picture(
                                          event.object.message["text"])))

    def send_message(self, peer_id, message, keyboard="first_keyboard.json", attachment=None):
        self.vk_api.messages.send(peer_id=peer_id,
                                  message=message,
                                  random_id=0,
                                  keyboard=open(keyboard).read(),
                                  attachment=attachment)

    def send_picture(self, pictures):
        photos = self.upload.photo_messages(pictures)
        attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photos)
        return attachment


class User():
    def __init__(self):
        self.number_of_keyboard, self.number_of_keyboard_x = 0, 0
        self.files = all_files
        self.files_not_x = list(filter(lambda x: x[0] != 'x', self.files))
        self.files = list(filter(lambda x: x.startswith('x'), self.files))
        shuffle(self.files)
        shuffle(self.files_not_x)
        self.x = False
        self.all_tags = {'Fire Force': 'ff',
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
                         'Other': 'ot'}

    def num_keyboard(self, message):
        if self.x:
            if message.lower() == 'влево':
                self.number_of_keyboard = (self.number_of_keyboard + 1) % 4
            else:
                self.number_of_keyboard = (self.number_of_keyboard - 1) % 4
            return self.number_of_keyboard
        else:
            if message.lower() == 'влево':
                self.number_of_keyboard_x = (self.number_of_keyboard_x + 1) % 4
            else:
                self.number_of_keyboard_x = (self.number_of_keyboard_x - 1) % 4
            return self.number_of_keyboard_x

    def search_name(self, name: str):
        if self.x:
            file = self.files
        else:
            file = self.files_not_x
        for i in file:
            if name in i:
                yield i

    def find_picture(self, tags):
        tag = self.all_tags[tags]
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

    def find_comics(self, name):
        file_name = name.split('@')
        if len(file_name) == 1:
            return 0
        reserve_list = list(filter(lambda x: file_name[0] in x and file_name[1][1:] in x, all_files))
        reserve_list.sort()
        for i in reserve_list:
            self.files.pop(self.files.index(i))
        return reserve_list
