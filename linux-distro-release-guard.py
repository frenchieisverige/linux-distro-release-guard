#!/usr/bin/python
import feedparser
import time
import requests

url = 'https://distrowatch.com/news/torrents.xml'

distro_to_watch = [
    'debian',
    'ubuntu',
    'linuxmint',
    'raspbian',
    'clonezilla',
    'openmediavault',
    'FreeNAS',
    'gparted',
    ]

last_modified = 'none'

def get_feed(url, l_m='none'):
    if l_m == 'none':
        print('Get feed with no last_modified')
        return feedparser.parse(url)
    else:
        print('Get feed with last_modified', l_m)
        return feedparser.parse(url, modified=l_m)


def search_distro(feed):
    array_length = len(feed.entries)
    disto_list = []
    for i in range(array_length):
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
    #copy_to_watch_folder(torrents)

def read_update_frequency():
    f = open("./config/config.txt", "r")
    return int(f.readline())


def main():
    update_time = read_update_frequency()
    print('Starting application with update frequency:', update_time)
    while True:
        check_updates()
        time.sleep(update_time)
    
# Main prog
if __name__ == '__main__':
    main()
