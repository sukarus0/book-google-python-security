import dis


def my_function():
    i = 0
    while i < 4:
        print("Hello World!\n")
        i = i + 1


dis.dis(my_function)

