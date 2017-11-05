#!/usr/bin/env python3
# Ping a list of hosts with threads for increase speed
# use standard linux /bin/ping utility
from threading import Thread
import subprocess
import queue
import re

# some global vars
num_threads = 15
ips_q = queue.Queue()
out_q = queue.Queue()

# build IP array
ips = []
for i in range(129,158):
  ips.append("10.251.78."+str(i))

# thread code: wraps system Ping command
def thread_pinger(i, q):
  """ Pings hosts in queue """

  while True:
    # get an IP item form queue
    ip = q.get()
    # Ping it
    args=['/bin/ping', '-c', '1', '-W', '1', str(ip)]
    p_ping = subprocess.Popen(args,
                              shell=False,
                              stdout=subprocess.PIPE)
    # save Ping stdout
    p_ping_out = p_ping.communicate()[0]

    if (p_ping.wait() == 0):
      # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
      search = re.search(r'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms',
                         p_ping_out.decode('utf-8'), re.M|re.I)
      ping_rtt = search.group(2)
      out_q.put("OK " + str(ip) + " rtt= " + ping_rtt)

    # update queue: this IP is processed
    q.task_done()

# start the thread pool
for i in range(num_threads):
  worker = Thread(target=thread_pinger, args=(i, ips_q))
  worker.setDaemon(True)
  worker.start()

# fill queue
for ip in ips:
  ips_q.put(ip)

# wait until worker threads are done to exit
ips_q.join()

# print result
while True:
  try:
    msg = out_q.get_nowait()
  except queue.Empty:
    break
  print(msg)