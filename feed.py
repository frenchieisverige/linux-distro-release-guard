# Standard libraries
import logging
# Libraries installed via pip
import feedparser


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