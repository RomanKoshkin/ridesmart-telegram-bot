# Ride-sharing bot for Moscow


<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Generic badge](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)
![GitHub](https://img.shields.io/github/license/RomanKoshkin/ema_x_bot)
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

<p float="left">
  <img src="Telegram_logo.svg" width="100" />
  <img src="logo.png" width="150" /> 
</p>


## What is it?

This is a ride-sharing bot for Telegram. If you live in Moscow, Russia, you're in luck, because the bot is already operational and you can share your taxi rides (and the money it takes) with other people planning to take a similar trip at more or less the same time.

## If you are in Moscow
Just search Telegram for RideSmart, type `/start`, and share your rides.

## If you are elsewhere, but want to make ride sharing available in your area

1. Create a bot on [Telegram](https://telegram.org/). To do that, download the Telegram app, go to [@BotFather](https://telegram.me/BotFather) and copy your bot API token into `bot4.py`.
2. Create a free account on [MongoDB](https://www.mongodb.com/) and a database, get the API key and paste it into `bot4.py`. Make sure you white list your DB client's IP address.
3. Edit the hop-on/hop-off locations in `bot4.py`.
4. Run the bot backend `bot4.py`. For the bot to be available at all times, it is best to host the bot on a cloud VM like [PythonAnywhere](https://pythonanywhere.com) or similar.

## Features

- Hop-on/hop-off locations include over 280 metro stations, railway stations, airports and major universities (yes, this should be good for students).
- Hop-on/hop-off locations can be picked from the list or using a pin on Telegram's built-in map.

<p align="center">
  <img src="tg_screen.png" style="width:20%">
</p>

## Telegram commands
- `/start` - starts the bot (only needs to be run once)

## Dependencies

`pip install pymongo==3.10.1 jupyter==1.0.0 numpy==1.20.3 pandas==1.2.4 python-telegram-bot==13.6 requests==2.25.1 beautifulsoup4==4.7.1`

## Development

Want to contribute? Great!

## License

**Free Software, Hell Yeah!**



# make sure you white list the this DB client's IP address at:
# https://cloud.mongodb.com/v2/5ead3348c42d6d5c938d2f75#security/network/whitelist

"""
dependencies:
pip install python-telegram-bot --upgrade
for ip: Just type curl ifconfig.me in the terminal.
python -m pip install pymongo[srv]
"""
