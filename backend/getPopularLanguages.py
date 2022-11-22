from pymongo import MongoClient
import csv

# Предпочитаемые языки программирования в зависимости от ранга

def get_database():
   CONNECTION_STRING = "mongodb://root:qwerty@45.12.18.238:27019/?authMechanism=DEFAULT"
   client = MongoClient(CONNECTION_STRING)
   return client["codewars"]

def get_users_cursor():
   db = get_database()
   collection = db['users']
   return collection.find({})

def get_katas_cursor():
   db = get_database()
   collection = db['katas']
   return collection.find({})

# Статистика по популярности языков
def get_common_stat():
   languagesStat = {}

   for user in get_users_cursor():
      for t in user["userCompletedTasks"]:
         for task in t:
            if (type(task) is dict and "completedLanguages" in task):
               for language in task["completedLanguages"]:
                  if (language in languagesStat):
                     languagesStat[language] = languagesStat[language] + 1
                  else:
                     languagesStat[language] = 1

   with open('popular_language.csv', 'w', newline='') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      spamwriter.writerow(['language', 'numbers'])
      for language in languagesStat:
         spamwriter.writerow([ language, languagesStat[language] ])

# Статистика по популярности языков в зависимости от ранга
def get_specific_stat():
   rankStat = {}   

   for user in get_users_cursor():
      rank = user["ranks"]["overall"]["rank"]
      languageStat = {}

      for t in user["userCompletedTasks"]:
         for task in t:
            if (type(task) is dict and "completedLanguages" in task):
               for language in task["completedLanguages"]:
                  if (language in languageStat):
                     languageStat[language] = languageStat[language] + 1
                  else:
                     languageStat[language] = 1

      if (rank in rankStat):
         rankS = rankStat[abs(rank)]
         for language in languageStat:
            if (language in rankS):
               rankS[language] = rankS[language] + languageStat[language]
            else:
               rankS[language] = languageStat[language]
      else:
         rankStat[abs(rank)] = languageStat

   with open('E:\\projects\\data-science-codewars\\backend\\popular_language_rank.csv', 'w', newline='') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      spamwriter.writerow(['language', 'numbers'])

      # Здесь записываем только самый популярный язык
      for rank in rankStat:
         max = 0
         maxLang = ""
         
         for language in rankStat[rank]:
            cnt = rankStat[rank][language]
            
            if cnt > max:
               max = cnt
               maxLang = language

         spamwriter.writerow([ abs(rank), maxLang, max ])

get_specific_stat()
