from src.objs import *

#: Main reply keyboard
def mainReplyKeyboard(userId, userLanguage):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    button1 = telebot.types.KeyboardButton(text=language['fileManagerBtn'][userLanguage])
    button2 = telebot.types.KeyboardButton(text=language['activeTorrentsBtn'][userLanguage])
    button3 = telebot.types.KeyboardButton(text=language['wishlistBtn'][userLanguage])
    button4 = telebot.types.KeyboardButton(text=language['accountBtn'][userLanguage])
    button5 = telebot.types.KeyboardButton(text=language['settingsBtn'][userLanguage])
    button6 = telebot.types.KeyboardButton(text=language['helpBtn'][userLanguage])
    button7 = telebot.types.KeyboardButton(text=language['supportBtn'][userLanguage])
    button9 = telebot.types.KeyboardButton(text=language['addAccountBtn'][userLanguage])
    button10 = telebot.types.KeyboardButton(text=language['switchBtn'][userLanguage])
    
    account = dbSql.getAccounts(userId)

    #! If user has no account
    if not account:
        keyboard.row(button9)
        keyboard.row(button5, button6, button7)
    
    else:
        keyboard.row(button1, button2)
        keyboard.row(button10, button3, button4) if len(account) > 1 else keyboard.row(button3, button4)
        keyboard.row(button5, button6, button7)

    return keyboard