#!/usr/bin/python3

############################## Imports ###################################
# Standard Libraries
import argparse
import logging
import json  
from shutil import copyfile
from datetime import datetime  
from datetime import timedelta
from time import sleep
# Libraries installed via pip
import feedparser
import requests

############################## XML Feed ##################################
def get_feed(url, last_modified='none'):
    """Retrieves the "Latest torrents for source software releases", in other
        words, the latest linux distribution releases.

    Args:
        url (str): A URL where the feed should be fetch of.
        last_modified (str): A date telling when the last 
            modification in the feed has been performed.
            The first time last_modified is unknown.

    Returns:
        A dict (feedparser.FeedParserDict) containing feed information as
        well as the last releases. 

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    if last_modified == 'none':
        logging.info('Get xml feed with no last_modified')
        return feedparser.parse(url)
    else:
        logging.info("Get xml feed with last_modified %s" % last_modified)
        return feedparser.parse(url, modified=last_modified)


def check_updates(url, last_modified):
    """Check if the feed has been updated given a date. Inform as well the 
        status of the current feed.

    Args:
        url (str): A URL where the feed should be fetch of.
        last_modified (str): A date telling when the last 
            modification in the feed has been performed.
            The first time last_modified is unknown.

    Returns:
        A dict (feedparser.FeedParserDict) containing feed information as
        well as the last releases. 

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    logging.info("Check new releases on %s" % last_modified)
    feed = get_feed(url, last_modified=last_modified)

    if feed.status == 200:   
        return feed
    elif feed.status == 301:
        logging.warning("Redirected premanently to %s" %feed.href)
    elif feed.status == 304:
        logging.info(feed.debug_message)
    elif feed.status == 401:
        logging.error("Feed does not exist anymore")
        exit(1)
    else:
        logging.warning("Feed does not exist anymore")


############################# Distribution ###############################
def search_distro(feed, wishing_list):
    """Search if the distribution on the wishing list is in the current
        feed.

    Args:
        feed (dict): A feed which has been previously fetched.
        wishing_list (list): An array containing the wishedlinux distributions
            of the user.

    Returns:
        A list containing a dict per linux distribution. The dict is containing
        the link and name of the distribution. 

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    distro_list = []
    for i in range(len(feed.entries)):
        for j in wishing_list:  
            if isinstance(j, list):
                if all(s in feed.entries[i].title for s in j):
                    distro_list.append({"name": feed.entries[i].title, "link": feed.entries[i].link})
    return distro_list


def read_wishing_list():
    """Read the wishing list from a txt file stored locally.

    Args:
        none

    Returns:
        A list containing a nested list per linux distribution. 
        This nested list contains the name and the flavour of 
        the linux distribution.

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    distro_to_watch = []
    file = open("./config/distro-list.txt", "r")
    for line in file:
        # rstrip: removes /n lines
        if "-" in line:
            distro_to_watch.append(line.rstrip().split("-"))
        elif line.startswith('#') or line in ['\n', '\r\n']:
            continue
        else:
            distro_to_watch.append([line.rstrip()])
    return distro_to_watch


############################### Torrent ##################################
def add_to_watch_folder(torrentList, watchDir):
    """Download the torrent file and copy it to the watch folder of the 
        bitTorrent client.

    Args:
        torrentList (list): A list contaning link and name of the linux
            distribution
        watchDir (str): A path to the watch folder of the bitTorrent Client

    Returns:
        none

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    for j in torrentList:
        myfile = requests.get(j.get("link"), allow_redirects=True)
        path = watchDir + j.get("name")
        open(path, 'wb').write(myfile.content)
        logging.info("Add %s to download" % j.get("name")) 

def routine(feed, wishing_list, watchDir):
    """ A routine that is executed when a new distribution has been found.

    Args:
        feed (dict): A feed which has been previously fetched.
        wishing_list (list): An array containing the wishedlinux distributions
            of the user.
        watchDir (str): A path to the watch folder of the bitTorrent Client

    Returns:
        None

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    torrents = search_distro(feed, wishing_list)
    add_to_watch_folder(torrents, watchDir)


############################# Read Config ################################
def read_arg_parameters():
    """Read arguments given as sysargs.

    Args:
        none

    Returns:
        A int containing the update frequency.

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    description= ('Watch automatically your favourite Linux distribution' 
                    'release and send it to your BitTorrent client in order' 
                    'to download it!')
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0')
    parser.add_argument("-u", "--update-frequency", help="how often the script should check new releases (in hours)")
    parser.add_argument("-s", "--site", help="the url where the feed should be pulled from")
    parser.add_argument("-d", "--directory", help="the watch directory of the bitTorrent client")
    args = parser.parse_args()

    if args.update_frequency:
        update_config("updateFrequency", int(args.update_frequency))
    if args.site:
        update_config("url", args.site)
    if args.directory:
        update_config("watchDir", args.directory)

def read_config():
    """Read the configuration file from the dik.

    Args:
        none

    Returns:
        A tuple (str, str) containing the url and the watch directory of the 
        bitTorrent Client.

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    with open('./config/config.json', 'r') as configFile:
        config = json.load(configFile)

    url = config['url']
    watchDir = config['watchDir']
    update_frequency = config['updateFrequency']*3600
    return url, watchDir, update_frequency

def update_config(key, value):
    with open("./config/config.json", "r") as configFile:
        config = json.load(configFile)
    config[key] = value
    with open("./config/config.json", "w") as configFile:
        json.dump(config, configFile)


################################# MAIN ###################################
def main():
    # Start application
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    read_arg_parameters()
    last_modified = 'none'
    url, watchDir,update_frequency = read_config()
    
    logging.info("Starting application with update frequency: %s seconds" % update_frequency)
    
    while True:
        distro_feed = check_updates(url,last_modified)
        wishing_list = read_wishing_list()
        if distro_feed:
            routine(distro_feed, wishing_list, watchDir)
            # Update last_modified
            last_modified = distro_feed.modified
        logging.info("Next check at %s" % (datetime.now() + timedelta(seconds=update_frequency)))
        sleep(update_frequency)
    
# Main prog
if __name__ == '__main__':
    main()
