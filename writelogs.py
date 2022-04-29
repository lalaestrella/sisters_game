class logs:
    # Print a line to terminal and also to logfile
    @staticmethod
    def print(string: object) -> object:
        print(f'{string}')
        with open("templogs.txt", "a") as file:
            file.write(string + "\n")

    # print a line into logs only
    @staticmethod
    def printtologs(string):
        with open("templogs.txt", "a") as file:
            file.write(string + "\n")

    # Read a line from terminal and also add it to logfile
    @staticmethod
    def input():
        string = input()
        with open("templogs.txt", "a") as file:
            file.write(">>>>>> " + string + "\n")
        return string
