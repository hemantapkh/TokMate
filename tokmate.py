import ssl
from aiohttp import web

from src import *
from src.message import sendVideo

#: Configuration for webhook
webhookBaseUrl = f"https://{config['webhookOptions']['webhookHost']}:{config['webhookOptions']['webhookPort']}"
webhookUrlPath = f"/{config['botToken']}/"

app = web.Application()


#: Process webhook calls
async def botHandler(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)


async def apiHandler(request):
    try:
        data = await request.json()
        url, token = data['url'], data['token']

        try:
            chatId = dbSql.getUserFromToken(token)

            if chatId:
                sendVideo(url, chatId)
                return web.json_response({'message': 'success'}, status=200, headers={'Access-Control-Allow-Origin': 'https://www.tiktok.com'})

            else:
                return web.json_response({'message': 'invalid token'}, status=401, headers={'Access-Control-Allow-Origin': 'https://www.tiktok.com'})

        except Exception:
            return web.json_response({'message': 'error while sending video'}, status=400, headers={'Access-Control-Allow-Origin': 'https://www.tiktok.com'})

    except Exception:
        return web.json_response({'message': 'please pass URL and Token'}, status=422, headers={'Access-Control-Allow-Origin': 'https://www.tiktok.com'})


async def getApiHandler(request):
    return web.Response(text='Welcome to the TokMate API !!')


def isSubscribed(userId):
    try:
        status = bot.get_chat_member('-1001270853324', userId)
        if status.status == 'left':
            return False

        else:
            return True

    except Exception:
        return False


async def isSubscribedHandler(request):
    userId = request.rel_url.query['userid'] if 'userid' in request.rel_url.query else None

    if userId:
        return web.json_response({'subscribed': isSubscribed(userId)}, status=200)

    else:
        return web.json_response({'message': 'please pass userid'}, status=422)


app.router.add_post('/tokmateApi/', apiHandler)
app.router.add_get('/tokmateApi/', getApiHandler)
app.router.add_get('/isSubscribed', isSubscribedHandler)
app.router.add_post('/{token}/', botHandler)


#: Polling Bot
if config['connectionType'] == 'polling':
    #! Remove previous webhook if exists
    bot.remove_webhook()
    bot.polling(none_stop=True)


#: Webhook Bot
elif config['connectionType'] == 'webhook':
    #! Set webhook
    bot.set_webhook(url=webhookBaseUrl + webhookUrlPath,
                    certificate=open(config['webhookOptions']['sslCertificate'], 'r'))

    #! Build ssl context
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(config['webhookOptions']['sslCertificate'], config['webhookOptions']['sslPrivatekey'])

    #! Start aiohttp server
    web.run_app(
        app,
        host=config['webhookOptions']['webhookListen'],
        port=config['webhookOptions']['webhookPort'],
        ssl_context=context,
    )
