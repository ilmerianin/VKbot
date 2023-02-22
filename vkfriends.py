# vkfriends
import vk
import requests
import json
import pprint 
import sys
import os
import vk_skech
from colorama import init
import pprint
import time
import vkclasses

# import colorama
path = 'serv' # есть в polygon
servfile = 'vk_no_git.txt' # файл для хранения токенов и пиролей# есть в polygon


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

menu = str(color.Green + ' [' + color.Yellow + 
'1' + color.Green + '] -------------------\n [' + color.Yellow + 
'2' + color.Green + '] меню выбора друзей цели\n ['+ color.Yellow + 
'3' + color.Green + '] чтение инфы цели по API  красивый вывод\n [' + color.Yellow + 
'4' + color.Green + '] получение нового токена сушествующего API \n [' + color.Yellow + 
'5' + color.Green + '] -- получение списка групп цели\n [' + color.Yellow +
'6' + color.Green + '] --Найти обшие группы \n [' + color.Yellow + 
'7' + color.Green + '] Скачивание истории сообщений с целевым другом--Найти фотграфии цели\n [' + color.Yellow + 
'8' + color.Green + '] получение списка публикаций на стене группы--Найти общих друзей\n [' + color.Yellow + 
'9'+ color.Green +'] Поиск в диалоге по сообщению\n [' + color.Yellow +  '0' + color.Green + '] Выход' + color.END)




def take_post_wal(api,**kwargs):
	'''посылка поста на стену
	 strpost dict  '''
	print('take_post_wal  kwargs:',kwargs)
	#print('take_post_wal  args:',args)
	r =api.wall.post(**kwargs)
	print('Ответ api.wall.post:', r)
	return r

def get_post_wal(api, targGroup = '77419940',targGroupName= 'def:тексты и книги',count='2'):
	'''Получение последних сообщений со стены группы 
	api - открытая сессия API
	teragGroup str( целевая группа)
	targGroupName : str(название для отображения в запросе не учавствунт)
	count :str(количество сообщений define = 2 

	return dict'''

	if targGroup == 0: # ручной ввод номера группы 
		print('Не заданна цель!!')
		targGroup = str(input('введите  id цели => '))

	print('Получение постов из групы: ', targGroup, targGroupName)
	dataPosts = api.wall.get(
		owner_id = '-'+str(targGroup), # номер группы -ном ли ном человека
		# offset = 0 # смешение первого сообщения
		count=count  #количество сообшений
		)




	pprint.pprint(dataPosts)

	return dataPosts

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

def get_group_list(api, id):
	# запрос списка групп по сушествующему API
	'''принимает API , ID пользователя 
	   отдает:
		{'count': 625,
 		 'items': [126892066,54012242]}
	   ''' 
	r = api.groups.get(user_id=id, extended='1',fields='name,activity, description')

	pprint.pprint(r['items'][0:3])
	print('количество групп: ',r['count'])

	return r

	# загрузка списков друзей и выдоц целей
def choise_friends_target(api = 0, id = '22842277' , path = 'serv'):
	''' выбор цели (человек)
	принивмет открытый API , id -цели загружает или скачивает список друзей и сохраняет
	реализует выбор целевого друга
	возврашает: 
		targetID  : str id
		 targ_str : str (first_name + last_name)'''
	
	print( str(color.Green +'целевой человек id:'+ color.Yellow + str(id) +color.Green + '\n[' + color.Yellow + '1' + color.Green + '] Загрузить список друзей из VK'))

	# отработка наличия сохраненных файлов
	x = [True for x in os.listdir(path) if id in x]
	if len(x) > 0 :
		print( str(color.Green + '[' + color.Yellow + 
'2' + color.Green + '] Взять список друзей из сохр базы'))

	chois = str(input('>>'))

	if chois == '1' :
	# запрос списка друзей  по открытому API
		try:
			if api:   # проверка на наличие открытого API
				print(' найден api >> работаю')
				friendsD = get_friend_list(api, id) # получение списка   друзей
				print('Выход из get_friend_list')

				dictData = vk_skech.ist_to_dict(friendsD['items'],'id')

				if 'y' in str(input('Сохранить список друзей y/n ? >> ')):

# выбрать вариант сохранения  ответа или сделать оба а один пока задокументировать
# в дальнейшем сделать сравнение и добавление данных 
					newNameFile = str(path+'/'+ id + '_friends.txt')
					print('Сохраняю',newNameFile)
					saveR(friendsD, newNameFile) # сохранение варианта с LIST

				# преобразование LIST в  DICT 
					 # print('Обработка DICT')
					#translateL_D(path) # созрание доп файла в формате DICT

					
					newNameFile = str(path+'/'+'dict_' + id + '_friends.txt')

					print('Сохраняю', newNameFile)
					saveR(dictData, newNameFile)

				
		except NameError:
			print(' похоже вашего api нет!!')
			foult = True
		except vk.exceptions.VkAPIError:
				print('VkAPIError') 
				given_nev_token(api)
				#print('out  api._api.accsess_token:', api._api.access_token)
				return  id, 'сбой API повторите запрос'

	elif chois == '2': 
	# загрузка базы
		if x[0] == True: #  если файлы с базой есть
			dictData = loadR(path+'/dict_' +id +'_friends.txt')
	else: 
		print('выбор не понятен')
		return False
	
