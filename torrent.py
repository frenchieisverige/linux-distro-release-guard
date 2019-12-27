# Standard libraries
import logging
import requests
# Module
from distribution import search_distro

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