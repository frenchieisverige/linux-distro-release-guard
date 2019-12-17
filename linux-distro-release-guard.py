#!/usr/bin/python

# Standard Libraries
from time import sleep
import argparse
import logging
from shutil import copyfile
from datetime import datetime  
from datetime import timedelta  
# Libraries installed via pip
import feedparser
import requests

# Global variables
url = 'https://distrowatch.com/news/torrents.xml'

def get_feed(url, l_m='none'):
    if l_m == 'none':
        logging.info('Get feed with no last_modified')
        return feedparser.parse(url)
    else:
        logging.info("Get feed with last_modified %s" % l_m)
        return feedparser.parse(url, modified=l_m)


def search_distro(feed, wishing_list):
    feed_length = len(feed.entries)
    distro_list = []
    for i in range(feed_length):
        for j in wishing_list:
            if j in feed.entries[i].title:
                logging.info("Add %s to download" % feed.entries[i].title)
                distro_list.append({"name": feed.entries[i].title, "link": feed.entries[i].link})

    return distro_list

def copy_to_watch_folder(torrentList):
    for j in torrentList:
        myfile = requests.get(j.get("link"), allow_redirects=True)
        path = './torrents/' + j.get("name")
        open(path, 'wb').write(myfile.content) 

def check_updates(last_modified):

    logging.info("Check new releases on %s" % last_modified)
    feed = get_feed(url, l_m=last_modified)

    if feed.status == 304:
        logging.info(feed.debug_message)
        return

    #if feed.status == 200:   
    #    routine(feed)
    return feed

def routine(feed):
    wishing_list = read_wishing_list()
    torrents = search_distro(feed, wishing_list)
    copy_to_watch_folder(torrents)

# rstrip removes /n lines
def read_wishing_list():
    distro_to_watch = []
    file = open("./config/distro-list.txt", "r")
    for line in file:
        if line.startswith('#') or line in ['\n', '\r\n']:
            continue
        distro_to_watch.append(line.rstrip())
    return distro_to_watch

def read_arg_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0')
    parser.add_argument("-u", "--update-frequency", help="how often the script should check new releases (in hours)")
    args = parser.parse_args()

    if args.update_frequency:
        return int(args.update_frequency)*3600

def main():

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    update_frequency = read_arg_parameters()
    last_modified = 'none'

    # Start application
    logging.info("Starting application with update frequency: %s seconds" % update_frequency)
    while True:
        distro_feed = check_updates(last_modified)
        last_modified = distro_feed.modified
        routine(distro_feed)

        logging.info("Next check at %s" % (datetime.now() + timedelta(seconds=update_frequency)))
        sleep(update_frequency)
    
# Main prog
if __name__ == '__main__':
    main()
