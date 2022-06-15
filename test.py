def prettfy(func):
    def inner():
        print('Decorated')
        func()
    return inner


@prettfy
def ordinary():
    print('I am ordinary')

ordinary()

# expression for item in iterable if condition it returns a list

filter_even = [x for x in range(0, 10) if x%2==0]
print(filter_even)

# key, value for(key, value) in iterable if condition

double = {n: n*n for n in range(1, 10)}
print(double)

i = iter(filter_even)
print(next(i))
print(next(i))


def square(s):
    for item in range(1, s+1):
        yield item*item


a = square(3)

print(next(a))
print(next(a))
print(next(a))


class Dog:
    def __init__(self, name, color):
        print(name, color)


d = Dog('HUSHH', 'white')


class pup(Dog):
    def __init__(self):
        print("Dogs babies are called pups")
        super().__init__("Pari", "Brown")


p1 = pup()


