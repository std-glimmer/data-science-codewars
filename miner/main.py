import sys
import os
import mining
from time import sleep

TARGET_DIR = ""

# Вечный цикл
# Программа рассчитана на потенциальные падения и в случае перезапуска продолжит работу в штатном режиме
def run_forever():
    try:
        while True:
            mining.start(TARGET_DIR)
            sleep(10)
            raise Exception("Error simulated!")
    except Exception:
        print("Something crashed your program. Let's restart it")
        run_forever()
        handle_exception()

def handle_exception():
    # code here
    pass

# python3 main "../storage"
def main():
    if __name__ == "__main__":
        if (len(sys.argv) <= 1):
            print("Need to set target dir path.")
        else:
            dir = sys.argv[1]
            if (os.path.isdir(dir)):
                TARGET_DIR = dir
                run_forever()
            else:
                print("Invalid target dir")

main()