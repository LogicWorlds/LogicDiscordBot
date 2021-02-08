import discord, requests, json
from discord.ext import tasks, commands
import config as conf
from ProjectEverydayLogo import MakePerfect as mpi
		
class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)
		print('Uid:',self.user.id)
		
	def get_from(self, url):
		headers = {'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
		try:
			req = requests.get(url, headers=headers, timeout=15)
		except Timeout:
			return False
		else:
			return json.loads(req.text)
	
	async def on_message(self, message):
        # don't respond to ourselves
		if message.author == self.user:
			return

		message.content = message.content.lower()
		#print(message.content)
		if(message.content == '<@!'+str(self.user.id)+'>'):
			text = 'Что Вам необходимо?\n ' + \
			'**Доступные команды на данный момент:** \n' + \
			'`Cмени аву плз` - Смена аватара сервера на случайно сгенерированный\n' + \
			'`Бип` - Послать ботов\n' + \
			'`Шуткани` -  Случайная шутка\n' + \
			'`Факт` - Случайный факт\n' + \
			'`Топ голосующих` - Вывести топ голосующих на текущий момент\n' + \
			'`Статус серверов` - Узнать статус игровых серверов\n'
			await message.channel.send(text)
			
		if message.content == 'бип':
			await message.channel.send('Буп')
				
		if message.content == 'смени аву плз':
			if(message.guild == None):
				await message.channel.send('Данную команду можно использовать только на сервере!')
				return;
			await message.channel.send('Окей..')
			mpi.generateIcon()
			server = discord.Client.get_guild(self, id=message.guild.id)
			
			with open('ProjectEverydayLogo/out/out.png', 'rb') as f:
				icon = f.read()
			await server.edit(icon=icon)
			await message.channel.send('Нати.')
		if message.content == 'шуткани':
			req = self.get_from('https://randstuff.ru/joke/generate/')
			if(req == False):
				await message.channel.send('Ошибка соединения с API')
				return
			await message.channel.send(req['joke']['text'])
		if message.content == 'факт':
			req = self.get_from('https://randstuff.ru/fact/generate/')
			if(req == False):
				await message.channel.send('Ошибка соединения с API')
				return
			await message.channel.send(req['fact']['text'])
		if message.content == 'топ голосующих':
			positions = ['Первое место', 'Второе место', 'Третье место', 'Четвёртое место', 'Пятое место']
			spisok = self.get_from('https://logicworld.ru/launcher/tableTopVote.php?mode=api')
			if(spisok == False):
				await message.channel.send('Ошибка соединения с API')
				return
			text = "На текущий момент топ голосующих такой:\n"
			i = 0
			for userdata in spisok:
				static_text = " - **" + userdata['user'].title() + "** Счёт - **" + userdata['ammount'] + "** Доп. голоса - **" + userdata['cheatAmmount'] + "**\n"
				if i < len(positions):
					text += positions[i] + static_text
				else:
					text += str(i+1) + static_text
				i += 1
			await message.channel.send(text)
		if message.content == 'статус серверов':
			spisok = self.get_from('https://logicworld.ru/monAJAX/ajax.php')
			if(spisok == False):
				await message.channel.send('Ошибка соединения с API')
				return
			text = "Статус игровых серверов:\n"
			for s_name in spisok['servers']:
				s_data = spisok['servers'][s_name]
					
				if ( s_data['status'] == 'online' ):
					stat_e = ':green_circle:'
					if (s_data['ping'] > 300):
						stat_e = ':yellow_circle:'
					if (s_data['ping'] > 350):
						stat_e = ':orange_circle:'
					if (s_data['ping'] > 450):
						stat_e = ':brown_circle:'
					text += stat_e+"**"+ s_name +"** - ("+ str(s_data['online']) + "/" + str(s_data['slots']) + ") (" + str(s_data['ping']) + "ms)\n"
				else:
					text += ":red_circle:**"+s_name+"** - (**"+ s_data['status'] + "**)" + "\n"
			text += "\n**Общий онлайн:** " + str(spisok['online']) + "/" + str(spisok['slots']) + "\n"
			text += "**Рекорд дня:** " + str(spisok['recordday']) + " (" + spisok['timerecday'] + ")\n"
			text += "**Рекорд:** " + str(spisok['record']) + " (" + spisok['timerec'] + ")\n"
			await message.channel.send(text)

client = MyClient()
client.run(conf.bot_token)
