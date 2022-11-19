# определение классов

class postGetting(object):
	'''Класс разбора сообщния стены'''
	count = 0 # счетчик экземпляров класса

	def __init__(self, postDict:dict):
		self.owner_id = postDict['owner_id']	#
		self.from_id = postDict['from_id']	#
		self.date = postDict['date']	#
		self.id = postDict['id']		#
		self.text = postDict['text']         #
		self.post_type = postDict['post_type'] #
		self.hash = postDict['hash']	# хеш сообщения
		self.copy_history = postDict['copy_history'] # не понивает нужен разбор на запчасти
		self.attachments = postDict['copy_history'][0]
		self.listKeys = list(postDict.keys())
		self.listAttachment = list(self.attachments['attachments'][0].keys())

		print('listKeys :', self.listKeys)
		print('attachment keys: ', self.listAttachment)


	def sendpost(self, owner_id = '-105251634' ,  from_group = '1'):

		strPost ={'owner_id' : owner_id, 'from_group': from_group, 'message': self.text, 'copy_history': self.copy_history}
		
		return strPost #owner_id, from_group, self.text
	def attachrevirv(self, attach):
		strattach = attach['ovner_id'] + '_' + attach['id']  +'_' + attach['access_token']

class postCreateBox:

	METHOD_COMMON_PARAMS = {'v', 'lang', 'https', 'test_mode'}

	def __new__(cls, *args, **kwargs):
		# язь 12.11ю22
		print(' APIBase __new___ kwargs:', type(kwargs), kwargs)
		method_common_params = {
			key: kwargs.pop(key) # выбор из kwargs нужного по ключу	
			for key in tuple(kwargs) if key in cls.METHOD_COMMON_PARAM
			}

		print('postCreateBox method_common_params :',type(method_common_pa

        api = object.__new__(cls)
        api.__init__(*args, **kwargs) # вызов APIBase __init__

        return APINamespace(api, method_common_params)
