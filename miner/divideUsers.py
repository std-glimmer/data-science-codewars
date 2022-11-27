
# Функция для считывания списка, сохраненного в файле
def readListFromFile(filePath):
    lst = set()
    file = open(filePath, 'r+')
    for row in file.read().splitlines():
        lst.add(row)
    file.close()
    return lst

mainUserList = readListFromFile("E:\\projects\\data-science-codewars\\miner\\users.txt")
readedUsers = readListFromFile("E:\\projects\\data-science-codewars\\miner\\saved_user_ids.txt")

restUsers = mainUserList - readedUsers

userFile = open("E:\\projects\\data-science-codewars\\miner\\restUsers.txt", 'a+')
for user in restUsers:
    try:
        userFile.write(user + "\n")
        userFile.flush()
    except:
        print("Error")
userFile.close()