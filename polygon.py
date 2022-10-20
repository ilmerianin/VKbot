
# тренировка по  питон видео
import vk
import requests
import json
import pprint #https://docs.python.org/3.10/library/pprint.html
import sys
from colorama import init                                             

# import colorama

sekret ='9WyNPBBs2wdoTvCwPPjB'

token2 = '8fba30158fba30158f01f052d78fc27f7d88fba8fba3015ecf7eba072843e68952b65c6' # получен через секретный код приложения

token1 = 'a731730fa731730fa731730fc9a7493c67aa731a731730fc47cbedf7bd2e65c0eaade9c'

token ='4f5f55394f5f55394f5f5539044f271a5144f5f4f5f55392f90f04afb7fcb405ee2697e'

# https://m.vk.com/id22842277
# https://api.vk.com/method/users.get?user_id=210700286&v=5.131
was_id =  22842277 # вася
VKlogin = 'ilmerianin@mail.ru'
VKparol = 'igthvekm135'

id_kod = { 'user' : [{	'id': was_id,
			'login' : VKlogin,
			'parol' :VKparol }],
	'token' : [{'di_app' : 7884648,
		'access_token': token }]
	}
# старый способ получения токена https://oauth.vk.com/authorize?client_id=7884648&redirect_uri=https://oauth.vk.com/blank.html&scope=1325122&display=mobile&response_type=token #получение  токена возможно старый вариант

#scope= 2+64+2048+4096+8192+262144+1048576 #коды разрешений  доступов
#print(scope)лг



init(autoreset=True) # сброс цветного указателя                                                                                                                                                                   
class color:
	Red = '\033[91m'
	Green = '\033[1;32m'
	Yellow = '\033[93m'
	Blue = '\033[94m'
	Magenta = '\033[95m'
	Cyan = '\033[96m'
	White = '\033[97m'
	Grey = '\033[90m'
	BOLD = '\033[1m'
	ITALIC = '\033[3m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

menu = str(color.Green + ' [' + color.Yellow + '1' + color.Green + '] проверка работы в принципе\n [' + color.Yellow + '2' + color.Green + '] блок получения токена по секретному коду\n ['+ color.Yellow + '3' + color.Green + '] попытка что нибудь прочитать с токеном\n [' + color.Yellow + '4' + color.Green + '] взять токен из файла\n [' + color.Yellow + '5' + color.Green + '] работа с  библиотекой vk\n [' + color.Yellow + '6' + color.Green + '] получение API по паролю и логину \n [' + color.Yellow + '7' + color.Green + '] запрос списка груп по сушествующему API\n [' + color.Yellow + '8' + color.Green + '] запрос списка друзей  по сушествующему API\n [' + color.Yellow + '9'+ color.Green +' ] Поиск в диалоге по сообщению\n [' + color.Yellow +  '0' + color.Green + '] Выход' + color.END)




def test_request(id = was_id, token = token):
	# проверка работы в принципе по токену
	print('token: ', token)
	resp = requests.get("http://api.vk.com/method/users.get", params = {"user_ids" : id, "access_token" : token, 'v': 5.131})
	
	print(resp, 'len(resp)', type(resp), resp.text)

	return  resp.json()


def Create_token_from_sekret(id = was_id,token = token):
	''' получение токена через секретный код '''
	print('sekret: ', sekret)
	try:
		
		resp = requests.get("https://oauth.vk.com/access_token", params = {"client_id" : 7884648, "client_secret" : sekret, 'v': 5.131 , 'grant_type' :'client_credentials'})
# client_id  ид приложения
# client_secret секретный код приложения
# https://oauth.vk.com/access_token?client_id= + CLIENT_ID + &client_secret= + CLIENT_SECRET + &v=5.131&grant_type=client_credentials

	except:
		print("error requests")

	print(resp,  type(resp), resp.text)

	return  resp.json()

def try_r(id = was_id,token = token):
	#resp = requests.get("http://REDIRECT_URI#access_token=token&expires_in=86400&user_id=id&state=123456")

	print('token: ', token)
	try:
		resp = requests.get("http://api.vk.com/method/friends.get", params = {"user_ids" : id, "access_token" : token, 'v': 5.131})
	except:
		print("error requests")

	print(resp,  type(resp), resp.text)

	return  resp.json()

def VK_api(token = token, id = was_id):
	# работа с  библиотекой vk через токен токен пока слабый
	print('token: ', token,'\nid: ',id )
	api = vk.API(access_token = token,v='5.131')
	r = api.users.get(user_ids = id) 
	
	print('type(r):', type(r))

	'''  >>> api = vk.API(access_token='...', v='5.131')            |          >>> print(api.users.get(user_ids=1))                       |          [{'id': 1, 'first_name': 'Павел', 'last_name': 'Дуров', ... }] '''
	return r

def vk_comunity(id= was_id, login = VKlogin, parol= VKparol):
	# получение API по паролю и логину не работает
	api = vk.CommunityAPI(
		user_login=login,
		user_password=parol,
		group_ids=[11648449],
		scope='messages', # параметры доступа
		v='5.131')
	r = api.users.get(user_ids=id)

	return r

def vk_userapi(id= was_id, login = VKlogin, parol= VKparol):
	# получение API по паролю и логину 
	# работает 16.10.22
	'''id= was_id, login = VKlogin, parol= VKparol
	   отдает api  '''
	api = vk.UserAPI(
		user_login=login,
		user_password=parol,
		scope='offline,wall,messages', # параметры доступа
		v='5.131')
	# r = api.users.get(user_ids=id)

	return  api

