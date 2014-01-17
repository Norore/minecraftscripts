#!/usr/bin/env python

import json
import re

data = "/home/mineternity/mineternity/stats/Norore.json"
fic = open(data, 'r')
jsondata = fic.read()
fic.close()

try:
	dico = json.loads(jsondata)
except:
	print "data not loaded"

cpt=1
for key in dico.keys():
	strkey = str(key)
	if re.match(r'achievement', key):
		print key,dico[key]
		cpt+=1

print cpt
