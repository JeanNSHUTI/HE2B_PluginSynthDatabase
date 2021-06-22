from utilities import *


if __name__ == '__main__':

    _command = ""

    # input
    # command = str(input())
    startup()
    while _command.lower() != "exit" and _command.lower() != "q":
        print(">>>>")
        command = input()
        command = command.split(" ", 1)
        _command = command[0]
        if _command.lower() != "exit" and _command.lower() != "q":
            switch(command)
        else:
            print("Good Bye.")
            break
