import mongoManager
import get_usernames as gu
import json
from statistics import mean

# Соотношение количества очков к количеству решённых катов у лидеров топ-100. 
# Посмотреть сколько задач им потребовалось решить, чтобы попасть в топ leaderboard.
def getLeadersStat():
   leadersStat = []

   # Получаем актуальный список лидеров по задачам
   usernames = gu.getUsernames(gu.LEADERBOARD_2)

   print(len(usernames))

   i = 0
   for user in mongoManager.get_users_cursor():
      if user["username"] in usernames:
         leadersStat.append({ "score": user["ranks"]["overall"]["score"], "katasAuthored": user["codeChallenges"]["totalAuthored"], "katasSolved": user["codeChallenges"]["totalCompleted"] })
      i = i + 1
      print("User " + str(i) + " passed")

   # Обрезаем до первых 100
   leadersStat.sort(key=lambda leader: leader["katasSolved"], reverse=True)
   leadersStat = leadersStat[0:100]

   mid_rates = []
   mid_scores = []
   mid_katas_solved = []
   for leader in leadersStat:
      mid_scores.append(leader["score"])
      mid_katas_solved.append(leader["katasSolved"])
      mid_rates.append(leader["score"] / leader["katasSolved"])

   result = {
      "max_katas": leadersStat[0]["katasSolved"],
      "min_katas": leadersStat[len(leadersStat) - 1]["katasSolved"],
      "max_score": leadersStat[0]["score"],
      "min_score": leadersStat[len(leadersStat) - 1]["score"],
      "mid_scores": mean(mid_scores),
      "mid_katas_solved": mean(mid_katas_solved),
      "mid_rate": mean(mid_rates),
      "data": leadersStat
   }

   with open('top100Stat.json', 'w', newline='') as file:
      file.write(json.dumps(result))
      file.close()

getLeadersStat()
