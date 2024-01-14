import telebot
import shadowrocket
import openchat
import wangyiyun
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6517716713:AAHJsJB3xiW_SgT2qM0iuNmAIRE9YwBpLIY')

@bot.message_handler(commands=['shadowrocket'])
def send_shadowrocket(message):
    # Get the HTML content from the URL
    html_content = shadowrocket.get_html_content('https://xiaohuojian.link')

    # Extract the account info from the HTML content
    account_data = shadowrocket.extract_account_info(html_content)

    # Create a string to send as a message
    message_to_send = ""
    for account_info, email, password in account_data:
        message_to_send += f"Account Info: {account_info}\nEmail: {email}\nPassword: {password}\n\n"

    # Send the message
    bot.reply_to(message, message_to_send)

@bot.message_handler(commands=['music'])
def send_music(message):
    # Extract the music name from the message text
    music_name = message.text[7:]

    # Use the function in wangyiyun.py to get the music link and name
    music_link, music_name = wangyiyun.get_music_link(music_name)

    # Check if the music link and name are None
    if music_link is None or music_name is None:
        bot.send_message(message.chat.id, "没找到捏")
        return

    # Download the music
    wangyiyun.download_music(music_link,music_name)

    # Send the music file
    audio = open(music_name, 'rb')
    bot.send_audio(message.chat.id, audio)

    # Close the file
    audio.close()

    # Delete the file
    os.remove(music_name)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    response = openchat.chat_with_gpt(message.text)
    bot.reply_to(message, response)

bot.polling()