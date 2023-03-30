#!/bin/bash
basepath=$(cd `dirname $0`; pwd)

nohup python3 $basepath/bot/main.py >> $basepath/run.log &
