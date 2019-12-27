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
