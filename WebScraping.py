from flask import Flask, jsonify, request, json
import requests
from bs4 import BeautifulSoup


#def TimesOfIndia():
    #url = "https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States"
url = "https://timesofindia.indiatimes.com/"
page = requests.get(url)


print(page.status_code) 

soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

tb = soup.find('div', class_='top-story')

#print(tb)

print("Top News Story: Times Of India ")
for link in tb.find_all('li'):
    name = link.find('a')
    print("NEWS: "+name.get_text('title'))
    #return jsonify({"NewsResult": name})
    


#https://www.codementor.io/@dankhan/web-scrapping-using-python-and-beautifulsoup-o3hxadit4