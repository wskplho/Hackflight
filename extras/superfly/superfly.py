#!/usr/bin/env python3
'''
superfly.py : Python script to fly the SuperFly flight controller over wifi

Requires: pygame
          https://github.com/simondlevy/pysticks

Copyright (C) Simon D. Levy 2018

This file is part of Hackflight.

Hackflight is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.
This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http:#www.gnu.org/licenses/>.
'''

SUPERFLY_ADDR = '192.168.4.1'
SUPERFLY_PORT = 80
TIMEOUT_SEC   = 4

from socket import socket
from pysticks import get_controller
from msppg import serialize_SET_RC_NORMAL

# Start the controller
con = get_controller()

# Set up socket connection to SuperFly
sock = socket()
sock.settimeout(TIMEOUT_SEC)
sock.connect((SUPERFLY_ADDR, SUPERFLY_PORT))    
    
while True:

    # Make the controller acquire the next event
    con.update()

    # Put stick demands and aux switch value into a single array,
    # with zero for Aux1 and aux switch for Aux2
    cmds = (con.getThrottle(), con.getRoll(), con.getPitch(), con.getYaw(), 0, con.getAux())

    # Report commands for debugging
    print('Throttle:%+2.2f Roll:%+2.2f Pitch:%+2.2f Yaw:%+2.2f Aux1:%+2.2f Aux2:%+2.2f' % cmds)

    # Send the array of commands to SuperFly
    sock.send(serialize_SET_RC_NORMAL(*cmds))

