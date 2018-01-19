import multiprocessing 
from multiprocessing import pool 
print("cpu count: ", multiprocessing.pool.cpu_count())

import os, time

# g_cnt is not shared with each worker
g_cnt = 4
def test_process_with_global_variable():
  def worker(idx, in_data, out_data):
    global g_cnt
    g_cnt += idx 
    time.sleep(1 - 0.1*idx) 
    # print("worker", idx, g_cnt, in_data)
    out_data.append(g_cnt)

  global g_cnt
  manager = multiprocessing.Manager()
  results = manager.list()
  for i in range(5):
    # input data is a string that is not shared, output a list that is sharef
    p = multiprocessing.Process(target=worker, args=(i, "in_data", results) )
    p.start()
    p.join()
  print("g_cnt: ", g_cnt)
  #time.sleep(2)
#you can sleep for some time if you decide to leave out join
  for r in results:
    print r

# show several processes run in parallel by pool of processes
# does not work yet
class XY():
  def __init__(self, x, y):
    self.x = x
    self.y = y

# g_v is not reliable in this case
g_v = 4
g_lock = multiprocessing.Lock()
def square(d):
  # print 'module name:', __name__
  # if hasattr(os, 'getppid'): 
  #    print 'parent process:', os.getppid()
  #  print 'process id:', os.getpid()
  global g_v
  #with g_lock: 
    #print(g_v)
  g_v += 1
  print ("g_v",)

  return d.x*d.x + d.y

def test_process_pool_map():
  pool = multiprocessing.Pool(processes=multiprocessing.pool.cpu_count())    
  print('Starting run at ' + time.strftime('%Y-%m-%d-%H:%M:%S', time.gmtime()))
  tot = 0
  iter_cnt = 10
  proc_cnt = 16 
  for j in xrange(iter_cnt):
    dl = [XY(1.1111113+i,2.133+j) for i in xrange(proc_cnt)]
    sqr = pool.map(square, dl) 
    tot += sum(sqr) 
  print(tot)
  print('Ending run at ' + time.strftime('%Y-%m-%d-%H:%M:%S', time.gmtime()))

def test_shared_class():

  class SharedClass():
    def __init__(self):
      self.queue = multiprocessing.Queue()
      self.lock =  multiprocessing.Lock()
      self.process_cnt = 2
      self.data = 5.1111
 
    def _process(self, idx):
      max_cnt = 20
      cnt = 0
      while cnt < max_cnt:
        with self.lock:
          s = "{} + {}".format(idx, cnt)
          self.queue.put([s, self.data])
        cnt += 1
 
    def run(self):
      pool = []
      for i in range(self.process_cnt):
        self.data += i
        p = multiprocessing.Process(target=self._process, args=(i,) )
        p.start()
        pool.append(p)

      for p in pool:
        p.join()

      while not self.queue.empty():
        d = self.queue.get()
        print(d)

  s = SharedClass()
  s.run()

# send back message to parent by pipe 
def test_shared_by_pipe():
  def send_by_pipe(conn):
    conn.send([42, None, 'hello'])
    conn.close()

  parent_conn, child_conn = multiprocessing.Pipe()
  p = multiprocessing.Process(target=send_by_pipe, args=(child_conn,))
  p.start()
  print parent_conn.recv() 
  p.join() 

# synchronization among processes
def test_locked_print():
  def locked_print(lock, i):
    #with lock: 
    print('hello world', i)
    print('hello world', i+100)
    time.sleep(0.1) 
    print('hello world', i+200)
    print('hello world', i+300)

  l = multiprocessing.Lock()
  pool = []
  for i in range(50):
    p = multiprocessing.Process(target=locked_print, args=(l, i) )
    pool.append(p)
    p.start()
   
  for p in pool: 
    p.join()

# # python documentation have very good examples for addtional features
#test_process_pool_map()
test_locked_print()
# test_shared_by_pipe()
#test_process_with_global_variable()
# test_shared_class()
