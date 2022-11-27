import mongoManager
import json

# Соотношение количества очков к количеству решённых катов у лидеров топ-100. 
# Посмотреть сколько задач им потребовалось решить, чтобы попасть в топ leaderboard.
def getLeadersStat():
   leadersStat = []

   i = 0
   for user in mongoManager.get_users_cursor():
      #if type(user["leaderboardPosition"]) is int and user["leaderboardPosition"] <= 100:
      leadersStat.append({ "position": user["leaderboardPosition"], "honor": user["honor"], "score": user["ranks"]["overall"]["score"], "katasAuthored": user["codeChallenges"]["totalAuthored"], "katasSolved": user["codeChallenges"]["totalCompleted"] })
      i = i + 1
      print("User " + str(i) + " passed")

   leadersStat.sort(key=lambda leader: leader["score"], reverse=True)

   with open('E:\\projects\\data-science-codewars\\backend\\leadersStat.json', 'w', newline='') as file:
      file.write(json.dumps(leadersStat))
      file.close()

def getLenWithoutDublicates():
   unique = set()

   file =  open('E:\\projects\\miner\\users.txt', 'r')
   for row in file.read().splitlines():
      unique.add(row)
   file.close()

   print(len(unique))

getLenWithoutDublicates()
