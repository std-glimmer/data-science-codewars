import mongoManager
import json

# Статистика по использованию языков для решения кат среди игроков разных уровней
def get_common_stat():
   rankStat = [
      { "rank": 1, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 },
      { "rank": 2, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 },
      { "rank": 3, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 },
      { "rank": 4, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 },
      { "rank": 5, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 },
      { "rank": 6, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 },
      { "rank": 7, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 },
      { "rank": 8, "languagesSolutions": {}, "topLanguage": {}, "totalSolutions": 0, "totalUsers": 0 }
   ]

   i = 1
   for user in mongoManager.get_users_cursor():
      rank = abs(user["ranks"]["overall"]["rank"])

      for stat in rankStat:
         if stat["rank"] == rank:
            stat["totalUsers"] = stat["totalUsers"] + 1

            for t in user["userCompletedTasks"]:
               for task in t:
                  if (type(task) is dict and "completedLanguages" in task):
                     for language in task["completedLanguages"]:
                        stat["totalSolutions"] = stat["totalSolutions"] + 1
                        if (language in stat["languagesSolutions"]):
                           stat["languagesSolutions"][language] = stat["languagesSolutions"][language] + 1
                        else:
                           stat["languagesSolutions"][language] = 1

            break

      print("User " + str(i) + "done.")
      i = i + 1
   
   # Делаем выводим самый популярный язык отдельно
   for rank in rankStat:
      solutions = rank["languagesSolutions"]
      max = 0
      maxSolution = ""

      for solution in solutions:
         if solutions[solution] > max:
            max = solutions[solution]
            maxSolution = solution
      
      rank["topLanguage"] = { maxSolution: max }

   with open('E:\\projects\\data-science-codewars\\backend\\data\\languagesStat.json', 'w', newline='') as file:
      file.write(json.dumps(rankStat))
      file.close()

get_common_stat()
