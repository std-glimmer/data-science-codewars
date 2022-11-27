import get_usernames as gu

def startMiningUsernames():
    usernames = set()

    i = 0
    while(i < 550):
        usernames = usernames | gu.getUsernamesFromKataList()
        print("Iteration ", i, ": ", len(usernames))
        i = i + 1

    print("Found ", len(usernames), " users")

    leaders = gu.getLeadernames()

    print("Found ", len(leaders), " leaders")

    usernames = usernames | leaders

    print("In total ", len(usernames), " unique users")

    print("Saving...")
    userFile = open("E:\\projects\\data-science-codewars\\miner\\data\\users.txt", 'a+')
    for user in usernames:
        try:
            userFile.write(user + "\n")
            userFile.flush()
        except:
            print("Error")
    userFile.close()
    print("Saved")

startMiningUsernames()