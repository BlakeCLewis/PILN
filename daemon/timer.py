#   PiLN: Rassberry Pi electric kiln controller
#
#   Copyright (C) 2017  pvarney     git@github.com:pvarney/PiLN.git
#   Copyright (C) 2018  BlakeCLewis git@github.com:BlakeCLewis/PILN.git
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 3
#   published by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time

def do_every(period,f,*args):
    def g_tick():
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t + count*period - time.time(),0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)

def hello(s):
    print('hello {} ({:.4f})'.format(s,time.time()))
    time.sleep(.3)

do_every(1,hello,'foo')
