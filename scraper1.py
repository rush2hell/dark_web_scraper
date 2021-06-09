#!/usr/bin/env python
from bs4 import *
import requests
import csv
import socks
import socket
import os
import datetime

def folder_create(images):
	try:
		# year month day 
		dayTime = datetime.datetime.now().strftime('%Y-%m-%d')
		# Minutes and seconds 
		hourTime = datetime.datetime.now().strftime('%H-%M-%S')

		folder_name = dayTime + '_' + hourTime
		#folder_name = input("Enter Folder Name:- ")
		# folder creation
		pwd = os.getcwd() + '\\' + "Evidence" + '\\' + folder_name
		print(pwd)
		 # Determine whether the folder already exists
		isExists = os.path.exists(pwd)
		if not isExists:
		    os.makedirs(pwd)
		#os.mkdir(folder_name)

	# if folder exists with that name, ask another name
	except:
		print("Folder Exist with that name!")
		folder_create()

	# image downloading start
	download_images(images, pwd)


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, pwd):
	
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
					with open(f"{pwd}/images_{folder_name+1}.jpg", "wb+") as f:
						f.write(r)

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
	folder_create(images)


# Configuring Socks to use Tor
from urllib.request import urlopen
socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
socket.socket = socks.socksocket

# It is necessary to use Tor for DNS resolution of Onion websites
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo

print("---There are 66 pages in Total which to scrape----")
page = input("Enter the page number to download : ")

#get url
url = "http://zqnrg4q6yn3ho4ii.onion"
final_url = url + "/pedo/page" + page + ".html"
main(url)




