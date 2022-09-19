import concurrent.futures
import json
import os
import re
import shutil

import requests
from bs4 import BeautifulSoup


class GetHomePageAnime():

	def __init__(self):
		self.BaseUrl = "https://myself-bbs.com/"
		self.Url = 'https://myself-bbs.com/portal.php'
		self.Header = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
						 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36" }
		self.FileStorage = os.path.join(os.getcwd(), "src/animes/")

		if not os.path.exists(self.FileStorage):
			os.mkdir(self.FileStorage)

	def download_images(self, info):
		image_data = info['image']
		filename = os.path.join(self.FileStorage, image_data.split("/")[-1])
		if not os.path.exists(filename):
			response = requests.get(headers=self.Header, url=self.BaseUrl+image_data, stream=True)
			if response.status_code == 200:
				with open(filename, 'wb') as f:
					response.raw.decode_content = True
					shutil.copyfileobj(response.raw, f)

	def start_crawler(self):
		try:
			response = requests.get(headers=self.Header, url=self.Url)
		except requests.exceptions.ConnectionError:
			print("ConnectionError")
			exit(1)

		soup = BeautifulSoup(response.text, 'lxml')

		Anime_area = soup.find('div', {"id": "diy1"}, {"class": "area"})
		Anime_blocks = Anime_area.find_all('div', {"class": "blocktitle title", "style": True})
		Anime_blocks_contents = Anime_area.find_all('div', {"class": "module cl ml"})

		anime = []

		for segment in Anime_blocks_contents:
			result = segment.find_all('li')
			if result != []:
				anime.append(result)

		anime[3].extend(anime[4])
		anime.pop(4)

		Anime_blocks.insert(3, Anime_blocks[2])

		area_set = []

		for num, segment in enumerate(Anime_blocks):
			if num == 3:
				block_name = segment.string + "-續"
			else:
				block_name = segment.string

			block_set = []

			for item in anime[num]:
				page_link = item.find('a').attrs['href']
				image_data = item.find('img', {"src": re.compile(r'.*[".jpg"|".jpeg"]')}).attrs['src'][2:]
				anime_title = item.find('p').text.strip()
				anime_info = {"title": anime_title, "image": image_data, "link": page_link}
				block_set.append(anime_info)

			with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
				executor.map(self.download_images, block_set)

			anime_block = {"area_name": block_name, "block_content": block_set}
			area_set.append(anime_block)

		return area_set


class GetEveryWeekAnime():

	def __init__(self):
		self.BaseUrl = "https://myself-bbs.com/"
		self.Url = 'https://myself-bbs.com/portal.php'
		self.Header = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
						 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36" }

	def start_crawler(self):
		try:
			response = requests.get(headers=self.Header, url=self.Url)
		except requests.exceptions.ConnectionError:
			print("ConnectionError")
			exit(1)

		area_set = {}

		soup = BeautifulSoup(response.text, 'lxml')

		Anime_title = ["portal_block_955_content", "portal_block_956_content", "portal_block_957_content", "portal_block_958_content", "portal_block_959_content", "portal_block_960_content", "portal_block_961_content"]

		for week, id in enumerate(Anime_title):

			Anime_area = soup.find("div", {"id": id}, {"class": "dxb_bc"})
			Anime_blocks_contents = Anime_area.find_all('div', {"class": "module cl xl xl1"})

			for segment in Anime_blocks_contents:
				result = segment.find_all('li')
				if result != []:
					area_set[week+1] = result

		for num, segment in enumerate(area_set.values()):

			one_week_anime = []

			for item in segment:

				page_link = item.find('a').attrs['href']
				anime_title = item.find('a').attrs['title']
				anime_text = item.find('span').text.strip()
				anime_info = {"title": anime_title, "text": anime_text, "link": page_link}
				
				one_week_anime.append(anime_info)
			
			area_set[num+1] = one_week_anime

		return area_set


class GetSeriesAnime():

	def __init__(self, url='https://myself-bbs.com/forum-133-1.html'):
		self.BaseUrl = "https://myself-bbs.com/"
		self.Url = url
		self.Header = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
						 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36" }
		self.FileStorage = os.path.join(os.getcwd(), "src/animes/")

		if not os.path.exists(self.FileStorage):
			os.mkdir(self.FileStorage)

	def download_images(self, info):
		image_data = info['image']
		filename = os.path.join(self.FileStorage, image_data.split("/")[-1])
		if not os.path.exists(filename):
			response = requests.get(headers=self.Header, url=self.BaseUrl+image_data, stream=True)
			if response.status_code == 200:
				with open(filename, 'wb') as f:
					response.raw.decode_content = True
					shutil.copyfileobj(response.raw, f)

	def start_crawler(self):
		try:
			response = requests.get(headers=self.Header, url=self.Url)
		except requests.exceptions.ConnectionError:
			print("ConnectionError")
			exit(1)

		soup = BeautifulSoup(response.text, 'lxml')

		Anime_area = soup.find('div', {"id": "threadlist"})
		Anime_list = Anime_area.find_all('li')

		num_of_page = soup.find('div', {"class": "pg"}).find_all('a')[-2].text
		current_page = soup.find('div', {"class": "pg"}).find_all('strong')[0].text

		if "... " in num_of_page:
			num_of_page = num_of_page.split("... ")[1]

		# print("Page: {}/{}".format(current_page, num_of_page))

		if int(num_of_page) < int(current_page):
			num_of_page = current_page

		area_set = []

		for segment in Anime_list:
			page_link = segment.find('a').attrs['href']
			image_data = segment.find('img', {"src": re.compile(r'.*[".jpg"|".jpeg"]')}).attrs['src'][2:]
			anime_title = segment.find('a').attrs['title']
			anime_info = {"title": anime_title, "image": image_data, "link": page_link}
			area_set.append(anime_info)

		with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
			executor.map(self.download_images, area_set)

		return {"page": int(current_page), "total_page": int(num_of_page), "content": area_set}


