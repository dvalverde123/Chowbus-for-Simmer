import ast, json, string, operator, re, os, time, pickle, requests
import argparse as ap
import pandas as pd
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from urllib.request import urlopen
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from menu_from_db import extract_json, save_locally
from save_sentences_csv import items_in_sentence, optimize_list, read_items
from menu_from_db import extract_json
import time


#Open browser in incognito

def run_chowbusimagescraper(chowbus_id, foodie_id):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(options=chrome_options)

	wiki = "https://www.chowbus.com" + chowbus_id
	driver.get(wiki)
 
#Logistics
	script_dir = os.path.abspath(os.path.join(__file__ , "../.."))
	path = script_dir + "/csvfiles/images/" + foodie_id + "-images-chowbus/"
	exceptions = ['a', 'an', 'of', 'the', 'is', 'with', 'or', 'and', 'to', 'from'] + foodie_id.split('-')
	print(path)


# menu_items = read_items(script_dir, foodie_id)
	json = extract_json(foodie_id)
	if(json['Items'] == []):
		return 'Could not pull images from database. Potential FoodieID mismatch.'
	menu_items = save_locally(json, foodie_id)

	foodie_ids = []
	source_ids = []
	items = []
	filenames = []
	matches = []
	n = 0


	elements = driver.find_elements_by_xpath("//*[@id='7489']")
	print(elements)
	print("Elements length", len(elements))
	for element in elements:
		print("more food")
		item_name = element.find_elements_by_class_name("//*[@id='7489']").get_attribute(getText())

		matched_items = items_in_sentence(item_name, menu_items, 2, foodie_id, exceptions)
		if(len(matched_items) == 0):
			continue

		imgs = element.find_elements_by_class_name("//*img[@class=jss327jss329]")
		for img in imgs:
			img_src = img.get_attribute("src")
			print(img_src)
			print("more food food")
			
		
			optimized_items = optimize_list(matched_items, item_name.lower())
			print("the length of list is: ", len(optimized_items))
			for item in optimized_items:
				if n == 0:
					try: os.makedirs(path)
					except OSError: pass
	
			filename = foodie_id + "-" + str(n) + ".jpg"
			urlretrieve(img_src, path + filename)
			print(filename)

			foodie_ids.append(foodie_id)
			items.append(item)
			filenames.append(filename)
			print("even more food")
			matches.append(item_name)
			n += 1 
			print(n)

	driver.close()
	if n > 0:
		d = {'FoodieID' : foodie_ids, 'Item' : items, 'Filename' : filenames, 'Matches' : matches}
		df = pd.DataFrame(d)
		df.to_excel(path + foodie_id + ".xlsx", sheet_name='Sheet1', encoding="utf8", index=False)
	return 'Added Chowbus Imgs'
	print(path)
	print("eat")

def pull_content(chowbus_id):
	wiki = "https://www.chowbus.com/" + chowbus_id
	r.requests.get(wiki)
	encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
	soup = BeautifulSoup(r.content, from_encoding=encoding)
	print(soup)
	print("amazing")
	
	   # print(soup)

	# foodie_ids = []
	# items = []
	# filenames = []
	# matches = []

	# exceptions = ['a', 'an', 'of', 'the', 'is', 'with', 'or', 'and', 'to', 'from'] + foodie_id.split('-')
	# json = extract_json(foodie_id)
	# menu_items = save_locally(json, foodie_id)
	# script_dir = os.path.abspath(os.path.join(__file__ ,"../.."))
	# path = script_dir + "/csvfiles/images/" + foodie_id[:100] + "-images-chowbus/"
	# try: os.makedirs(path)
	# except OSError: pass

	# for container in soup.find_all("div", attrs={"data-react-class" : "OfferTilesContainer"}):
	# 	# print(ast.literal_eval(str(container.get('data-react-props'))))

	# 	for dish in container.get('data-react-props'):
	# 		image_name = dish['name']
	# 		image_url = dish['imageSet'][0]['hidpi']

	# 		matched_items = items_in_sentence(image_name, menu_items, 2, foodie_id, exceptions)
	# 		if(len(matched_items) == 0):
	# 			continue

	# 		optimized_items = optimize_list(matched_items, image_name.lower())
	# 		for item in optimized_items:
	# 			filename = foodie_id + "-" + str(n) + ".jpg"
	# 			urlretrieve(link, path + filename)

	# 			foodie_ids.append(foodie_id)
	# 			items.append(item)
	# 			filenames.append(filename)
	# 			matches.append(image_name)
	# 			n += 1

	# 	d = {'FoodieID' : foomanchi-new-york-221die_ids, 'Item' : items, 'Filename' : filenames, 'Matches' : matches}
	# 	df = pd.DataFrame(d)
	# 	df.to_excel(path + foodie_id[:100] + ".xlsx", sheet_name='Sheet1', encoding="utf8", index=False)

	# return n 


	
if __name__ == '__main__':
	parser = ap.ArgumentParser()
	parser.add_argument('-f', '--foodie_id', help="FoodieID", default="sizzling-pot-king-chicago-761")
	parser.add_argument('-c', '--chowbus_id', help="ChowbusID", default="pickup/Sizzling%20pot%20king%20chicago%20/227/")

	args = vars(parser.parse_args())
	foodie_id = args['foodie_id']
	chowbus_id = args['chowbus_id']
	run_chowbusimagescraper(chowbus_id, foodie_id)
