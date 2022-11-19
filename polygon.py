
# тренировка по  питон видео
import vk
import requests
import json
import pprint #https://docs.python.org/3.10/library/pprint.html
import sys
import os
import vk_skech
import vkfriends
from colorama import init

# import colorama
path = 'serv'
servfile = 'vk_no_git.txt' # файл для хранения токенов и пиролей
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

demoColor =str( color.Red + '-Красный\n' + color.Green + '-Зелёный\n' + color.Yellow + '-Жёлтый\n' + color.Blue +'-Голубойэ\n' + color.Magenta + '-Cyan\n' + color.White + '-Коричневый\n' + color.BOLD +'-BOLD\n'  + color.ITALIC+ '-UNDERLINE\n' + color.END  + '-END\n')

menu = str(color.Green + ' [' + color.Yellow + 
'1' + color.Green + '] получение API по паролю и логину\n [' + color.Yellow + 
'2' + color.Green + '] блок получения токена по секретному коду\n ['+ color.Yellow + 
'3' + color.Green + '] чтение ID по API и красивый вывод\n [' + color.Yellow + 
'4' + color.Green + '] взять токен из файла\n [' + color.Yellow + 
'5' + color.Green + '] работа с  библиотекой vk\n [' + color.Yellow +
'6' + color.Green + '] работа с друзьями \n [' + color.Yellow + 
'7' + color.Green + '] запрос списка груп по сушествующему API\n [' + color.Yellow + 
'8' + color.Green + '] запрос списка друзей  по сушествующему API\n [' + color.Yellow + 
'9'+ color.Green +'] Поиск в диалоге по сообщению\n [' + color.Yellow +
'10'+ color.Green +'] Сохранение токена usera\n [' + color.Yellow+  '0' + color.Green + '] Выход' + color.END)




def test_request(id , token): #id = was_id, token = token)
	# проверка работы в принципе по токену
	print('token: ', token)
	resp = requests.get("http://api.vk.com/method/users.get", params = {"user_ids" : id, "access_token" : token, 'v': 5.131})
	
	print(resp, 'len(resp)', type(resp), resp.text)

	return  resp.json()


def Create_token_from_sekret(id, token, sekret):
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

def try_r(id,token ): #id = was_id,token = token
	#resp = requests.get("http://REDIRECT_URI#access_token=token&expires_in=86400&user_id=id&state=123456")

	print('token: ', token)
	try:
		resp = requests.get("http://api.vk.com/method/friends.get", params = {"user_ids" : id, "access_token" : token, 'v': 5.131})
	except:
		print("error requests")

	print(resp,  type(resp), resp.text)

	return  resp.json()

def VK_api(token, id):
	# работа с  библиотекой vk через токен токен пока слабый
	print('token: ', token,'\nid: ',id )
	api = vk.API(access_token = token,v='5.131')
	r = api.users.get(user_ids = id) 
	
	print('type(r):', type(r))

	'''  >>> api = vk.API(access_token='...', v='5.131')            |          >>> print(api.users.get(user_ids=1))                       |          [{'id': 1, 'first_name': 'Павел', 'last_name': 'Дуров', ... }] '''
	return r

#def vk_comunity(id, login , parol):
	# получение API по паролю и логину не работает!!! возможнотне указал параметр 
#        api = vk.CommunityAPI(
#    user_login='...',
#    user_password='...',
#    group_ids=[123456, 654321],
#    scope='messages',
#    v='5.131'
#)
'''
	api = vk.CommunityAPI(
		user_login=login,
		user_password=parol,
		group_ids=[11648449],
		scope='messages', # параметры доступа
		v='5.131')
	r = api.users.get(user_ids=id)

	return r
'''
def vk_userapi(id, login, parol):
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

def get_group_list(api, id):
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

def get_friend_list(api, id):
	# запрос списка друзей по сушествующему API
	'''принимает API , ID пользователя 
	   отдает:
		{'count': 625,
 		 'items': [126892066,54012242]}
	   ''' 
	r = api.friends.get(user_id=id, fields = 'nickname, contacts, has_mobile, status')

	pprint.pprint(r['items'][0:3])
	print('количество друзей',r['count'])

	return r

#Поиск в диалоге по сообщению
def search_by_word(api):
	''' вводим ID пользователя и фразу  
	работает 19.10.22
	вывод ток на печать  '''

	peer_Id = int(input(color.Yellow + 'ID пользователя >>> ' + color.Green))
	color.END
	query = str(input(color.Yellow + 'Фраза, по которой будем искать >>> ' + color.Green))
	color.END
	search = api.messages.search(q=query, peer_id=peer_Id)
	print(search)




def saveR(jsonR, namefile = 'requesVK.txt'):
	'''Сохранение отвера json в файл  
	 доработать на сервисный файл '''
	with open(namefile, 'w') as file:
		json.dump(jsonR, file, sort_keys = True, indent = 4)
	print('сохраненно в файл: ', namefile)
	return


def loadR(namefile = 'requesVK.txt'):
	with open(namefile, 'r') as file:
		r = json.load(file)
	return r

def workJson(jsonR , namefile = 'vk_no_git.txt'):
	'''Сохранение  json в файл  и проверка сделанна для первичного сохранения данных акаунтов и токенов 19.10.22 '''

	print('получился файл')
	pprint.pprint(jsonR)
	saveR(jsonR, namefile)
	
	print('сохраненно в файл: ', namefile)
	sekret = loadR(namefile)
	pprint.pprint(sekret)
	
	return sekret

