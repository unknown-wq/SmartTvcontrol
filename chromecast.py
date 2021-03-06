import pychromecast
import time
import sys

print("Scanning...",end=" It's take no more than a minute.\n")
services, browser = pychromecast.discovery.discover_chromecasts()
pychromecast.discovery.stop_discovery(browser)
if len(services)==0:
	print("\33[91m 0 \33[0m Devices Found\n")
	exit()
if len(sys.argv)>1:
	if sys.argv[1]=="--d":
		print(" \33[92m",len(services),"\33[0m Devices found")
		print("\t Name\t UID")
		for x in  range(len(services)):
			print("\33[94m %d. \33[0m\t %s\t %s"% (x,services[x][3],services[x][1]))



else:
	print("\33[92m",len(services),"\33[0m Devices found")
	print("\t Name\t UID")
	for x in  range(len(services)):
		print("\33[94m %d. \33[0m \t%s\t "% (x,services[x][3]))
print('Enter number of device: ',end='')

chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[services[int(input())][3]])
[cc.device.friendly_name for cc in chromecasts]
cast = chromecasts[0]
if len(cast.device)==5:
	print("Connected")
else:
	print("Connection error")
	print(cast.device)
	print(cast.status)
	exit()
cast.wait()
#print(cast.device)
#print(cast.status)
mc = cast.media_controller
mc.block_until_active()

while True:
	print("\t1.) Play \n\t2.) Pause \n\t3.) Show what playing now \n\t4.) Set volume \n\t5.) play video\n\t6.) Pause and exit")
	print("$: ",end="")
	a=int(input())
	if a==1:
		mc.play()
		print('sent.')
	if a==2:
		mc.pause()
		print('sent.')

	if a==3:
		if len(sys.argv)>1:
			if sys.argv[1]=="--d":
				print(mc.status)
		else:
			print(mc.status.title, end="\t")
			print(mc.status.artist)
			print(mc.status.current_time,end=" ")
			print("of",end=" ")
			print(mc.status.duration)
	if a==6:
		pychromecast.discovery.stop_discovery(browser)
		print('sent. \n Connection closed.')
		mc.pause()
		print('exit')
		exit()
	if a==4:
		print(mc.status.volume_level)
		print("Muted: ",end="")
		print(mc.status.volume_muted)
		print("Enter volume(from 0 to 100): ", end="")
		cast.set_volume((float(input())/100))
	if a==5:
		print('input link to video:',end=" ")
		link=input()
		mc.play_media(link, 'video/mp4')
	else:
		pass
