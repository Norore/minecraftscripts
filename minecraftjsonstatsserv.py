#!/usr/bin/env python

import json
import re

data = "minecraftserver/map/stats/playerName.json"
fic = open(data, 'r')
jsondata = fic.read()
fic.close()

try:
	dico = json.loads(jsondata)
except:
	print "data not loaded"

ach,stat=1,1
for key in dico.keys():
	if re.match(r'achievement', key):
#		print key,dico[key]
		ach+=1
	if re.match(r'stat', key):
#		print key,dico[key]
		stat+=1

print "Nombre de succes :",ach
print "Nombre de stat :",stat
