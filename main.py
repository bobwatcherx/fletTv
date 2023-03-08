from flet import *
import requests
import subprocess
import os
import json

def main(page:Page):

	you_tv_name = TextField(label="insert tv name")

	# AND NOW REQUEST API to IPTV AND GET URL AND TV NAME
	myurl = "https://iptv-org.github.io/iptv/index.country.m3u"
	response = requests.get(myurl)
	# AND REMOVE LINE \n
	lines = response.text.split("\n")




	# AND NOW SEARCH TV FROM THE API
	def search_tv():
		channels = []
		for i,line in enumerate(lines):
			if line.startswith('#EXTINF:'):
				# EXTRACT INFORMATION LIKE TV NAME LOGO TV 
				info = line.split(",")[1]
				if '(' in info:
					tv_name,country_name = info.split(" (",maxsplit=1)
					country_name = country_name[:-1]
				else:
					tv_name = info
					country_name = ''
				# AND NOW EXTRACT THE URL OF TV 
				# IF FOUND
				url = lines[i+1].strip()

				logo_url = None
				for item in line.split(" "):
					if item.startswith("tv-logo="):
						logo_url =  item.split('"')[1]
						break

				# AND NOW CREATE ARRAY JSON TO WRITE TO  CHANNEL.json FILE
				current_channel = {
					'tv_name':tv_name,
					'country_name':country_name,
					'url':url,
					'logo_url':logo_url

				}

				channels.append(current_channel)

		# AND NOW WRITE TO JSON FIEL AFTER REQUEST ip TV 
		# AND ADD PERMISION TO THIS FOLDER PROJECT 
		# FOR WRITE AND READ
		# IF YOU USE LINUX USE chmod -R 777 THIS FOLDER
		with open("channels.json","w") as f:
			json.dump(channels,f,indent=4)

	# AND NOW CALL FUNCTION WHEN FLET FIRST RUNNING
	search_tv()


	def watchnowtv(e):
		# NOW OPEN FILE channels.Json AND READ FILE
		with open("channels.json","r")as f:
			channels = json.load(f)

		# AND FIND YOU INPUT TV BY NAME IN FILE CHANNELS.json 
		tv_name = you_tv_name.value.lower()
		matched_channel = [channel for channel in channels if tv_name in channel['tv_name'].lower()]

		# AND IF NOT MATCHER THEN PRINT NOT MATCHED TV
		if not matched_channel:
			print(f" no tv found you search {tv_name}")
			return

		# AND IF FOUND > 1 TV . 
		if len(matched_channel) > 1:
			print("YOU FOUND MANY TV ")
			for i , channel in enumerate(matched_channel):
				# SHOW DUPLICATE NAME TV IF FOUND 2 OR MANY
				print(f"{i+1} . TV : {channel['tv_name']} {channel['country_name'] }")
			choices = int(input("choice you tv for watch = "))
			
		else:
			choices = 1

		# AND NOW PLAY TV TO VLC WITHOUT ROOT
		# IF YOU USE ROOT for RUN flet main.py YOU CANt play
		# YOU MUST RUN THIS APP WITH normal USER
		channel_url = matched_channel[choices-1]['url']
		# AND CALL VLC FROM TERMINAL
		subprocess.call(['vlc',channel_url])
		page.update()


		# AND NOW THE APPLICATION WILL LONG TIME REFRESH
		# BEACAUSE FIND TV
		# YOU WAITING FOR OPEN APP




	page.add(
	AppBar(
	title=Text("FLet Tv",weight="bold",color="white"),
	bgcolor="blue"
		),
	Column([
		you_tv_name,
		ElevatedButton("watch tv now",
			bgcolor="blue",color="white",
			on_click=watchnowtv
			)

		])
		)

flet.app(target=main)
