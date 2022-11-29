from pymongo import MongoClient
import csv
import collections
import datetime

# Анализ зависимости категорий решаемых катов от ранга 

def get_database():
  CONNECTION_STRING = "mongodb://root:qwerty@45.12.18.238:27019/?authMechanism=DEFAULT"
  client = MongoClient(CONNECTION_STRING)
  return client["codewars"]

def get_users_cursor():
  if 'cached_users' not in globals():
    db = get_database()
    collection = db['users']
    cached_users = collection.find({})
  return cached_users

def get_kat_id_kat_dict():
  if 'cached_katas' not in globals():
    cached_katas = {}
    db = get_database()
    collection = db['katas']
    katas = collection.find({})
    for obj in katas:
      if 'id' in obj:
        cached_katas[obj['id']] = obj
  return cached_katas

# Статистика по категорий катов для рангов
def get_kat_category_stat():
  rankKatTagStat = {}
  tagNameList = []
  katas = get_kat_id_kat_dict()
  for user in get_users_cursor():
    if 'ranks' in user and 'overall' in user['ranks'] and 'rank' in user['ranks']['overall']:
      rank = abs(user['ranks']['overall']['rank'])
      if rank not in rankKatTagStat:
        rankKatTagStat[rank] = {}
      for t in user['userCompletedTasks']:
        for task in t:
          if (type(task) is dict and 'id' in task):
            tags = []
            if task['id'] in katas and 'tags' in katas[task['id']]:
              tags = katas[task['id']]['tags']
            for tag in tags:
              if tag not in tagNameList:
                tagNameList.append(tag)
              if tag in rankKatTagStat[rank]:
                rankKatTagStat[rank][tag] = rankKatTagStat[rank][tag] + 1
              else:
                rankKatTagStat[rank][tag] = 1
  name = 'rank_kat_tag_stat.csv'
  tagNameList.sort()
  sortedDict = collections.OrderedDict(sorted(rankKatTagStat.items()))
  with open(name, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    names = ['№', 'rank']
    for tag in tagNameList:
      names.append(tag)
    spamwriter.writerow(names)
    # записываем ранг и статистику
    for rank, tagList in sortedDict.items():
      row = [abs(rank), rank]
      for tag in tagNameList:
        if tag in tagList:
          row.append(tagList[tag])
        else:
          row.append(0)
      spamwriter.writerow(row)

get_kat_category_stat()
