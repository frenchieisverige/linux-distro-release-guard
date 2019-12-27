import argparse
import json

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
    """Update the configuration file.

    Args:
        key (str): the key of the parameter to be updated.
        value: (str,int): the new value

    Returns:
        none

    Raises:
        TODO
        IOError: An error fetching the feed.
    """
    with open("./config/config.json", "r") as configFile:
        config = json.load(configFile)
    config[key] = value
    with open("./config/config.json", "w") as configFile:
        json.dump(config, configFile)