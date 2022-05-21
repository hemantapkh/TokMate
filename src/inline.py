from src.objs import *
from src.keyboard import *

from urllib.parse import urlparse
from urllib.parse import parse_qs


#: Inline query
@bot.inline_handler(lambda query: len(query.query) >= 0)
def inline(inline_query):
    userLanguage = dbSql.getSetting(inline_query.from_user.id, 'language')

    query = inline_query.query

    if len(query) == 0:
            bot.answer_inline_query(inline_query.id, results=[], is_personal=True, switch_pm_text=language['enterLink'][userLanguage], switch_pm_parameter='inlineQuery')

    else:
        url = query.split('/?')[0]
        url = 'https' + url if not url.startswith('http') else url

        #! Check if the URL is already in the database
        videoId = dbSql.getVideo(url=url)

        fromDb = True
        if not videoId:
            video = getVideo(url)

            if video['success']:
                videoLink = video['link']

                #! Getting the rc parameter from the link
                rc = parse_qs(urlparse(videoLink).query)['rc'][0]

                #! Check if the rc is already in the database
                videoId = dbSql.getVideo(rc=rc)
                if not videoId:
                    videoId = videoLink
                    fromDb = False

        #! If video download is successful
        if videoId:
            #! If the video is already in the database
            if fromDb:
                url = 'https://t.me/tokmatebot?start=getLink_'+ videoId['id']
                result = telebot.types.InlineQueryResultCachedVideo(id=0, video_file_id=videoId['videoId'], title=videoId['description'], description=language['clickToSend'][userLanguage], reply_markup=resultKeyboard(userLanguage, url))
                dbSql.increaseCounter('inlineRequestCached')

            else:
                result = telebot.types.InlineQueryResultVideo(id=0, title=video['description'], video_url=video['link'], mime_type='video/mp4', thumb_url=video['thumbnail'], description=language['clickToSend'][userLanguage], reply_markup=resultKeyboard(userLanguage, url, btn=2))
                dbSql.increaseCounter('inlineRequest')

            bot.answer_inline_query(inline_query.id, [result], cache_time=9999999999)

        #! Error
        else:
            bot.answer_inline_query(inline_query.id, results=[], cache_time=0, is_personal=True, switch_pm_text=language[video['error']][userLanguage].replace('<b>','').replace('</b>',''), switch_pm_parameter='inlineQuery')