from server import Server, User
from config import vk_api_token
from os import getcwd, listdir
from os.path import isfile, join

my_path = getcwd() + '\\Test_directory'
my_path = getcwd()
all_files = [my_path+'\\'+f for f in listdir(my_path) if isfile(join(my_path, f))]

server1 = Server(vk_api_token, 196086399, "Hukommelse")
server1.start()
