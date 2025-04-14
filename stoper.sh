#!/bin/sh
ps ax | grep 4inRserver_test | grep -v grep | awk {'print $1'} | xargs kill