# выбор цели
	#return dictData
	targetID, targ_str = choisTargetFriends(dictData) #выбор цели распечатк
	print('end!! return',targetID, targ_str)

	return targetID, targ_str


def  choisTargetFriends(data:dict):
	# выбор цели распечатка с частичной инфой и выбор по номеру	возврат ID b name
	print('  choisTarget')
	listKey = list(data.keys())
	print('listKey[0:3]:',listKey[0:3])
	
	for i in range(len(listKey)):
		
		print('№ ', i,' id::', listKey[i],'  ', data[listKey[i]]['first_name'], ' ',  data[listKey[i]]['last_name'])
		if i % 50 == 0: # должно быть количество строк вывода на экране
			yn = str(input('дальше ? n-break(далее ввод выбранного номера) '))
			if 'n' in yn: break
	chois = int(input('введите номер >>'))
	print("ввод", chois)
	
	return  listKey[chois], str( data[listKey[chois]]['first_name'] +' ' +  data[listKey[chois]]['last_name'])


	# выбор цели распечатка с частичной инфой и выбор по номеру	возврат ID b name 
def  choisTarget(data:dict, item1, item2):
	''' универсальный вариант выбора с передачей ключей item1 первый ключь распечатки  item2 - второй ключ'''

	print('  choisTarget')
	listKey = list(data.keys())
	print('listKey[0:1]:',listKey[0:3])
	
	for i in range(len(listKey)):
		
		print('№ ', i,' id::', listKey[i],'  ', data[listKey[i]][item1], ' ',  data[listKey[i]][item2])
		if i % 50 == 0: # должно быть количество строк вывода на экране
			yn = str(input('дальше ? n-break(далее ввод выбранного номера) '))
			if 'n' in yn: break
	chois = int(input('введите номер >>'))
	print("ввод", chois)
	
	return  listKey[chois], str(data[listKey[chois]][item1]) + data[listKey[chois]][item2]


# загрузка списков групп и выдоц целей
def choise_group_target(api = 0, id = '22842277' , path = 'serv'):
	''' выбор цели (группа)
	принивмет открытый API , id -цели загружает или скачивает список групп и сохраняет
	реализует выбор целевой группы
	возврашает: 
		targetID  : str id группы
		targ_str : str (group_name)'''

	namefile = str(id) + '_dict_groups.txt' #часть имени файла
	print( str(color.Green +'целевой человек id:'+ color.Yellow + str(id) +color.Green + '\n[' + color.Yellow + '1' + color.Green + '] Загрузить список групп из VK'))

	# отработка наличия сохраненных файлов
	x = [True for x in os.listdir(path) if namefile in x]
	if len(x) > 0 :
		print( str(color.Green + '[' + color.Yellow + 
'2' + color.Green + '] Взять список груп человека из сохр базы'))

	chois = str(input('>>'))

	if chois == '1' :
	# запрос списка group friend  по открытому API
		try:
			if api !=0:   # проверка на наличие открытого API
				print(' найден api >> работаю')
				groups = get_group_list(api, id) # получение списка  групп

				print('Выход из get_group_list')

				dictData = vk_skech.ist_to_dict(groups['items'],'id') 

				if 'y' in str(input('Сохранить список груп y/n ? >> ')):

# выбрать вариант сохранения  ответа или сделать оба а один пока задокументировать
# в дальнейшем сделать сравнение и добавление данных 
				#	newNameFile = str(path+'/'+ id + '_group.txt')
				#	print('Сохраняю',newNameFile)
				#	saveR(friendsD, newNameFile) # сохранение варианта с LIST

				# преобразование LIST в  DICT 
					 # print('Обработка DICT')
					#translateL_D(path) # созрание доп файла в формате DICT

					newNameFile = str(path+'/'+ namefile)

					print('Сохраняю', newNameFile)
					saveR(dictData, newNameFile)


			else:
				print(' похоже вашего api нет!!')
				foult = True
		except vk.exceptions.VkAPIError:
				print('VkAPIError') 
				given_nev_token(api)
				#print('out  api._api.accsess_token:', api._api.access_token)
				return  id, 'сбой API повторите запрос'

	elif chois == '2': 
	# загрузка базы
		if x[0] == True: #  если файлы с базой есть
			dictData = loadR(path+'/'+ namefile)
	else: 
		print('выбор не понятен')
		return False
	
# выбор цели
	#return dictData
	targetID, targ_str = choisTarget(dictData, 'is_admin','name') #выбор цели распечатк
	print('end!! return',targetID, targ_str)

	return targetID, targ_str


