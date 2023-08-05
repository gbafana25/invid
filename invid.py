#!/usr/bin/python3
import json
import requests
import sys
import os
import time

# add list of instances
#BASE_URL = "https://vid.puffyan.us/api/v1"
#BASE_URL = "https://invidious.slipfox.xyz/api/v1"
BASE_URLS = ["https://invidious.slipfox.xyz","https://vid.puffyan.us", "inv.tux.pizza", "invidious.io.lol"]
URL = ""

# removes characters that cause ffmpeg command to fail
def sanitizeTitle(name):
	return name.replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').replace("\"", "").replace(":", "").replace(",", "")

def convertToMp3(name, src):	
	print(name)
	print(src)
	os.system("ffmpeg -i "+src+" "+name+".mp3")


def searchVideos(term):
	# returns first video from search
	if(term != None):
		print("searching...")
		r = requests.get(URL+"/api/v1/search?q="+term)
		p = r.json()	
		return (p[0]['videoId'], p[0]['title'], "n")

	qu = input("Search> ")	
	print("searching...")
	r = requests.get(URL+"/api/v1/search?q="+qu)
	p = r.json()
	count = 0
	vid_list = []
	for e in range(10):
		try:
			if(p[e]['type'] == "video"):
				vid_title = ""
				if(len(p[e]['title']) <= 25):
					vid_title = p[e]['title']
				else:
					vid_title = p[e]['title'][:24]+"..."
					
					
				print(str(count) + ")", vid_title + "|" + p[e]['author'] + "|" + str(round(p[e]['lengthSeconds']/60)) + "min|" + str(p[e]['viewCount']) + "|" + p[e]['publishedText'])
				vid_list.append((count, e))
				count += 1
		except:
			pass

	v = input("> ")
	for i in range(len(vid_list)):
		if vid_list[i][0] == int(v):
			form = input("Keep as video? [y/n] ").lower()	
			return (p[vid_list[i][1]]['videoId'], p[vid_list[i][1]]['title'], form)
		

def downloadVideo(l):
	v = requests.get(URL+"/api/v1/videos/"+l[0])
	p = json.loads(v.text)	
	# list index correlates to video quality 
	# 0 - usually 144p

	url = p['formatStreams'][len(p['formatStreams'])-1]['url']
	print("downloading video...")
	raw = requests.get(url)
	ext = ".mp4"
	filename = sanitizeTitle(l[1])
	with open(filename+ext, "wb+") as o:
		o.write(raw.content)
		o.close()

	if(l[2] == 'y'):
		print("Keeping as .mp4...")
	elif(l[2] == 'n'):
		convertToMp3(filename, filename+ext)
	"""
	if(len(sys.argv) == 2):
		convertToMp3(filename, filename+ext)
	elif(sys.argv[2] == "video"):
		print("Keeping as .mp4...")
	"""

def testInstances():
	for i in range(len(BASE_URLS)):
		try:
			r = requests.get(BASE_URLS[i])
			return BASE_URLS[i]
		except ConnectionError:
			print(URL+" doesn't work, skipping...")	


if(len(sys.argv) >= 2):
	URL = testInstances()	
	if(sys.argv[1] == 'search'):
		while True:
			vid = searchVideos(None)
			downloadVideo(vid)
	elif(sys.argv[1] == 'from-list'):
		with open("search-terms", "r") as searches:
			for search in searches:
				vid = searchVideos(search)
				downloadVideo(vid)
				print("5 second delay for rate limit")
				time.sleep(5)
	
else:
	print("type a command...")
	exit(0)
