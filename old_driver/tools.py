# coding=utf-8
import hashlib
import random


def session_init(datetime):
    salt = 'xiaochengxu'
    datetime = str(datetime)
    hash_object = hashlib.sha1(salt + datetime)
    session = hash_object.hexdigest()
    return session


def random_num_string():
    num = str(int(random.random() * 100000))
    while len(num) < 5:
        num = '0' + num
    return num


def fileLogging(logging_var):
    f = open('logging.txt', 'a+')
    f.write('this step is' + ' : ' + logging_var + '\n')
    f.close()
