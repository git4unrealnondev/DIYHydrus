'''
A tempory file for me to check stuffs.
'''
import time
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count


def power(x, n):

    time.sleep(1)

    print("x", x)
    print("n", n)

def main():

    start = timer()

    print(f'starting computations on {cpu_count()} cores')

    values = \
        print(type(values), len(values))
    for each in values:
        print(each)

    with Pool() as pool:
        res = pool.starmap(power, values)
        print(res)

    end = timer()
    print(f'elapsed time: {end - start}')


if __name__ == '__main__':
    main()
