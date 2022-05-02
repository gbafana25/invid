#!/usr/bin/python3
import json
import requests
import sys

BASE_URL = "https://vid.puffyan.us/api/v1"


def searchVideos():
	# parameter list, attach to end of url
	# not in request body
	qu = input("Search> ")
	d = {
		'q':qu,
		'page':1,
		'sort_by':'relevance',
		'date':'today',
		'duration':'short',
		'type':'video',
		'features':'hd',
		'region':'US'
	}
	ds = json.dumps(d)
	print("searching...")
	r = requests.get(BASE_URL+"/search?q="+qu)
	p = r.json()
	for e in range(len(p)):
		try:
			print(str(e) + ")", p[e]['title'] + "  | " + str(round(p[e]['lengthSeconds']/60)) + "min")
		except:
			pass
	v = input("> ")
	return e[int(v)]['videoId']
	


def popularVideos():
	print("getting list of popular videos...")
	r = requests.get(BASE_URL+"/popular")
	s = json.loads(r.text)
	for i in range(len(s)):
		print(str(i) + ")", s[i]['title'] + "  | " + str(round(s[i]['lengthSeconds']/60)) + "min")
	v = input("> ")
	return s[int(v)]['videoId']


def downloadVideo(l):
	v = requests.get(BASE_URL+"/videos/"+l)
	p = json.loads(v.text)
	for t in p['formatStreams']:
		if(t['resolution'] == '720p'):
			#print(t['url'])
			raw = requests.get(t['url'])
			o = open("video.mp4", "wb+")
			print("downloading video...")
			o.write(raw.content)
			o.close()


if(len(sys.argv) == 2):
	if(sys.argv[1] == 'search'):
		vid = searchVideos()
		downloadVideo(vid)
	elif(sys.argv[1] == 'popular'):
		vid = popularVideos()
		downloadVideo(vid)
else:
	print("type a command...")
	exit(0)
