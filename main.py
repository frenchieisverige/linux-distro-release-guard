# Standard Libraries
import logging
from datetime import datetime  
from datetime import timedelta
from time import sleep

# Modules
import feed
from distribution import read_wishing_list
from torrent import routine
from parameters import read_arg_parameters, read_config


################################# MAIN ###################################
def main():
    # Start application
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    read_arg_parameters()
    last_modified = 'none'
    url, watchDir,update_frequency = read_config()
    
    logging.info("Starting application with update frequency: %s seconds" % update_frequency)
    
    while True:
        distro_feed = feed.check_updates(url,last_modified)
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
