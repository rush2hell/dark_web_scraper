#!/usr/bin/env python
from bs4 import *
import requests
import csv
import socks
import socket
import datetime
import time
from elasticsearch import Elasticsearch
import cv2 
import glob 
import requests
import urllib.request
import numpy as np
from PIL import Image
import imagehash
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse


def create_elk(images):
	check = es.indices.exists(index="images")
	print(check)
	if check == "True":
		download_images(images,pwd)
	else:
		print("Index Exist with that name!")
		create_elk()

	# image downloading start
	download_images(images)


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images):
	#creating hash dictionary
	hash_doc = {"caption":[], "link":[], "hash":[], "timestamp": str(datetime.datetime.now())};
	_id = 1
	
	# intitial count is zero
	count = 0

	# print total images found in URL
	print(f"Total {len(images)} Image Found!")

	# checking if images is not zero
	if len(images) != 0:
		for i, image in enumerate(images):
			# From image tag ,Fetch image Source URL

						# 1.data-srcset
						# 2.data-src
						# 3.data-fallback-src
						# 4.src

			# Here we will use exception handling

			# first we will search for "data-srcset" in img tag
			try:
				# In image tag ,searching for "data-srcset"
				image_link = image["data-srcset"]
				
			# then we will search for "data-src" in img
			# tag and so on..
			except:
				try:
					# In image tag ,searching for "data-src"
					image_link = image["data-src"]
				except:
					try:
						# In image tag ,searching for "data-fallback-src"
						image_link = image["data-fallback-src"]
					except:
						try:
							# In image tag ,searching for "src"
							image_link = url + image["src"]
							print(image_link)

							hash_doc["link"].append(image_link)
							#creating hash for image 
							image_data = Image.open(requests.get(image_link, stream=True).raw)
							dhash = imagehash.dhash(image_data)
							hash_value = str(dhash)
							hash_doc["hash"].append(hash_value)
							print(hash)

						# if no Source URL found
						except:
							pass

			# After getting Image Source URL
			# We will try to get the content of image
			try:
				r = requests.get(image_link).content
				try:

					# possibility of decode
					r = str(r, 'utf-8')

				except UnicodeDecodeError:

					# After checking above condition, Image Download start
					a = urlparse(url)
					image_name = os.path.basename(a.path)
					print(image_name) 
					hash_doc["caption"].append(image_name)
					# counting number of image downloaded
					count += 1
			except:
				pass

		# There might be possible, that all
		# images not download
		# if all images download
		if count == len(images):
			print("Done")
		# if all images not download
		else:
			print(f"Total {count} Images Downloaded Out of {len(images)}")

# MAIN FUNCTION START
def main(url):
	
	# content of URL
	r = requests.get(url)

	# Parse HTML Code
	soup = BeautifulSoup(r.text, 'html.parser')

	# find all images in URL
	images = soup.findAll('img')

	# Call folder create function
	create_elk(images)


# Configuring Socks to use Tor
from urllib.request import urlopen
socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
socket.socket = socks.socksocket

# It is necessary to use Tor for DNS resolution of Onion websites
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo

# create a client instance of Elasticsearch
es = Elasticsearch([{'host': '84.247.12.226', 'port': 9200}])

print("---There are 66 pages in Total which to scrape----")
page = input("Enter the page number to download : ")

#get url
url = "http://zqnrg4q6yn3ho4ii.onion"
final_url = url + "/pedo/page" + page + ".html"
print(final_url)
main(final_url)
