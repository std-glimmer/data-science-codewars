import get_usernames as gu
import requests
import json
import os

# Функция для считывания списка, сохраненного в файле
def readListFromFile(filePath):
    file = open(filePath, 'r+')
    lst = file.read().splitlines()
    file.close()
    return lst

# Получение и обработка списка пользователей
def processUsernames(saved_user_ids):
    users = []
    before_utf_users = gu.getLeadernames()
    # Убираем из списка уже загруженных пользователей    
    before_utf_users = before_utf_users.difference(saved_user_ids)
    # Проверка на совместимость с utf-8, тех кто не подходит - отсеиваем
    for user in before_utf_users:
        try:
            user.encode('utf-8')
            users.append(user)
        except UnicodeError:
            continue;
    utfDiff = len(before_utf_users) - len(users)

    if utfDiff > 0:
        print(utfDiff + " users erased from list, because usernames contain restricted symbols.")

    return users

def start(targetPath):
    
    API_USER_REQUEST        = "https://www.codewars.com/api/v1/users/{user}"
    API_COMPLETED_REQUEST   = "https://www.codewars.com/api/v1/users/{user}/code-challenges/completed?page={page}"
    API_CHALLENGES_REQUEST  = 'https://www.codewars.com/api/v1/code-challenges/{challenge}'
    GITHUB_USER_REQUEST     = 'https://api.github.com/users/{user}'

    # Настройка путей
    USERNAMES_FILE          = targetPath + "saved_user_ids.txt"
    TASK_IDS_FILE           = targetPath + "saved_task_ids.txt"
    USERS_DATA_FILE         = targetPath + "users.json"
    TASKS_DATA_FILE         = targetPath + "tasks.json"

    if not os.path.exists(USERNAMES_FILE):
        os.mknod(USERNAMES_FILE)
        print(USERNAMES_FILE, "created.")
    if not os.path.exists(TASK_IDS_FILE):
        os.mknod(TASK_IDS_FILE)
        print(TASK_IDS_FILE, "created.")

    # Читаем списки уже загруженных пользователей и задач
    saved_user_ids = readListFromFile(USERNAMES_FILE)
    saved_task_ids = readListFromFile(TASK_IDS_FILE)

    # Получаем список пользователей из api
    users = processUsernames(saved_user_ids)
    
    # Открываем на запись файл со списком загруженных задач и пользователей
    task_ids_file = open(TASK_IDS_FILE, 'a+')
    user_ids_file = open(USERNAMES_FILE, 'a+')
    
    print("Users will be recorded to " + USERS_DATA_FILE)
    print("Tasks will be recorded to " + TASKS_DATA_FILE)
    print("Already loaded ", len(saved_user_ids), " users.")
    print("Already loaded ", len(saved_task_ids), " tasks.")
    print("Found new ", len(users), " users.")
    
    # Создаем / открываем файл пользователей
    usersFile = open(USERS_DATA_FILE, 'a+', newline="", encoding="utf-8")
    
    # Создаем / открываем файл задач
    tasksFile = open(TASKS_DATA_FILE, 'a+', newline="", encoding="utf-8")
    
    # Служебные функции
    # ------------------------------------------------------------------------------------------------------------------
    # Сохранить информацию о задаче в файл
    def saveTaskToFile(task):
        if (task and ("id" in task)):
            id = task["id"]
            if id not in saved_task_ids:
                saved_task_ids.append(id)
                task_ids_file.write(id + "\n")
                tasksFile.write(json.dumps(task) + "\n")
                return True
    
        return False
    
    # Получить информацию по выполненным задачам пользователя (страница pageN)
    def getTasksInfoOnPage(user, pageN):
        tasks = []
        userCompletedTasksPage = ""
    
        try:
            response = requests.get(API_COMPLETED_REQUEST.replace("{user}", user).replace("{page}", str(pageN)))
            userCompletedTasksPage = response.json()
        except requests.exceptions.JSONDecodeError:
            print(user, "JSONDecodeError on page #", pageN)
            return "", 0, 0
    
        userTotalPages = userCompletedTasksPage["totalPages"]
        userTotalTaskCount = userCompletedTasksPage["totalItems"]
        userCompletedTasksData = userCompletedTasksPage["data"]

        taskC = 1
        # Делаем запрос на информацию по задаче и мерджим с userCompletedTasksData
        for task in userCompletedTasksData:
            taskInfo = {}
    
            try:
                taskInfoRes = requests.get(API_CHALLENGES_REQUEST.replace("{challenge}", task["id"]))
                taskInfo = taskInfoRes.json()
            except requests.exceptions.JSONDecodeError:
                print(user, "JSONDecodeError on page #", pageN, "in task", task["id"])
                continue;
    
            # Сохраняем задачи в файл
            if saveTaskToFile(taskInfo):
                print("Saved task", task["id"], "|", taskC, "/", len(userCompletedTasksData))
    
            taskInfo['completedAt'] = task['completedAt']
            taskInfo['completedLanguages'] = task['completedLanguages']

            tasks.append(taskInfo)

            taskC = taskC + 1
    
        return tasks, userTotalPages, userTotalTaskCount
    
    # Оформить информацию о выполненных задачах пользователя
    def getCompletedTasks(user):
        userCompletedTasks = []
    
        print("Investigating page #1...")
    
        # Сначала получаем информацию по первой странице + узнаем сколько всего страниц
        tasksInfo, userTotalPages, userTotalTaskCount = getTasksInfoOnPage(user, 0)
        userCompletedTasks.append(tasksInfo)
    
        print("Found ", userTotalPages, "pages with tasks.")
        
        # Если больше 0 -> продолжаем добирать
        for n in range(1, userTotalPages):
            userCompletedTasks.append(getTasksInfoOnPage(user, n))
            print("Page", n, "done.")
    
        return userCompletedTasks, userTotalTaskCount
    
    # Получить информацию о профиле Github пользователя, если такой имеется
    def getGithubData(user):
        data = []
    
        try:
            github_response = requests.get(GITHUB_USER_REQUEST.replace("{user}", user))
        except requests.exceptions.JSONDecodeError:
            print(user, "JSONDecodeError in github request")
            return data
        
        if (bool(github_response)):
            data = github_response.json()
            print(user + " has Github account. Loaded.")
        else:
            print(user + " has NOT Github account.")
        
        return data
    # ------------------------------------------------------------------------------------------------------------------
    
    print("Starting...")
    print(len(users), "new users found. Loading...")
    
    # Начинаем основной цикл запросов к codewars и github за подробностями по пользователям
    i = 1
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
            continue;
        
        print("Done.")
    
        # Информация по выполненным задачам
        print("Requesting completed tasks data...")
        userCompletedTasks, userTotalTaskCount = getCompletedTasks(user)
        print("Done.")
    
        # Информация по профилю github-а
        print("Requesting Github data...")
        github_data = getGithubData(user)
        print("Done.")
    
        print("Saving data...")
        rowJson = {
            'username':             userData['username'],
            'name':                 userData['name'],
            'honor':                userData['honor'],
            'clan':                 userData['clan'],
            'leaderboardPosition':  userData['leaderboardPosition'],
            'skills':               userData['skills'],
            'ranks':                userData['ranks'],
            'codeChallenges':       userData['codeChallenges'],
            'github_data':          github_data,
            'userTotalTaskCount':   userTotalTaskCount,
            'userCompletedTasks':   userCompletedTasks
        }
    
        user_ids_file.write(user + "\n")
        usersFile.write(json.dumps(rowJson) + "\n")
        
        print(user, "done.", len(users) - i, "remaining")
        i += 1
    
    # Закрываем дескрипторы
    usersFile.close()
    tasksFile.close()
    user_ids_file.close()
    task_ids_file.close()