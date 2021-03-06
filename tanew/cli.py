"""
tanew

Usage:
  tanew status
  tanew linkaccount
  tanew createlist [<file>] [-v] [--list-name=<name>] [--list-mode=<mode>]
  tanew addtolist <slug> [-v] [<file>]
  tanew backup [-v] [<file>] [--user-id=<id>]
  tanew unfollowall [-v]
  tanew followall <file> [-v]
  tanew -h | --help  
  tanew --version  

Options:
  -v --verbose
  -h --hel
  --version
"""

import json
import logging
from inspect import getmembers, isclass

import tweepy
from docopt import docopt

import tanew.util as util
from tanew.__init__ import __version__ as VERSION


def main():
    log = logging.getLogger(__name__)

    try:
        app_file = open('app.json')

        app = json.load(app_file)
        key = app['key']
        secret = app['secret']
        auth = tweepy.OAuthHandler(key, secret)

        try:
            access_tokens_file = open('access_tokens.json')
            access_tokens = json.load(access_tokens_file)

            token = access_tokens['token']
            token_secret = access_tokens['token_secret']

            auth.set_access_token(token, token_secret)

        except FileNotFoundError:
            pass

        import tanew.commands as commands
        options = docopt(__doc__, version=VERSION)

        for k, v in options.items():
            if hasattr(commands, k) and v:
                module = getattr(commands, k)
                commands = getmembers(module, isclass)
                command = [command[1] for command in commands if command[0] != 'Base'][0]
                command = command(options)
                command.run(auth)

    except FileNotFoundError as fnfe:
        log.error(fnfe)
        print("No application (app.json) linked to application")
    except json.decoder.JSONDecodeError as jde:
        log.error(jde)
    except KeyError as ke:
        log.error(ke)
    except tweepy.TweepError as te:
        log.error(util.parse_te(te))
        if te.api_code == 32:
            print("The application pointed to in app.json does not exist")
