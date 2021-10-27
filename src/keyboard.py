from src.objs import *

#: Buttons for results
def resultKeyboard(userLanguage, link, inline=False):
    markup = telebot.types.InlineKeyboardMarkup()

    markup.add(telebot.types.InlineKeyboardButton(text=language['linkBtn'][userLanguage], url=link), telebot.types.InlineKeyboardButton(text=language['joinChannelBtn'][userLanguage], url="https://t.me/h9youtube"))
    
    if not inline:
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