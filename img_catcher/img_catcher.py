#!/usr/bin/env python

import re, os, sys, urllib2, threading, time

class Catcher(threading.Thread):
  def __init__(self, lock, id, queue):
    super(Catcher, self).__init__(name = id)
    self.lock = lock
    self.queue = queue
  def run(self):
    global index
    while index < len(queue):
      self.lock.acquire()
      self.index = index
      url = queue[index]
      index = index + 1
      self.lock.release()
      try:
        net = urllib2.urlopen(urllib2.Request(url), timeout=60)
      except:
        self.lock.acquire()
        print '404: ' + imgName
        self.lock.release()
        continue
      data = net.read()
      imgName = url.split('/')[-1]
      img = open(imgName, 'wb')
      img.write(data)
      img.close()
      self.lock.acquire()
      global less
      less = less - 1
      print 'less:' + str(less) + ' + ' + imgName
      self.lock.release()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print 'Usage: ' + sys.argv[0].split('\\')[-1] + ' <dataFile> [outputDir]'
    exit()

  queue = []
  index = 0

  re_http = re.compile('http+')
  re_img = re.compile('.*[.](jpg$|png$|gif$).*$')

  dataFile = sys.argv[1]
  if len(sys.argv) >= 3:
    outPath = sys.argv[2]
  else:
    outPath = time.strftime('%Y%m%d', time.gmtime())

  f = open(dataFile)
  for line in f:
    for u in line.split('"'):
      if re_http.search(u) and re_img.search(u):
        queue.append(u)
  f.close()
  less = len(queue)
  print str(less) + ' images'

  if not os.path.exists(outPath) or not os.path.isdir(outPath):
    os.mkdir(outPath)
  os.chdir(outPath)

  lock = threading.Lock()

  for i in range(0, 5):
    Catcher(lock, i, queue).start()

  while less > 0:
    i = i
  print '\ndone'
