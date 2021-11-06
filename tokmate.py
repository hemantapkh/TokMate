import ssl
from aiohttp import web

from src import *
from src.message import sendVideo

#: Configuration for webhook
webhookBaseUrl = f"https://{config['webhookOptions']['webhookHost']}:{config['webhookOptions']['webhookPort']}"
webhookUrlPath = f"/{config['botToken']}/"

app = web.Application()

#: Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

async def extensionHandle(request):
    try:
        data = await request.json()
        url, token = data['url'], data['token']
        
        try:
            chatId = dbSql.getUserFromToken(token)
            
            if chatId:
                sendVideo(url, chatId)
                return web.json_response({'message': 'success'}, status=200)
            
            else:
                return web.json_response({'message': 'invalid token'}, status=401)

        except Exception:
            return web.json_response({'message': 'error while sending video'}, status=400)
    
    except Exception:
        return web.json_response({'message': 'please pass URL and Id'}, status=422)

app.router.add_post('/tokmateApi/', extensionHandle)
app.router.add_post('/{token}/', handle)
    
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