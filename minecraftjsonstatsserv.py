#!/usr/bin/env python

import json
import re
import unicodedata

data = "minecraftserver/map/stats/playerName.json"

class MCJson:
	def __init__(self, data):
		fic = open(data, 'r')
		jsondata = fic.read()
		fic.close()

		self.dic_ach = {}
		self.dic_block = {"mine":[]}
		self.dic_item = {"use":[], "crafted":[], "break":[]}

		try:
			dico = json.loads(jsondata)
		except:
			print "data not loaded"

		for key in dico.keys():
			key.encode('ascii', 'ignore')
			a_item = re.split('\.', key)
			if len(a_item) >= 3:
				ident = a_item[2].encode('ascii', 'ignore')

			if re.match(r'achievement', key):
				ach = a_item[1].encode('ascii', 'ignore')
				self.dic_ach[ach] = dico[key]

			if a_item[0] == 'stat':
				if a_item[1] == 'useItem':
					t_item = (int(ident), dico[key])
					self.dic_item["use"].append(t_item)
				if a_item[1] == 'craftItem':
					t_item = (int(ident), dico[key])
					self.dic_item["crafted"].append(t_item)
				if a_item[1] == 'breakItem':
					t_item = (int(ident), dico[key])
					self.dic_item["break"].append(t_item)
				if a_item[1] == 'mineBlock':
					t_item = (int(ident), dico[key])
					self.dic_block["mine"].append(t_item)

		print "Nombre de succes :", len(self.dic_ach)
		print self.dic_ach
		print "Objets utilises :", len(self.dic_item["use"])
		print self.dic_item["use"]
		print "Objets fabriques :", len(self.dic_item["crafted"])
		print self.dic_item["crafted"]
		print "Objets detruits :", len(self.dic_item["break"])
		print self.dic_item["break"]
		print "Blocs mines :", len(self.dic_block["mine"])
		print self.dic_block["mine"]

if __name__ == "__main__":
	MCJson(data)

exit(0)
