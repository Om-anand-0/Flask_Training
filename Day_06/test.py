def sistec(func):
    def wrapper(*args):
        print("Hello")
        return func(*args)
    return wrapper


@sistec
def func(name):
    return name

name = "tillu"
print(func(name))  