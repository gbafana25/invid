#!/usr/bin/python3
import json
import requests
import sys

BASE_URL = "https://inv.riverside.rocks/api/v1"


def searchVideos():
	qu = input("Search> ")	
	print("searching...")
	r = requests.get(BASE_URL+"/search?q="+qu)
	p = r.json()
	for e in range(10):
		try:
			print(str(e) + ")", p[e]['title'] + "  | " + str(round(p[e]['lengthSeconds']/60)) + "min  | " + p[e]['publishedText'])
		except:
			pass
	v = input("> ")
	return (p[int(v)]['videoId'], p[int(v)]['title'])
	


def popularVideos():
	print("getting list of popular videos...")
	r = requests.get(BASE_URL+"/popular")
	s = json.loads(r.text)
	for i in range(len(s)):
		print(str(i) + ")", s[i]['title'] + "  | " + str(round(s[i]['lengthSeconds']/60)) + "min  | " + s[i]['publishedText'])
	v = input("> ")
	return (s[int(v)]['videoId'], s[int(v)]['title'])


def downloadVideo(l):
	v = requests.get(BASE_URL+"/videos/"+l[0])
	p = json.loads(v.text)
	#print(p['adaptiveFormats'])
	for t in range(len(p['formatStreams'])):
		print(str(t) + ") " + p['formatStreams'][t]['resolution'])
	res = input("Select quality> ")
	url = p['formatStreams'][int(res)]['url']
	print("downloading video...")
	raw = requests.get(url)
	ext = ".mp4"
	with open("video"+ext, "wb+") as o:
		o.write(raw.content)
		o.close()



if(len(sys.argv) == 2):
	if(sys.argv[1] == 'search'):
		while True:
			vid = searchVideos()
			downloadVideo(vid)
	elif(sys.argv[1] == 'popular'):
		vid = popularVideos()
		downloadVideo(vid)
else:
	print("type a command...")
	exit(0)
