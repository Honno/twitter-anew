# tanew/commands/backup.py

import logging

import tweepy

import tanew.util as util
from .base import Base

DEFAULT_BACKUP_FILENAME = 'backup.txt'


class Backup(Base):

    def run(self, auth):
        if self.options['--verbose']:
            logging.basicConfig(level=logging.INFO)
        log = logging.getLogger(__name__)

        file_arg = self.options['<file>']
        filename = file_arg if file_arg is not None else DEFAULT_BACKUP_FILENAME

        try:
            api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

            user_id_arg = self.options['--user-id']
            user_id = user_id_arg if user_id_arg is not None else api.me().id
            log.info("Storing users followed by user {}".format(user_id))
            friends_ids_cursor = tweepy.Cursor(api.friends_ids, id=user_id)

            friends_ids = []

            for friend_id in friends_ids_cursor.items():
                log.info("Storing user {}".format(friend_id))
                friends_ids.append(friend_id)

            with open(filename, 'w+') as f:
                f.write("List of friend ids followed by {}".format(user_id))
                f.write('\n\n')
                for friend_id in friends_ids:
                    log.info("Writing {} to {}".format(friend_id, filename))
                    f.write(friend_id.__str__())
                    f.write('\n')

            print("All accounts being followed by user {} backed up in {}".format(user_id, filename))

        except tweepy.TweepError as te:
            log.error(util.parse_te(te))
