import requests
import json
import os

# Функция для считывания списка, сохраненного в файле
def readListFromFile(filePath):
    lst = set()
    print(filePath)
    file = open(filePath, 'r+')
    for row in file.read().splitlines():
        lst.add(row)
    file.close()
    return lst

def mining_users(targetPath):
    API_USER_REQUEST        = "https://www.codewars.com/api/v1/users/{user}"
    API_COMPLETED_REQUEST   = "https://www.codewars.com/api/v1/users/{user}/code-challenges/completed?page={page}"

    # Настройка путей
    USERNAMES_FILE          = targetPath + "\\saved_usernames.txt"
    KATA_IDS_FILE           = targetPath + "\\saved_katas.txt"
    INVALID_USERNAMES_FILE  = targetPath + "\\invalid_users.txt"

    # Читаем списки уже загруженных пользователей и задач
    saved_user_ids = readListFromFile(USERNAMES_FILE)
    saved_kata_ids = readListFromFile(KATA_IDS_FILE)

    # Получаем список пользователей из api
    users = saved_user_ids | readListFromFile(targetPath + "\\sourceUsers.txt")
    
    # Открываем на запись файл со списком загруженных задач и пользователей
    kata_ids_file = open(KATA_IDS_FILE, 'a+')
    user_ids_file = open(USERNAMES_FILE, 'a+')
    invalid_users_file = open(INVALID_USERNAMES_FILE, 'a+')
    
    print("Already loaded ", len(saved_user_ids), " users.")
    print("Already loaded ", len(saved_kata_ids), " tasks.")
    print("Found new ", len(users), " users.")
    
    # Служебные функции
    # ------------------------------------------------------------------------------------------------------------------    
    # Получить информацию по выполненным задачам пользователя (страница pageN)
    def getKatasInfoOnPage(user, pageN):
        userCompletedTasksPage = {}
        try:
            response = requests.get(API_COMPLETED_REQUEST.replace("{user}", user).replace("{page}", str(pageN)))
            userCompletedTasksPage = response.json()
        except requests.exceptions.JSONDecodeError:
            print(user, "JSONDecodeError on page #", pageN)
            return "", 0, 0

        for kata in userCompletedTasksPage["data"]:
            kata_ids_file.write(kata["id"] + "\n")
            kata_ids_file.flush()
    
        return userCompletedTasksPage["data"], userCompletedTasksPage["totalPages"]
    
    # Оформить информацию о выполненных задачах пользователя
    def getCompletedKatas(user):
        userCompletedKatas = []
    
        print("Investigating page #1...")
    
        # Сначала получаем информацию по первой странице + узнаем сколько всего страниц
        katasInfo, userTotalPages = getKatasInfoOnPage(user, 0)
        userCompletedKatas.append(katasInfo)
    
        print("Found ", userTotalPages, "pages with tasks.")
        
        # Если больше 0 -> продолжаем добирать
        for n in range(1, userTotalPages):
            userCompletedKatas.append(getKatasInfoOnPage(user, n))
            print("Page", n, "done.")
    
        return userCompletedKatas
    # ------------------------------------------------------------------------------------------------------------------
    
    print("Starting...")
    print(len(users), "new users found. Loading...")
    
    # i считаем уже загруженные файлы
    i = 0
    for path in os.listdir(targetPath + "\\users\\"):
        if os.path.isfile(os.path.join(targetPath + "\\users\\", path)):
            i += 1

    for user in users:
        print("\nStart processing " + user + "...")
    
        print("Requesting user data from Codewars...")
        userData = {}
        # Основная информация по пользователю из codewars
        try:
            response = requests.get(API_USER_REQUEST.replace("{user}", user))
            userData = response.json()
        except requests.exceptions.JSONDecodeError:
            print(user, "JSONDecodeError in user data request")
            invalid_users_file.write(user + "\n")
            invalid_users_file.flush()
            continue;
        
        print("Done.")
    
        print("Saving data...")
        userJson = {
            'username':                     userData['username'],
            'name':                         userData['name'],
            'honor':                        userData['honor'],
            'clan':                         userData['clan'],
            'leaderboardPosition':          userData['leaderboardPosition'],
            'skills':                       userData['skills'],
            'ranks':                        userData['ranks'],
            'codeChallenges':               userData['codeChallenges'],
            'userCompletedTasks':           getCompletedKatas(user)
        }
    
        user_ids_file.write(user + "\n")
        user_ids_file.flush()

        usersFile = open(targetPath + "\\users\\user" + str(i) + ".json", 'a+')
        usersFile.write(json.dumps(userJson))
        usersFile.close()

        print(user, "done.", len(users) - i, "remaining")
        i += 1
    
    # Закрываем дескрипторы
    user_ids_file.close()
    kata_ids_file.close()
    invalid_users_file.close()

mining_users(".\\")