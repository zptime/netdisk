#!/usr/bin/env bash
for i in `ps -ef|grep netdisk.wsgi|grep -v grep|awk '{print $2}'`
do
kill -9 $i
done
