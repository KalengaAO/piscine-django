def print_number(filename):
    with open(filename, "r") as file:
        content = file.read()
        numbers = content.replace(","," ").split(" ")
        for number in numbers:
            print(number)

if __name__ == "__main__":
    print_number("numbers.txt")