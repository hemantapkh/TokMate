from src.objs import *


#: Buttons for results
def resultKeyboard(userLanguage, url, btn=''):
    markup = telebot.types.InlineKeyboardMarkup()

    btn = language[f'link{btn}Btn'][userLanguage]
    markup.add(telebot.types.InlineKeyboardButton(text=btn, url=url))
    return markup

#: Buttons for links
def linkKeyboard(userLanguage, video):
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton(text=language['openInTTBtn'][userLanguage], url=video['url']))
    markup.add(telebot.types.InlineKeyboardButton(text=language['videoBtn'][userLanguage], url=f"https://t.me/tokmatebot?start=getVideo_{video['id']}"))
    markup.add(telebot.types.InlineKeyboardButton(text=language['joinChannelBtn'][userLanguage], url="https://t.me/h9youtube"), telebot.types.InlineKeyboardButton(text=language['joinDiscussionBtn'][userLanguage], url="https://t.me/h9discussion"))
    markup.add(telebot.types.InlineKeyboardButton(text=language['inlineQueryBtn'][userLanguage], switch_inline_query=''))

    return markup

#: Buttons for social links
def socialKeyboard(userLanguage):
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton(text=language['joinChannelBtn'][userLanguage], url="https://t.me/h9youtube"), telebot.types.InlineKeyboardButton(text=language['joinDiscussionBtn'][userLanguage], url="https://t.me/h9discussion"))

    return markup


#: Button for start command
def startKeyboard(userLanguage):
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton(text=language['inlineQueryBtn'][userLanguage], switch_inline_query_current_chat=''))
    markup.add(telebot.types.InlineKeyboardButton(text=language['inlineQuery2Btn'][userLanguage], switch_inline_query=''))

    return markup
