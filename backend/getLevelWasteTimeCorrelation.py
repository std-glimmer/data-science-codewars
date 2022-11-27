from pymongo import MongoClient
import csv
import collections
import datetime

# Оценка влияния уровня ранга на временную активность на сервисе 
# (сколько времени тратит пользователь на сервисе в зависимости от ранга)

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

def get_katas_cursor():
  if 'cached_katas' not in globals():
    db = get_database()
    collection = db['katas']
    cached_katas = collection.find({})
  return cached_katas

TYPE_DIVISION_DAY = 0
TYPE_DIVISION_WEEK = 1
TYPE_DIVISION_MONTH = 2

# Статистика по рангу пользователя и количеству решённых им катов за единицу времени
def get_time_stat(timeType = 1):
  rankKatCompletionStat = {}
  for user in get_users_cursor():
    if 'ranks' in user and 'overall' in user['ranks'] and 'rank' in user['ranks']['overall']:
      rank = user['ranks']['overall']['rank']
      for t in user['userCompletedTasks']:
        timeDict = {}
        for task in t:
          if (type(task) is dict and 'completedAt' in task):
            if timeType == TYPE_DIVISION_DAY:
              day = task['completedAt'].split('T')[0]
              if day in timeDict:
                timeDict[day] = timeDict[day]
              else:
                timeDict[day] = 1
            if timeType == TYPE_DIVISION_WEEK:
              day = datetime.datetime.fromisoformat(task['completedAt'].split('T')[0]).date().isocalendar()
              week = day.year.__str__() + 'w' + day.week.__str__()
              if week in timeDict:
                timeDict[week] = timeDict[week] + 1
              else:
                timeDict[week] = 1
            if timeType == TYPE_DIVISION_MONTH:
              strs = task['completedAt'].split('-')
              month = strs[0] + '-' + strs[1]
              if month in timeDict:
                timeDict[month] = timeDict[month] + 1
              else:
                timeDict[month] = 1

      AVG = 0
      if len(timeDict) > 0:
        for id, time in timeDict.items():
          AVG = AVG + time
        AVG = AVG / len(timeDict)
      if rank in rankKatCompletionStat:
        rankKatCompletionStat[rank].append(AVG)
      else:
        rankKatCompletionStat[rank] = [AVG]
  finalStat = {}
  for rank, usersAvgTimedTasks in rankKatCompletionStat.items():
    rankSum = 0
    for userStat in usersAvgTimedTasks:
      rankSum = rankSum + userStat
    rankSum = rankSum / len(usersAvgTimedTasks)
    finalStat[rank] = rankSum
  name = 'completed_task_rank_day.csv' if timeType == TYPE_DIVISION_DAY else \
      'completed_task_rank_week.csv' if timeType == TYPE_DIVISION_WEEK else 'completed_task_rank_month.csv'
  with open(name, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['№', 'rank', 'AVG katas per ' + ('week' if timeType == TYPE_DIVISION_WEEK else
        'day' if timeType == TYPE_DIVISION_DAY else 'month')])

    # записываем ранг и соответствующее среднее значение
    sortedDict = collections.OrderedDict(sorted(finalStat.items()))
    for rank, avg_competed_tasks in sortedDict.items():
      spamwriter.writerow([abs(rank), rank, avg_competed_tasks])

get_time_stat(TYPE_DIVISION_DAY)
get_time_stat(TYPE_DIVISION_WEEK)
get_time_stat(TYPE_DIVISION_MONTH)
