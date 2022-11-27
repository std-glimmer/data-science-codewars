import requests
import json

API_CHALLENGES_REQUEST  = 'https://www.codewars.com/api/v1/code-challenges/{challenge}'

# Функция для считывания списка, сохраненного в файле
def readListFromFile(filePath):
    lst = set()
    file = open(filePath, 'r+')
    for row in file.read().splitlines():
        lst.add(row)
    file.close()
    return lst

ids = readListFromFile("E:\\projects\\data-science-codewars\\miner\\data\\kata_ids.txt")

file = open("E:\\projects\\data-science-codewars\\miner\\data\\katas.json", 'a+')
file.write("[\n")
for id in ids:
    try:
        response = requests.get(API_CHALLENGES_REQUEST.replace("{challenge}", id))
        file.write(json.dumps(response.json()) + ",\n")
        file.flush()
    except:
        print("Error on", id)

file.write("]")
file.close()