#!/usr/bin/env python

import json
import re
import csv

data = "minecraftServer/map/stats/playerName.json"
items = "items_id.tsv"

class MCJson:
	def __init__(self, data, items):
		fic = open(data, 'r')
		jsondata = fic.read()
		fic.close()

		self.items = {}
		with open(items, 'rb') as csvfile:
			fic = csv.reader(csvfile, delimiter='\t')
			for item in fic:
				self.items[item[0]] = item[1]

		self.dic_ach = {}
		self.dic_block = {"mine":[]}
		self.dic_item = {"use":[], "craft":[], "break":[]}

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
					t_item = (ident, dico[key])
					self.dic_item["use"].append(t_item)
				if a_item[1] == 'craftItem':
					t_item = (ident, dico[key])
					self.dic_item["craft"].append(t_item)
				if a_item[1] == 'breakItem':
					t_item = (ident, dico[key])
					self.dic_item["break"].append(t_item)
				if a_item[1] == 'mineBlock':
					t_item = (ident, dico[key])
					self.dic_block["mine"].append(t_item)

		"""
		print "Liste des objets :", len(self.items)
		print self.items
		"""
		"""
		print "Nombre de succes :", len(self.dic_ach)
		print self.dic_ach
		print "Objets utilises :", len(self.dic_item["use"])
		print self.dic_item["use"]
		print "Objets fabriques :", len(self.dic_item["craft"])
		print self.dic_item["craft"]
		print "Objets detruits :", len(self.dic_item["break"])
		print self.dic_item["break"]
		print "Blocs mines :", len(self.dic_block["mine"])
		print self.dic_block["mine"]
		"""

	def get_item_table(self):
		table = {}
		# ordre de recuperation :
		# [0] => mine - [1] => use - [2] => craft - [3] => break
		for item in self.dic_block["mine"]:
			try:
				key = self.items[item[0]]
			except:
				key = item[0]
			if not key in table:
				table[key] = [0, 0, 0, 0]
			table[key][0] = item[1]

		for item in self.dic_item["use"]:
			try:
				key = self.items[item[0]]
			except:
				key = item[0]
			if not key in table:
				table[key] = [0, 0, 0, 0]
			table[key][1] = item[1]

		for item in self.dic_item["craft"]:
			try:
				key = self.items[item[0]]
			except:
				key = item[0]
			if not key in table:
				table[key] = [0, 0, 0, 0]
			table[key][2] = item[1]

		for item in self.dic_item["break"]:
			try:
				key = self.items[item[0]]
			except:
				key = item[0]
			if not key in table:
				table[key] = [0, 0, 0, 0]
			table[key][3] = item[1]

		return table

if __name__ == "__main__":
	json = MCJson(data, items)
	table_item = json.get_item_table()
	
	print "Item\tMined\tUsed\tCrafted\tBreak"
	for item in table_item.keys():
		print item+"\t"+ "\t".join(str(t) for t in table_item[item])
