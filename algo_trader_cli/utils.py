# import base64

# import json
import logging
import os
from os.path import expanduser
from configparser import ConfigParser

# import jwt
# import requests


# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.asymmetric import rsa, padding
# from cryptography.hazmat.primitives import serialization, hashes

# Local Imports

from algo_trader_cli.sb_core.validator import url_validator


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AlgoTraderCLIConfig:
    __metaclass__ = Singleton
    logger = logging.getLogger("AlgoTraderCLIConfig")

    def __init__(self, sb_type, setup=False, debug=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
        else:
            logging.basicConfig(level=logging.INFO)
        self.verbose = False
        self.username = None
        self.home_dir = os.environ.get("ALGO_CONFIG_HOME", expanduser("~"))
        logging.debug("Home directory: {}".format(self.home_dir))
        self.sb_type = sb_type
        # self.private_key = None
        self.config_dir = "{}/.algo_trade_cli".format(self.home_dir)
        self.env = os.environ.get("ALGO_TRADER_ENV", self.sb_type)
        self.config_file = "algo_trade.cfg"
        self.loaded = False
        self.username = None
        self.api_key = None
        self.api_secret = None
        if self.sb_type == "ZERODHA":
            self.server = "https://api.kite.trade"
        elif sb_type == "UPSTOX":
            self.server = "https://api.upstox.com/"

        if sb_type == "UPSTOX":
            self.upstox_redirect_uri = ""
        if not setup:
            self.config = self.load_config()
            # self.server = self.config.get(self.env, "server")
            # if self.server is None:
            #     print("No Kite server configured in config file '{}'. Please add server = <Kite URL here>".format(
            #         self._config_file()
            #     ))
            #     exit(1)
            self.username = self.config.get(self.env, "username")
            self.api_key = self.config.get(self.env, "api_key")
            self.api_secret = self.config.get(self.env, "api_secret")
            if self.sb_type == "UPSTOX":
                self.upstox_redirect_uri = self.config.get(self.env, "redirect_uri")

        else:
            self.config = ConfigParser()
            self.make_dir()
            file = self._config_file()
            if os.path.isfile(file):
                with open(file, 'r') as f:
                    self.config.read_file(f)
                if self.config.has_section(self.env):
                    self.username = self.get_username()
                    # self.server = self.config.get(self.env, "server")
                    self.api_key = self.config.get(self.env, "api_key")
                    self.api_secret = self.config.get(self.env, "api_secret")
                    if self.sb_type == "UPSTOX":
                        self.upstox_redirect_uri = self.config.get(self.env, "redirect_uri")
                else:
                    self.username = None
                    # self.server = None
                    self.api_key = None
                    self.api_secret = None
                    if self.sb_type == "UPSTOX":
                        self.upstox_redirect_uri = ""

    def setup(self):
        print("Environment: {}".format(self.env))

        username = self.username if self.username is not None else ""
        u_prompt = "Username: [{}] ".format(username) if username != "" else "Username: "
        new_username = input(u_prompt)
        if new_username == "":
            new_username = username

        server = self.server if self.server is not None else ""
        s_prompt = "Server URL: [{}] ".format(self.server) if server != "" else "Server URL: "
        input(s_prompt)
        # if new_server == "":
        #     new_server = server

        api_key = self.api_key if self.api_key is not None else ""
        api_key_prompt = "Api Key: [{}] ".format(api_key) if api_key != "" else "Api Key: "
        new_api_key = input(api_key_prompt)
        if new_api_key == "":
            new_api_key = api_key

        api_secret = self.api_secret if self.api_secret is not None else ""
        api_secret_prompt = "Api Secret: [{}] ".format(api_secret) if api_secret != "" else "Api Secret: "
        new_api_secret = input(api_secret_prompt)
        if new_api_secret == "":
            new_api_secret = api_secret
       
        if self.sb_type == "UPSTOX":
            redirect_uri = self.upstox_redirect_uri
            def func_redirect_uri():
                redirect_uri_prompt = "Redirect URI: [{}] ".format(redirect_uri) if redirect_uri != "" else "Redirect URI: "
                new_redirect_uri_prompt = input(redirect_uri_prompt)
                if new_redirect_uri_prompt == "":
                    new_redirect_uri_prompt = redirect_uri
                else:
                    # validate
                    if not url_validator(new_redirect_uri_prompt):
                        print("Not a valid redirect uri, Please provide redirect uri")
                        return func_redirect_uri()
                return new_redirect_uri_prompt
            new_redirect_uri_prompt = func_redirect_uri()

        if not self.config.has_section(self.env):
            self.config.add_section(self.env)
        # self.config[self.env]['server'] = self.server
        self.config[self.env]['username'] = new_username
        self.config[self.env]['api_key'] = new_api_key
        self.config[self.env]['api_secret'] = new_api_secret

        if self.sb_type == "UPSTOX":
            self.config[self.env]['redirect_uri'] = new_redirect_uri_prompt


        self.make_dir()
        file = self._config_file()
        with open(file, 'w') as f:
            self.config.write(f)
            print("Config file {} updated".format(self._config_file()))

    def _config_file(self):
        return "{}/{}".format(self.config_dir, self.config_file)

    def load_config(self):
        parser = ConfigParser()
        file = self._config_file()
        logging.debug("Config file: {}".format(self._config_file()))
        if os.path.isfile(file):
            parser.read_file(open(file))
        else:
            print("No config file found. Please run algo trader cli setup")
            exit(1)
        return parser

    def get_username(self):
        if self.username is None:
            self.username = self.config.get(self.env, 'username')
        if self.username is None:
            print("Username not configured in config file '{}'. Please add username = <your username>"
                  .format(self._config_file()))
            exit(1)
        return self.username

    def get_api_key(self):
        if self.api_key is None:
            self.api_key = self.config.get(self.env, 'api_key')
        if self.api_key is None:
            print("api_key not configured in config file '{}'. Please add api_key = <your api_key>"
                  .format(self._config_file()))
            exit(1)
        return self.api_key

    def get_api_secret(self):
        if self.api_secret is None:
            self.api_secret = self.config.get(self.env, 'api_secret')
        if self.api_secret is None:
            print("api_secret not configured in config file '{}'. Please add api_secret = <your api_secret>"
                  .format(self._config_file()))
            exit(1)
        return self.api_secret
    
    def get_redirect_uri(self):
        if self.redirect_uri is "":
            self.redirect_uri = self.config.get(self.env, 'redirect_uri')
        if self.redirect_uri is "":
            print("redirect_uri not configured in config file '{}'. Please add redirect_uri = <your redirect_uri>"
                  .format(self._config_file()))
            exit(1)
        return self.redirect_uri

    def keys_existing(self):
        return os.path.isfile("{}/{}".format(self.config_dir, self.config_file))

    def make_dir(self):
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
