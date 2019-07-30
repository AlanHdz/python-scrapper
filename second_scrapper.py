from bs4 import BeautifulSoup
import requests
import threading

from pymongo import MongoClient

GOOGLE_NEWS_URL = 'https://news.google.com.mx/'
CUSTOM_TARGET = 'www.eluniversal.com'

def get_beautiful_soup(href):
	re = requests.get(href)
	if re.status_code == 200:
		return BeautifulSoup(re.text, 'html.parser')

def set_robot(article, database):
	title = article.find('a', { 'class': 'DY5T1d' }).getText()
	href = article.find('').get('href')
	json = {'title': title, 'link': href}
	database.articles.insert_one(json)
	print('Nuevo articulo en la base de datos')
	"""
	Obtener link del articulo
	href = article.find('').get('href')
	if CUSTOM_TARGET in href:
		soup = get_beautiful_soup(href)
		if soup is not None:
			container = soup.find('div', {'class': 'field field-name-body'})
			paragraphs = container.find_all('p')
			article = ''
			for paragraph in paragraphs:
				article = '{} {}'.format(article, paragraph)
	"""

def scraping_site():
	soup = get_beautiful_soup(GOOGLE_NEWS_URL)
	if soup is not None:
		client = MongoClient('localhost', 27017)
		database = client.scrapper
		articles = soup.find_all('h3', { 'class': 'ipQwMb' })
		for article in articles:
			robot = threading.Thread(name='set_robot', 
			target=set_robot, args=(article, database) )
			robot.start()
                

if __name__ == '__main__':
	scraping_site()
