import telebot
from pytube import YouTube, Search
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
    youtube = YouTube(url)
    stream = youtube.streams.filter(progressive=True, file_extension="mp4").first()
    stream.download()
    with open(stream.default_filename, "rb") as video:
        bot.send_video(chat_id=message.chat.id, video=video, caption=title)


@bot.message_handler(commands=["search"])
def search_video(message):
    search = message.text.split(' ', 1)[1]
    user_search = Search(search).results[0].video_id
    youtube= YouTube.from_id(video_id=user_search)
    stream = youtube.streams.filter(progressive=True, file_extension="mp4").first()
    stream.download()
    with open(stream.default_filename, "rb") as video:
        bot.send_video(chat_id=message.chat.id, video=video)

if __name__ == "__main__":
    print("run bot")
    bot.polling()
    print("exit bot")
