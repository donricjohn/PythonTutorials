# newton's search
def newtonsearch():

    x = 10
    h = 0.0000000001
    def f(x):
        return 9 - x*(x-10)

    def df(x):
        return ((9 - (x + h)*((x + h) - 10)) - (9 - x*(x-10)))/h


    for itercept in range(1, 10):
        i = x - f(x)/df(x)
        x = i
    print(x)

newtonsearch()

