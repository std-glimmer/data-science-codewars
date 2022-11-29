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

# Статистика по среднему числу решений ката в зависимости от его категории
def get_kat_category_stat():
  katTagStat = {}
  katas = get_kat_id_kat_dict()
  print_tags = False
  for user in get_users_cursor():
    for t in user['userCompletedTasks']:
      for task in t:
        if (type(task) is dict and 'id' in task):
          tags = []
          if task['id'] in katas and 'tags' in katas[task['id']]:
            tags = katas[task['id']]['tags']
            if not print_tags:
              print(tags)
              print_tags = True
          for tag in tags:
            if tag not in katTagStat:
              katTagStat[tag] = {}
            if task['id'] in katTagStat[tag]:
              katTagStat[tag][task['id']] = katTagStat[tag][task['id']] + 1
            else:
              katTagStat[tag][task['id']] = 1
  name = 'kat_tags_stat.csv'
  sortedDict = collections.OrderedDict(sorted(katTagStat.items()))
  with open(name, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    names = ['category', 'Avg kat completed']
    spamwriter.writerow(names)
    # записываем ранг и статистику
    for category, katStat in sortedDict.items():
      avg = 0
      for kat, stat in katStat.items():
        avg = avg + stat
      if len(katStat) > 0:
        avg = avg / len(katStat)
      row = [category, avg]
      spamwriter.writerow(row)

get_kat_category_stat()
