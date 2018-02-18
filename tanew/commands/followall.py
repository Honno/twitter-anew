import tweepy

from .base import Base

from .backup import DEFAULT_BACKUP_FILENAME

import logging


import tanew.util as util

class FollowAll(Base):
    def run(self, auth):
        if self.options['--verbose']:
            logging.basicConfig(level=logging.INFO)
        log = logging.getLogger(__name__)

        try:
            file_param = self.options['<file>']
            filename = file_param if file_param != None else DEFAULT_BACKUP_FILENAME
            friends_ids = util.read_friends_ids(filename)

            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            
            if len(friends_ids) != 0:

                for friend_id in friends_ids:
                    log.info("Following user {}".format(friend_id))
                    api.create_friendship(friend_id)

                print("All users from {} being followed".format(filename))
            else:
                log.critical("No friend ids in {}".format(filename))

        except tweepy.TweepError as te:
            log.error(util.parse_te(te))

        except FileNotFoundError as fnfe:
            log.error(fnfe)
