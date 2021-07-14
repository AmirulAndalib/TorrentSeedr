from src.objs import *
from src.functions.urlEncode import urlEncode
from src.functions.floodControl import floodControl
from src.functions.exceptions import exceptions, noAccount

#: Get download link of torrents
@bot.message_handler(func=lambda message: message.text and message.text[:9] == '/getLink_')
def getLink(message):
    userId = message.from_user.id
    userLanguage = dbSql.getSetting(userId, 'language')

    if floodControl(message, userLanguage):
        ac = dbSql.getDefaultAc(userId)

        #! If user has an account
        if ac:
            id = message.text[9:]
            account = Seedr(cookie=ac['cookie'])

            sent = bot.send_message(message.chat.id, language['fetchingLink'][userLanguage])
            response = account.createArchive(id).json()

            #! If download link found
            if 'archive_url' in response:
                encodedUrl = urlEncode(response['archive_url'])
                text = f"🔗 <code>{encodedUrl}</code>\n\n<b>🔥via @TorrentSeedrBot</b>"

                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text=language['openInBrowser'][userLanguage], url=encodedUrl))

                bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=sent.id, reply_markup=markup)
            
            else:
                exceptions(message, response, userLanguage)
        
        #! If no accounts
        else:
            noAccount(message, userLanguage)