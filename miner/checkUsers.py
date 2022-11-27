import os
import json

usernames = set()

dir = "E:\\projects\\data-science-codewars\\miner\\users\\"
for filename in os.listdir(dir):
   with open(os.path.join(dir, filename), 'r') as file:
      user = json.load(file)
      usernames.add(user["username"])

print(len(usernames))