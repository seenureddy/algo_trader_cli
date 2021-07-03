# Cli application for Stock Broker Connect API

## User setup

- Create .env file to add environment variables (ENV VARIABLES)

- Install the application local machine
  `python setup.py install`
  or
  `pip install -e .`

## Local developer setup

- Create .env file to add environment variables (ENV VARIABLES)

- Create the virtualenv and activate the virtualenv

- Install the requirements `pip install -r requirements.txt`

- Algo CLI run command `algocli setup -stb [ZERODHA|UPSTOX|FYERS]`
- `algocli setup` will create the `.algo_trade_cli` directory in windows or linux machines. Store the Information as follows:

```
[ZERODHA]
username = XXXXXX
api_key = XXXXXX
api_secret = XXXXXX

[UPSTOX]
username = XXXXXX
api_key = XXXXXX
api_secret = XXXXXX
redirect_uri = http://www.example.com

[FYERS]
username = XXXXXX
api_key = XXXXXX
api_secret = XXXXXX
```

# ENV VARIABLES

-
