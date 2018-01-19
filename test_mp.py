import multiprocessing as mp
from multiprocessing import pool 

chunks = [['a', 'b', 'c'], ['d','e','f'], ['g','h','i'], ['j','k','l']]

def update_(letters, numbers):
    #letters is a list of 3
    dic = {}
    for i, x in enumerate(letters):
        dic[x] = 10 - numbers[i]
    return dic

def update_vectors_process():
    pool = mp.Pool(processes=4)
    n = [4,2,8]
    results = list(pool.map(lambda x: update_(x, n), chunks))
    print(results)

def update_vectors():
    n = [4,2,8]
    results = list(map(lambda x: update_(x,n), chunks))
    print(results)
update_vectors_process()