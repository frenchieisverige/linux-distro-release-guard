#!/usr/bin/python
import feedparser
import time
import requests
import argparse

url = 'https://distrowatch.com/news/torrents.xml'

""" distro_to_watch = [
    'debian',
    'ubuntu',
    'linuxmint',
    'raspbian',
    'clonezilla',
    'openmediavault',
    'FreeNAS',
    'gparted',
    ] """
distro_to_watch = []
last_modified = 'none'

def get_feed(url, l_m='none'):
    if l_m == 'none':
        print('Get feed with no last_modified')
        return feedparser.parse(url)
    else:
        print('Get feed with last_modified', l_m)
        return feedparser.parse(url, modified=l_m)


def search_distro(feed):
    feed_length = len(feed.entries)
    disto_list = []
    for i in range(feed_length):
        for j in distro_to_watch:
            if j in feed.entries[i].title:
                print("Add",feed.entries[i].title,"to download")
                disto_list.append({"name": feed.entries[i].title, "link": feed.entries[i].link})

    return disto_list

def copy_to_watch_folder(torrentList):
    for j in torrentList:
        myfile = requests.get(j.get("link"), allow_redirects=True)
        path = './torrents/' + j.get("name")
        open(path, 'wb').write(myfile.content) 

def check_updates():
    global last_modified
    print('check_updates', last_modified)
    feed = get_feed(url, l_m=last_modified)

    if feed.status == 304:
        print(feed.debug_message)

    if feed.status == 200:   
        routine(feed)

def routine(feed):
    global last_modified
    last_modified = feed.modified
    torrents = search_distro(feed)
    copy_to_watch_folder(torrents)

# rstrip removes /n lines
def read_wishing_list():
    global distro_to_watch
    distro_to_watch = []
    file = open("./config/distro-list.txt", "r")
    for line in file:
        if line.startswith('#') or line in ['\n', '\r\n']:
            print("Skipping")
            continue
        distro_to_watch.append(line.rstrip())


def main():

    update_rate = 3600
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="show version")
    parser.add_argument("-u", "--update-frequency", help="how often the script should check new releases (in hours)")
    args = parser.parse_args()

    if args.version:
        print("linux-distro-release-guard is in version 1.0")
        exit(0)
    if args.update_frequency:
        update_rate = int(args.update_frequency)*3600


    print('Starting application with update frequency:', update_rate)
    while True:
        read_wishing_list()
        check_updates()
        time.sleep(update_rate)
    
# Main prog
if __name__ == '__main__':
    main()
