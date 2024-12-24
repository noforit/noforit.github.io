import csv
import datetime
import os
from time import sleep
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("--overwrite", "-ow", action="store_true", help="Overwrite existing files")
args = parser.parse_args()

template = """---
{header}---
"""

def get_url_content(url):
	response = requests.get(url)
	if response.status_code == 200:
		return response.content
	return None

def get_meta_data(url):
	content = get_url_content(url)
	soup = BeautifulSoup(content, 'lxml')
	image_url = None
	desp = None
	if "ir.hit.edu.cn" in url:
		try:
			image_url = soup.find("div", {"class":"main_content single_main_content"}).find("img")['src']
		except TypeError:
			logging.error(f"No image url found from {url}")

	elif "mp.weixin.qq.com" in url:
		image_url = soup.find(property="og:image")['content']
		image_path = f"static/images/news/{title.replace('/', '_')}.jpg"
		if not os.path.exists(image_path):
			with open(image_path, "wb") as f:
				f.write(get_url_content(image_url))
		sleep(1)
		image_url = f"/images/news/{title.replace('/', '_')}.jpg"
		desp = soup.find(property="og:description")['content']
	else:
		logging.log(logging.WARNING, f"Unsupported site: {urlparse(url).netloc}")
		image_url = None
	return {
		"image_url": image_url,
		"desp": desp
	}


def read_csv(file_name):
	with open(file_name, 'r') as f:
		reader = csv.reader(f)
		next(reader)
		data = list(reader)
	return data

data = read_csv('utils/news/scir_news.csv')

def writer(title, link, date, article_type, desp, overwrite=False):
	file_path = f"content/news/{title.replace('/', '_')}.md"
	if os.path.exists(file_path) and not overwrite:
		logging.log(logging.WARNING, f"File {file_path} already exists, skipping...")
		return
	with open(file_path, "w") as f:
		date = datetime.datetime.strptime(date, '%Y/%m/%d').strftime('%Y-%m-%d')
		meta_data = get_meta_data(link)
		desp = meta_data["desp"] or desp
		if len(desp) > 120:
			desp = desp[:120] + "..."
		header = {
			"title": title,
			"date": date,
			"sort_by": "date",
			"description": desp,
			"extra": {
				"url": link
			},
		}
		if meta_data["image_url"]:
			header["extra"]["image"] = meta_data["image_url"]
		if article_type:
			header["taxonomies"] = { "news_type" : [article_type] }
		header = yaml.dump(header, allow_unicode=True)
		f.write(template.format(header=header))
	pass

for row in data:
	if isinstance(row, list) and len(row) == 5:
		title, link, date, desp_buffer, article_type = row
		writer(title, link, date, article_type, desp_buffer, args.overwrite)
	else:
		raise Exception("Invalid row: ", row)
