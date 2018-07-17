#! /usr/bin/python3.6
def read_input():
    with open('/dev/stdin', mode='rb') as f:
        while True:
            inp = f.read(4)
            if not inp: break
            print('got :' , inp)

read_input()
