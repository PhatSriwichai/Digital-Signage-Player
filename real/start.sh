#!/bin/sh

cd /
cd home/pi/Digital-Signage-Player/real
python main.py
cd /
unclutter -display :0 -noevents -grab
