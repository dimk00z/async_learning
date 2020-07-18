from inspect import getgeneratorstate


def coroutine(func):
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return inner


def subgen():
    x = 'Ready to accept message'
    message = yield x
    print('Subgen received:', message)


@coroutine
def average():
    count = 0
    summ = 0
    average = None
    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
            break
        else:
            count += 1
            summ += x
            average = round(summ/count, 2)
    return average
