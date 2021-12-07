import json
from os import path

import telebot
from models import dbQuery
from tikTokScraper import getVideo, tikTokDomains

#! Finding the absolute path of the config file
scriptPath = path.abspath(__file__)
dirPath = path.dirname(scriptPath)
configPath = path.join(dirPath,'config.json')

config = json.load(open(configPath))
bot = telebot.TeleBot(config['botToken'], parse_mode='HTML')
language = json.load(open(config['language']))

dbSql = dbQuery(config['database'], config['videoDatabase'])