def get_group_list(api, id = was_id):
	# запрос списка груп по сушествующему API
	'''принимает API , ID пользователя 
	   отдает:
		{'count': 625,
 		 'items': [126892066,54012242]}
	  работает 19.10.22 ''' 
	r = api.groups.get(user_id=id, # Идентификатор пользователя, информацию о сообществах которого требуется получить
			extended ='1', # подробное описание груп (0)
			filter = 'admin') #, editor, moder, advertiser, groups, publics, events, hasAddress') #По умолчанию возвращаются все сообщества пользователя
			# fields =' ', #activity,can_create_topic,can_post,can_see_all_posts,city,contacts,counters,country,description,finish_date,fixed_post,links,members_count,place,site,start_date,status,verified, wiki_page.  # Список дополнительных полей, которые необходимо вернуть.  только при extended = 1
			# offset = '0' #Смещение, необходимое для выборки определённого подмножества сообществ
			#count = '3'   # количество груп в списке
		
	print('количество груп', r['count'])

	# pprint.pprint(r)
	return r

def get_friend_list(api, id = was_id):
	# запрос списка груп по сушествующему API
	'''принимает API , ID пользователя 
	   отдает:
		{'count': 625,
 		 'items': [126892066,54012242]}
	   ''' 
	r = api.friends.get(user_id=id)
	pprint.pprint(r)
	print('количество друзей',r['count'])

	return r

#Поиск в диалоге по сообщению
def search_by_word(api):
	peer_Id = int(input(color.Yellow + 'ID пользователя >>> ' + color.Green))
	color.END
	query = str(input(color.Yellow + 'Фраза, по которой будем искать >>> ' + color.Green))
	color.END
	search = api.messages.search(q=query, peer_id=peer_Id)
	print(search)




def saveR(jsonR, namefile = 'requesVK.txt'):
	'''Сохранение отвера json в файл  '''
	with open(namefile, 'w') as file:
		json.dump(jsonR, file, sort_keys = True, indent = 4)
	print('сохраненно в файл: ', namefile)
	return


def loadR(namefile = 'requesVK.txt'):
	with open(namefile, 'r') as file:
		r = json.load(file)
	return r

def workJson(jsonR = id_kod, namefile = 'vk_no_git.txt'):
	'''Сохранение  json в файл  '''
	print('получился файл')
	pprint.pprint(jsonR)
	saveR(jsonR, namefile)
	
	print('сохраненно в файл: ', namefile)
	sekret = loadR(namefile)
	pprint.pprint(sekret)	
	
	return sekret


def main(token = token, id = was_id):
	#print('token:',token)
	sekr = workJson()
	infinite = 0
	while infinite < 5:
		init()
		print(menu)
    		#color.Yellow
		cmd = str(input('>>> '))
    		#color.END
		if cmd == '0': break

		elif cmd == '1':  
		# проверка работы в принципе
			r = test_request()
			print('"Полученный ответ:\n"')
			pprint.pprint(r)
			print('----------------------------------------------------------------------')

		elif cmd == '2':
		# блок получения токена по секретному коду
			r = Create_token_from_sekret(was_id,token)
			print('"Полученный ответ:\n"')

			pprint.pprint(r)
			saveR(r) # запись в файл

			print('----------------------------------------------------------------------')

		elif cmd == '3': 
		# попытка что нибудь прочитать с токеном
			r = try_r(was_id,token)
			print('token:',token)
			print('"Полученный ответ\n"')
			pprint.pprint(r)
			print('----------------------------------------------------------------------')
		elif cmd == '4': 
		# взять токен из файла
			r = loadR()
			print('прочиталл:')
			pprint.pprint(r)
			print('''r['access_token']: ''',r['access_token'])
			token = r['access_token']
 
		elif cmd == '5': 
		# попытка получить токеи с  VK.api
			#print('token:', token)
			r = VK_api(token)
			print('прочиталл:')
			pprint.pprint(r)
		
		elif cmd == '6':
		# получение API по паролю и логину
			api  =  vk_userapi()

			r = api.users.get(user_ids=id)
			print('прочиталл:')
			pprint.pprint(r)

		elif cmd == '7':
		# запрос списка групп по открытому API
			try:
				if api: 
					print(' найден api')
					groupD = get_group_list(api)
			except: print(' похоже вашего api нет')

			

		elif cmd == '8': 
		# запрос списка друзей  по открытому API
			try:
				if api: 
					print(' найден api')
					friendsD = get_friend_list(api)
			except: print(' похоже вашего api нет')

		elif cmd == '9': 
		#Поиск в диалоге по сообщению
			search_by_word(api)

#    elif cmd == '':
#        clear()
#        continue
#    else: print(color.Green + 'Некорректный ввод!' + color.END)

#    print(color.Green + 'Вы хотите продолжить? [0, N, no, нет] Нет [1,
# Y, yes, да] Да\n' + color.END)
#    color.Yellow
#    y = input('>>> ')                                                     color.END                                                             if y == "0" or y == 'no' or y == 'N' or y == 'нет':
#        clear()
#        break                                                             if y == "1" or y == 'yes' or y == 'Y' or y == 'да':                       clear()

		



	
	
	
#   4f5f55394f5f55394f5f5539044f271a5144f5f4f5f55392f90f04afb7fcb405ee2697e

if __name__ =='__main__':
	main()
