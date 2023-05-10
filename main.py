import telebot
import pytube
from bs4 import BeautifulSoup
import requests
from config import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=["video"])
def send_video(message):
    url = message.text.split(" ")[1]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    youtube = pytube.YouTube(url)
    stream = youtube.streams.filter(progressive=True, file_extension="mp4").first()
    stream.download()
    with open(stream.default_filename, "rb") as video:
        bot.send_video(chat_id=message.chat.id, video=video, caption=title)

if __name__ == "__main__":
    print("run bot")
    bot.polling()
    print("exit bot")
