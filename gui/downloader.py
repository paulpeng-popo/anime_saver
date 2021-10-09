import os
import re
import ast
import lxml
import m3u8
import shutil
import requests
import threading
from time import sleep
from bs4 import BeautifulSoup
from collections import deque

class Worker(threading.Thread):

	def __init__(self, queue, anime_name):
		threading.Thread.__init__(self)
		self.workers = []
		self.numofthreads = 15
		self.queue = queue
		self.anime_name = anime_name
		self.CurrentDir = os.getcwd()
		self.Header = {
			"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
		}

	def get_link_info(self):
		weight = 0
		link = self.queue.pop()
		video_name = link.split('/')[-1]
		resources = ast.literal_eval(requests.get(link).text)
		basename = resources['video']['720p']
		m3u8_path = "https://vpx.myself-bbs.com/"

		return video_name, m3u8_path + basename

	def download_ts(self, segment_dir, url):
		while len(self.ts_queue) > 0:
			segment_filename = self.ts_queue[-1]

			try: video_stream = requests.get(headers=self.Header, url=url+segment_filename, stream=True)
			except Exception as error:
				print("Some error occurs")
				sleep(5)
				continue

			if video_stream.status_code == 200:
				with open(os.path.join(segment_dir, segment_filename), "wb") as file:
					video_stream.raw.decode_content = True
					shutil.copyfileobj(video_stream.raw, file)
				file.close()
				try: remove = self.ts_queue.pop()
				except IndexError as error: break

	def createNewDownloadThread(self, segment_dir, url):
		download_thread = threading.Thread(target=self.download_ts, args=(segment_dir, url))
		self.workers.append(download_thread)
		download_thread.start()

	def file_walker(self, path):
		file_list = []
		for root, dirs, files in os.walk(path):
			for fn in files:
				p = str(root + '\\' + fn)
				if fn != "check_list.txt":
					file_list.append(p)
		file_list.sort(key=lambda x: int(x[-6:-3]))
		return file_list

	def combine(self, ts_path):
		file_list = self.file_walker(ts_path)
		file_path = ts_path + ".mp4"
		with open(file_path, 'wb+') as fw:
			for i in range(len(file_list)):
				fw.write(open(file_list[i], 'rb').read())
		fw.close()

	def check_completeness(self, segment_dir, url):
		with open(os.path.join(segment_dir, "check_list.txt"), "r") as f:
			files = f.readlines()
			for file in files:
				file = file.replace('\n', '')
				print("check file:", segment_dir, file)
				while not os.path.isfile(os.path.join(segment_dir, file)):
					print(segment_dir, file, "file miss")
					print(url+file)
					try: video_stream = requests.get(headers=self.Header, url=url+file, stream=True)
					except Exception as error:
						print("Some error occurs")
						sleep(5)
						continue

					if video_stream.status_code == 200:
						with open(os.path.join(segment_dir, file), "wb") as ifile:
							video_stream.raw.decode_content = True
							shutil.copyfileobj(video_stream.raw, ifile)
						ifile.close()
						print(segment_dir, file, "file download successfully")
		f.close()

	def run(self):
		while len(self.queue) > 0:
			video_name, playlist_url = self.get_link_info()
			playlist = m3u8.load(playlist_url, verify_ssl=False)
			url = playlist_url[:playlist_url.rfind('/')+1]

			ts_list = []
			for line in playlist.dumps().split('\n'):
				if line.endswith(".ts"):
					ts_list.append(line)

			segment_dir = os.path.join(self.anime_name, video_name)
			os.mkdir(segment_dir)

			with open(os.path.join(segment_dir, "check_list.txt"), "w") as f:
				for item in ts_list:
					f.write(item+'\n')
			f.close()

			self.ts_queue = deque(ts_list)
			for number in range(self.numofthreads):
				self.createNewDownloadThread(segment_dir, url)

			for worker in self.workers:
				worker.join()

			self.check_completeness(segment_dir, url)
			self.combine(segment_dir)
			shutil.rmtree(segment_dir)

def video_download(Url, NumOfWorker):
	CurrentDir = os.getcwd()
	Header = {
		"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"
	}

	response = requests.get(headers=Header, url=Url)
	soup = BeautifulSoup(response.text, 'lxml')
	title_tag = soup.find('meta', {"name": "keywords"})
	video_name = title_tag['content']
	anime_name = os.path.join(CurrentDir, video_name)

	if os.path.isdir(anime_name):
		print("You had already downloaded the set of anime.")
	else:
		os.mkdir(anime_name)
		a_links = soup.find_all('a', {"data-href": re.compile(r'http.*')})
		links = [ link["data-href"].replace('player/play', 'vpx').replace("\r", "").replace("\n", "") for link in a_links ]
		waiting_queue = deque(links)
		print("Fetch links successfully.")

		workers = []
		for number in range(NumOfWorker):
			workers.append(Worker(waiting_queue, anime_name))

		for worker in workers:
			worker.start()

		for worker in workers:
			worker.join()

		print("Done")

if __name__ == '__main__':
	target = ''
	video_download(target, 12)
