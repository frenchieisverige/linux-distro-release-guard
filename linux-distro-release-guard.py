#!/usr/bin/python3

# Standard Libraries
import argparse
import logging
import configparser
from shutil import copyfile
from datetime import datetime  
from datetime import timedelta
from time import sleep  
# Libraries installed via pip
import feedparser
import requests

############################## XML Feed ##################################
def get_feed(url, l_m='none'):
    if l_m == 'none':
        logging.info('Get xml feed with no last_modified')
        return feedparser.parse(url)
    else:
        logging.info("Get xml feed with last_modified %s" % l_m)
        return feedparser.parse(url, modified=l_m)

def check_updates(url, last_modified):
    logging.info("Check new releases on %s" % last_modified)
    feed = get_feed(url, l_m=last_modified)

    if feed.status == 200:   
        return feed
    elif feed.status == 301:
        logging.warning("Redirected premanently to %s" %feed.href)
        return
    elif feed.status == 304:
        logging.info(feed.debug_message)
        return
    elif feed.status == 401:
        logging.error("Feed does not exist anymore")
        exit(1)
    else:
        logging.warning("Feed does not exist anymore")


############################# Distribution ###############################
def search_distro(feed, wishing_list):
    distro_list = []
    for i in range(len(feed.entries)):
        for j in wishing_list:  
            if isinstance(j, list):
                if all(s in feed.entries[i].title for s in j):
                    distro_list.append({"name": feed.entries[i].title, "link": feed.entries[i].link})
    return distro_list

# rstrip removes /n lines
def read_wishing_list():
    distro_to_watch = []
    file = open("./config/distro-list.txt", "r")
    for line in file:
        if "-" in line:
            distro_to_watch.append(line.rstrip().split("-"))
        elif line.startswith('#') or line in ['\n', '\r\n']:
            continue
        else:
            distro_to_watch.append([line.rstrip()])
    return distro_to_watch


############################### Torrent ##################################
def add_to_watch_folder(torrentList, watchDir):
    for j in torrentList:
        myfile = requests.get(j.get("link"), allow_redirects=True)
        path = watchDir + j.get("name")
        open(path, 'wb').write(myfile.content)
        logging.info("Add %s to download" % j.get("name")) 

def routine(feed, wishing_list, watchDir):
    torrents = search_distro(feed, wishing_list)
    add_to_watch_folder(torrents, watchDir)


############################# Read Config ################################
def read_arg_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0')
    parser.add_argument("-u", "--update-frequency", help="how often the script should check new releases (in hours)")
    args = parser.parse_args()

    if args.update_frequency:
        return int(args.update_frequency)*3600

def read_config_ini():
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    
    url = config['distrowatch.com']['url']
    watchDir = config['bitTorrentClient']['watchDir']

    return url, watchDir


################################# MAIN ###################################
def main():
    # Start application
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    update_frequency = read_arg_parameters()
    last_modified = 'none'
    url, watchDir = read_config_ini()
    
    logging.info("Starting application with update frequency: %s seconds" % update_frequency)
    
    while True:
        distro_feed = check_updates(url,last_modified)
        wishing_list = read_wishing_list()
        routine(distro_feed, wishing_list, watchDir)
        # Update last_modified
        last_modified = distro_feed.modified
        logging.info("Next check at %s" % (datetime.now() + timedelta(seconds=update_frequency)))
        sleep(update_frequency)
    
# Main prog
if __name__ == '__main__':
    main()