def translateL_D(serv):
	files = os.listdir(serv)
	for file in files:
		if os.path.isfile(serv + '/' + file):
			if 'friends' in file and 'dict_' not in file:

				print(serv + '/'+file)

				data = loadR(str(serv + '/'+file))
				dictData = vk_skech.ist_to_dict(data['items'],'id')
				newFileName = serv + '/' +'dict_'+file
				
				print('Сохраняю', newFileName)
				saveR(dictData, newFileName)
	

	return
#--------------____________________________________________


def main(servfile = servfile, path = path):

	if not os.path.isdir(path): # поверка сервисной папки
		print(str(color.Red + 'Нет папки :'+ path + color.Cyan + 'создаю заново' + color.END))
		os.mkdir(path)

	# sekr = workJson() #первичное создание парольного файла
	print(demoColor)

	sekr = loadR(servfile)  # загрузка имен и токенов из серв файла 
	user_id = sekr['user'][0]['id']
	login = sekr['user'][0]['login']
	parol = sekr['user'][0]['parol']
	user_access_token =  sekr['user'][0]['access_token']
	token = sekr['token'][0]['access_token'] 
	sekret = sekr['token'][0]['sekret']
	id_app = sekr['token'][0]['id_app']
	first_name  = sekr['user'][0]['first_name']

	print(str(color.Cyan + 'Найденно:' + color.Green + str(len(sekr['user'])) + color.Yellow + ' пользователей\n         ' + color.Green +  str(len(sekr['token'])) + color.Yellow + ' токен Груп\n' ))

	targFriendID = user_id
	targNameStr = '?'
	infinite = 0
#------------------------------- тело цикла
	while infinite < 5:
		init()
		print(str(color.Cyan + 'Текуший пользователь:' + color.Green + str(user_id) +' '+ first_name))
		print('цель:',targFriendID, targNameStr)

		# проверка на наличие открытой сессии API
		try:
			if api:
				print(str(color.Green + '--- Найден api'))
		except NameError: print(str(color.Red +' Рабочего API нет' + color.END))


		print(menu)
		cmd = str(input('>>> '))

		if cmd == '0': break

		elif cmd == '1':
		# получение API по паролю и логину
			api  =  vk_userapi(user_id, login, parol) #id, login, parol

			r = api.users.get(user_ids= user_id)
			print('прочиталл:')
			pprint.pprint(r)

		elif cmd == '2':
		# блок получения токена по секретному коду
			r = Create_token_from_sekret(user_id, token, sekret)
			print('"Полученный ответ:\n"')

			pprint.pprint(r)
			saveR(r) # запись в файл

			print('----------------------------------------------------------------------')

		elif cmd == '3': 
		# чтение инфы по API и красивый вывод
			vk_skech.info_by_id(api) #проц из vk_skech.py
		# попытка что нибудь прочитать с токеном
#			r = try_r(user_id,token)  #id ,token 
#			print('token:',token)
#			print('"Полученный ответ\n"')
#			pprint.pprint(r)
			print('----------------------------------------------------------------------')
		elif cmd == '4': 
		# взять токен из файла
			sekr = loadR(servfile)
			print('прочиталл:')
			pprint.pprint(sekr)
			
			token = sekr['token'][0]['access_token'] 
			print('access_token:',token)

		elif cmd == '5': 
		# работа с полученным раньше токеном  VK.api
			print('token:',len(token),'==', token)
			print('user_access_token:',len(user_access_token), '==', user_access_token)
			r = VK_api(user_access_token, user_id)
			print('прочиталл:')
			pprint.pprint(r)
		
		elif cmd == '6':
		#  работа с друзьями меню выбора друзей
			#targFriendID, targNameStr = vkfriends.choise_friends_target(api)
			vkfriends.main(api, user_id = user_id, user_name = first_name, targFriend = targFriendID, targName = targNameStr)

			print('Ответ:',targFriendID, targNameStr)
		

		# преобразование LIST в  DICT 
			'''print('translateL_D(serv)')
			translateL_D(path)''' 
			print('----------------------------------------------------------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		# проверка работы в принципе
			'''
			r = test_request(user_id, token) #id = was_id, token = token)
			print('"Полученный ответ:\n"')
			pprint.pprint(r)'''
			print('----------------------------------------------------------------------')

		elif cmd == '7': 
		# запрос списка групп по открытому API
			try:
				if api: 
					print(' найден api')
					groupD = get_group_list(api,targFriendID)
			except NameError: print(' похоже вашего api нет')

			

		elif cmd == '8': 
		# запрос списка друзей  по открытому API
			try:
				if api: 
					print(' найден api >> работаю')
					friendsD = get_friend_list(api, targFriendID)
					print('Выход из get_friend_list')
					if 'y' in str(input('Сохранить список друзей y/n ? >> ')):
						print('test')
						newNameFile = str(path+'/'+ str(user_id) + '_friends.json')
						print(newNameFile)
						saveR(friendsD, newNameFile)
			except NameError:
				print(' похоже вашего api нет!!')
				foult = True 

		elif cmd == '9': 
		#Поиск в диалоге по сообщению
			#search_by_word(api)
			vkfriends.save_mesage_history(api)

		elif cmd == '10':
                #для питона возврат API
			sekr = loadR(servfile)  # загрузка имен и токенов из серв файл
			sekr['user'][0]['access_token']= api._api.access_token
			saveR(sekr, servfile)
			pprint.pprint(sekr)
			return api
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
