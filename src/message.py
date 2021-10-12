from src.objs import *
from src.keyboard import *
from src.floodControl import floodControl

from urllib.parse import urlparse
from urllib.parse import parse_qs

#: Text handler
@bot.message_handler(content_types=['text'])
def message(message):
    userLanguage  = dbSql.getSetting(message.from_user.id, 'language')

    if floodControl(message, userLanguage):
        #! Start message handler
        if message.text == '/start':
            bot.send_message(message.chat.id, language['greet'][userLanguage].format(message.from_user.first_name), reply_markup=startKeyboard(userLanguage))

        #! Inline query start handler
        elif message.text == '/start inlineQuery':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANEYWV8vnrx1aDQVFFjqajvaCqpwc4AAksNAAIUOzlLPz1-YEAZN1QhBA')

        #! Link message handler
        else:
            url = message.text.split('?')[0]
            url = 'https' + url if not url.startswith('http') else url
            
            #! Check if the URL is already in the database
            videoId = dbSql.getVideo(url=url)
            setUrlVideoId = False
            setRcVideoId = False
            
            if not videoId:
                setUrlVideoId = True
                video = getVideo(message.text)

                if video['success']:
                    videoLink = video['link']

                    #! Getting the rc parameter from the link
                    rc = parse_qs(urlparse(videoLink).query)['rc'][0]

                    #! Check if the rc is already in the database
                    videoId = dbSql.getVideo(rc=rc)
                    if not videoId:
                        videoId = videoLink
                        setRcVideoId = True

            #! If video download is successful
            if videoId:
                bot.send_chat_action(message.chat.id, 'upload_video')

                if setRcVideoId:
                    sent = bot.send_video(message.chat.id, videoId, reply_markup=resultKeyboard(userLanguage, url))
                    dbSql.increaseCounter('messageRequest')
                
                else:
                    sent = bot.send_video(message.chat.id, videoId['videoId'], reply_markup=resultKeyboard(userLanguage, url))
                    dbSql.increaseCounter('messageRequestCached')

                bot.delete_message(message.chat.id, message.id)

                if setRcVideoId:
                    dbSql.setVideo(rc=rc, url=url, videoId=sent.video.file_id, duration=sent.video.duration, description=video['description'])

                elif setUrlVideoId:
                    dbSql.setVideo(url=url, rc=rc, setRc=False)
            
            #! Error
            else:
                bot.send_message(message.chat.id, language[video['error']][userLanguage], reply_markup=socialKeyboard(userLanguage) if video['error'] in ['exception', 'unknownError'] else None)