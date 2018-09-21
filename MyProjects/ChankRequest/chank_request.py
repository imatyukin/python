#!/usr/bin/env python3

import subprocess
import datetime


fname = 'a.out'
args = ['wget','-O']
location = '/dev/null'
url = '192.168.198.69:8802/hls/CH_R03_1TV/1537516800/1537520400.ts/0r2_655015876r11116.ts'


def run():
    global fname, args, location, url

    while True:
        with subprocess.Popen(['wget','-O', location, url],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              bufsize=1,
                              universal_newlines=True) as p:

            for line in p.stdout:
                if '=' in line:
                    sec = float((((line.split('=')[1]).split('s')[0])).replace(',', '.'))
                    print(sec, end='\n')
                    if (sec > 1):
                        f = open(fname, 'a')
                        time = datetime.datetime.now()
                        f.write(str(time))
                        f.write(' -- ALARM -- Chank Request > 1 sec -- ' + str(sec))
                        f.write('\n')
                        f.close


if __name__ == '__main__':
    run()
