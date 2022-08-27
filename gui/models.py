""" import required modules """
import concurrent.futures
import json
import os
import re
import shutil

import requests
from bs4 import BeautifulSoup


class GetHomePageAnime():

	""" GetHomePageAnime class """

	def __init__(self):
		self.BaseUrl = "https://myself-bbs.com/"
		self.Url = 'https://myself-bbs.com/portal.php'
		self.Header = { "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)\
						 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36" }
		self.FileStorage = os.path.join(os.getcwd(), "src/animes/")

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

			if not os.path.exists(self.FileStorage):
				os.mkdir(self.FileStorage)

			with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
				executor.map(self.download_images, block_set)

			anime_block = {"area_name": block_name, "block_content": block_set}
			area_set.append(anime_block)

		return area_set


if __name__ == "__main__":
	app = GetHomePageAnime()
	f = open(os.path.join(os.getcwd(), "animes.json"), "w")
	json.dump(app.start_crawler(), f, indent=4)
	f.close()
