#!/bin/bash

cd colorado-snow-report
python harvest.py
killall chrome
