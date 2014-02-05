#!/usr/bin/env python

import json
import re
import csv

data = "/home/mineternity/mineternity/stats/Norore.json"
items = "/home/site/mineternity/stats/items_id.tsv"

class MCJson:
    def __init__(self, data, items):
        try:
            fic = open(data, 'r')
            jsondata = fic.read()
            fic.close()
        except IOError:
            pass

        self.items = {}
        with open(items, 'rb') as csvfile:
            fic = csv.reader(csvfile, delimiter='\t')
            for item in fic:
                self.items[item[0]] = item[1]

        self.dic_ach = {}
        self.dic_block = {"mine":[]}
        self.dic_item = {"use":[], "craft":[], "break":[]}
        self.dic_kill = {"kill":[], "killBy":[]}
        self.biome = []
        self.dic_user = {}

        try:
            dico = json.loads(jsondata)
        except:
            dico = {}

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
                if a_item[1] == 'killEntity':
                    t_item = (ident, dico[key])
                    self.dic_kill["kill"].append(t_item)
                if a_item[1] == 'entityKilledBy':
                    t_item = (ident, dico[key])
                    self.dic_kill["killBy"].append(t_item)
                else:
                    stat = a_item[1].encode('ascii', 'ignore')
                    self.dic_user[stat] = dico[key]

            if a_item[0] == 'achievement':
                if a_item[1] == 'exploreAllBiomes':
                    for biome in dico[key][u'progress']:
                        biome = biome.encode('ascii', 'ignore')
                        self.biome.append(biome)

    def get_dic_achievement(self):
        return self.dic_ach

    def get_dic_item(self):
        return self.dic_item

    def get_dic_block(self):
        return self.dic_block

    def get_dic_kill(self):
        return self.dic_kill

    def get_dic_user(self):
        return self.dic_user

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

        items_list = []
        for key in table:
            item = { "item": key, "list": table[key] }
            items_list.append(item)
        return items_list

    def get_kill_count(self):
        table = {}
        # ordre de recuperation :
        # [0] => kill - [1] => killBy
        for item in self.dic_kill["kill"]:
            key = item[0]
            if not key in table:
                table[key] = [0, 0]
            table[key][0] = item[1]

        for item in self.dic_kill["killBy"]:
            key = item[0]
            if not key in table:
                table[key] = [0, 0]
            table[key][1] = item[1]

        mobs_list = []
        for key in table:
            mob = { "mob": key, "list": table[key] }
            mobs_list.append(mob)
        return mobs_list

    def get_explored_biomes(self):
        return self.biome

if __name__ == "__main__":
    json = MCJson(data, items)

    #print json.get_dic_achievement()
    #print json.get_dic_user()
    kills = json.get_kill_count()
    nbkill = 0
    for k in kills:
        if k["list"][1] != 0:
            nbkill += k["list"][1]
    print nbkill