#Поиск в диалоге по сообщению
def search_by_word(api, peer_id = 0):
	''' вводим ID пользователя и фразу  
	работает 19.10.22> изменение 04.11.22 
	вывод ток на печать  '''

	if peer_id == 0:
		peer_id = int(input(color.Yellow + 'ID пользователя >>> ' + color.Green))
	color.END

	query = str(input(color.Yellow + 'Фраза, по которой будем искать >>> ' + color.Green))
	color.END

	search = api.messages.search(q=query, peer_id=peer_id)
	print(search)

	return


def save_mesage_history(api, targID= '1666174', offset = 0, count = 199, timesl = 1):
	''' Сохраняет скачивает истроию сообщений  '''
	list_message = []
	while offset < 1000:
		list_message.append(api.messages.getHistory(peer_id = targID, offset = offset, count = count))
		print('count): ', list_message[0]['count'])
		offset += count
		time.sleep(0.3)

	#pprint.pprint(list_message)
	saveR(list_message, 'serv/mesages.txt')
	return

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
	''' транслирует всю папку
	список из словарей в словарь по ключам  id создавая повый файл с приставкой dict_ , пока заточен только на друзей 
	serv путь к сервисной папке относительный '''
	files = os.listdir(serv)
	for file in files:
		if os.path.isfile(serv + '/' + file):
			if 'friends' in file and 'dict_' not in file:

				#print(serv + '/'+file)
				data = loadR(str(serv + '/'+file))
				dictData = vk_skech.ist_to_dict(data['items'],'id')

				newFileName = serv + '/' +'dict_'+file
				print('Сохраняю', newFileName)

				saveR(dictData, newFileName)
			if 'groups' in file and 'dict_' not in file:

				#print(serv + '/'+file)
				data = loadR(str(serv + '/'+file))
				dictData = vk_skech.ist_to_dict(data['items'],'id')

				newFileName = serv + '/' +'dict_'+file
				print('Сохраняю', newFileName)

				saveR(dictData, newFileName)
	

	return

def given_nev_token(api):
	''' получение нового токена для существующей сессти API'''

	print('old api._api.accsess_token:', api._api.access_token)
	api._api.access_token = api._api.get_access_token()
#	print('new token:',access_token)
	print('api._api.accsess_token:', api._api.access_token)

	return 

def main(api =0, user_id = 0, user_name = 0, targFriend = 0,targName = 0,targGroup ='77419940',targGroupName ='Тексты и книги',  servfile = servfile, path = path):

	infinite = 0
#------------------------------- тело цикла
	while infinite < 5:
		init()
		print(str(color.Cyan + 'Текуший пользователь:' + color.Green + str(user_id) +' '+ user_name))
		print(str(color.Cyan + 'Текушая цель:' + color.Green + str(targFriend) +' '+ targName))

		# проверка на наличие открытой сессии API
		if api != 0:
			print(str(color.Green + '--- Найден api'))
		else: print(str(color.Red +' Рабочего API нет' + color.END))


		print(menu)
		cmd = str(input('>>> '))

		if cmd == '0': break

		elif cmd == '1':
		# 
			pass
		elif cmd == '2':
		# блок проверки работы выбора друзей
			targFriend, targName = choise_friends_target(api = api, id = str(targFriend)) 
			print('Возврат в main friends:',targFriend, targName)
			print('----------------------------------------------------------------------')

		elif cmd == '3': 
		# чтение инфы о целиЧеловек по API из VK и красивый вывод
			try:
				vk_skech.info_by_id(api, targFriend) #проц из vk_skech.py
			except vk.exceptions.VkAPIError:
				print('VkAPIError - получите новый токен')
			print('----------------------------------------------------------------------')
		elif cmd == '4': 
		# получение нового токена сушествующего API
			given_nev_token(api)
			
		elif cmd == '5': 
		# получение списка групп цели 
			targGroup, targGroupName = choise_group_target(api = api, id = targFriend)

		elif cmd == '6':
		# 
			print('-----------')
		

		elif cmd == '7': 
		# Скачивание истории сообщений с целевым другом
			save_mesage_history(api, targFriend)

		elif cmd == '8': 
		# получение списка публикаций на стене группы
			list_posts = get_post_wal(api, targGroup,targGroupName)
			post_class = vkclasses.postGetting(list_posts['items'][0]) #разборка принятого поста в класс

			print('вывод строки для отправуи сообщения на стену: \n', post_class.sendpost())
			if 'y' in str(input('постить на стену? y/да >>')):
				#owner_id, from_group, message =	take_post_wal
				p = post_class.sendpost()
				print('-----------p',p)
				take_post_wal(api,**p )

			#================================================================================================
		elif cmd == '9': 
		#Поиск в диалоге по сообщению
			search_by_word(api, targFriend)

	return targFriend, targName

if __name__ =='__main__':
	main()
 
