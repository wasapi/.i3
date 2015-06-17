#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

import imaplib

def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + '\n')
    sys.stdout.flush()

def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    obj = imaplib.IMAP4_SSL('localhost','1143')
    obj.login('ylambert','mot2pa$$e.')
    obj.select()

    while True:
        line, prefix = read_line(), ''
        # ignore comma at start of lines
        if line.startswith(','):
            line, prefix = line[1:], ','

        j = json.loads(line)
        # insert information into the start of the json, but could be anywhere
        # CHANGE THIS LINE TO INSERT SOMETHING ELSE
        unread = len(obj.search(None,'UnSeen')[1][0].split())

        if unread:
            j.insert(0, {
                'full_text' : '%d new emails' % unread, 
                'name' : 'newmail',
                'color' : '#FF0000'})
        # and echo back new encoded json
        print_line(prefix+json.dumps(j))
