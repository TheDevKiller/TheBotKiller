#!/bin/bash
echo $1
nohup python3 -u main.py reboot $1 > /tmp/thebotlogs 2>&1 &