class GetFinishAnimeList():

	def __init__(self):
		self.BaseUrl = "https://myself-bbs.com/"
		self.Url = "https://myself-bbs.com/portal.php?mod=topic&topicid=8"
		self.Header = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
						 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36" }
		self.FileStorage = os.path.join(os.getcwd(), "src/animes/")

		if not os.path.exists(self.FileStorage):
			os.mkdir(self.FileStorage)

	def start_crawler(self):
		try:
			response = requests.get(headers=self.Header, url=self.Url)
		except requests.exceptions.ConnectionError:
			print("ConnectionError")
			exit(1)

		soup = BeautifulSoup(response.text, 'lxml')

		Anime_area = soup.find('div', {"id": "diypage", "class": "area"})
		Anime_list = Anime_area.find_all('div', {"id": re.compile(r'tab.*'), "class": "frame-tab"})

		anime_set = {}

		for item in Anime_list:

			block_id = item.get('id')
			animes = item.find('div', {"id": block_id+"_title"})
			title = animes.find_all('div', {"class": "block"})
			
			for title_item in title:
				tab_name = title_item.find('div', {"class": "blocktitle"}).text.strip()
				tab_id = title_item.get('id')
				tab_content = title_item.find('div', {"id": tab_id+"_content"})
				tab_content_list = tab_content.find_all('a')
				anime_set[tab_name] = []
				for tab_content_item in tab_content_list:
					anime_set[tab_name].append({"title": tab_content_item.attrs['title'], "link": tab_content_item.attrs['href']})

		return anime_set


class GetR18HomePageAnime():

	def __init__(self):
		self.BaseUrl = "https://myself-bbs.com/"
		self.Url = 'https://myself-bbs.com/portal.php?mod=topic&topicid=3'
		self.Header = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
						 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36" }
		self.FileStorage = os.path.join(os.getcwd(), "src/animes/")

		if not os.path.exists(self.FileStorage):
			os.mkdir(self.FileStorage)

	def download_images(self, info):
		image_data = info['image']
		filename = os.path.join(self.FileStorage, image_data.split("/")[-1])
		if not os.path.exists(filename):
			response = requests.get(headers=self.Header, url=self.BaseUrl+image_data, stream=True)
			if response.status_code == 200:
				with open(filename, 'wb') as f:
					response.raw.decode_content = True
					shutil.copyfileobj(response.raw, f)

	def start_crawler(self):
		try:
			response = requests.get(headers=self.Header, url=self.Url)
		except requests.exceptions.ConnectionError:
			print("ConnectionError")
			exit(1)

		soup = BeautifulSoup(response.text, 'lxml')

		r18_anime_set = {}
		r18_area = ['frame4561NC', 'frameM646Dg', 'frame1sh3TV']

		for block_id in r18_area:
			anime_area = soup.find('div', {"id": block_id})
			area_names = [ item.text.strip() for item in anime_area.find_all('div', {"class": "title"}) ]
			if block_id == 'frame1sh3TV':
				area_names.insert(0, "編輯精選")
				area_names.insert(0, "編輯精選")
			animes = anime_area.find_all('div', {"class": "block"})
			for item in animes:
				area_id = item.get('id')
				area_content = item.find('div', {"id": area_id+"_content"})
				area_content_list = area_content.find_all('li')

				if area_content_list == []:
					continue

				key = area_names[animes.index(item)]
				if r18_anime_set.get(key) == None:
					r18_anime_set[key] = []

				for area_content_item in area_content_list:
					page_link = area_content_item.find('a').attrs['href']
					image_data = area_content_item.find('img', {"src": re.compile(r'.*[".jpg"|".jpeg"]')}).attrs['src'][2:]
					anime_title = area_content_item.find('p').text.strip()
					anime_info = {"title": anime_title, "image": image_data, "link": page_link}
					r18_anime_set[key].append(anime_info)

				with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
					executor.map(self.download_images, r18_anime_set[key])

		return r18_anime_set


if __name__ == "__main__":
	# app = GetHomePageAnime()
	# f = open(os.path.join(os.getcwd(), "home.json"), "w")
	# json.dump(app.start_crawler(), f, indent=4)
	# f.close()

	# app = GetEveryWeekAnime()
	# f = open(os.path.join(os.getcwd(), "week.json"), "w")
	# json.dump(app.start_crawler(), f, indent=4)
	# f.close()

	# app = GetSeriesAnime()
	# f = open(os.path.join(os.getcwd(), "continue.json"), "w")
	# json.dump(app.start_crawler(), f, indent=4)
	# f.close()

	# app = GetFinishAnimeList()
	# f = open(os.path.join(os.getcwd(), "finish.json"), "w")
	# json.dump(app.start_crawler(), f, indent=4)
	# f.close()

	app = GetR18HomePageAnime()
	f = open(os.path.join(os.getcwd(), "r18.json"), "w")
	json.dump(app.start_crawler(), f, indent=4)
	f.close()
	
	pass
