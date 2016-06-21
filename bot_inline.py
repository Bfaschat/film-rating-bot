# -*- coding: utf-8 -*-


import json
import time # Librería para hacer que el programa que controla el bot no se acabe.

import requests
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.

from key import *

bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.

 
@bot.inline_handler(lambda query: len(query.query) > 3)
def query_text(inline_query):
    url = 'http://www.omdbapi.com/?s=' + inline_query.query
   
    r = requests.get(url)
    json_object = r.json()
    parsed_data = json.dumps(json_object)
    search_list = json.loads(parsed_data)
    
    show_list = []
    
    if search_list["Response"]=='True':
        xd = search_list['Search']
        for result in xd:
            idfilm = result['imdbID']
            picfilm = result['Poster']
            title = result['Title']
            
            if picfilm == 'N/A':
                title = title.replace (" ", "+")
                picfilm = 'https://placeholdit.imgix.net/~text?txtsize=90&bg=ffffff&txt='+title+ '&w=512&h=512&fm=jpg&txttrack=0.jpg'

            url = 'http://www.omdbapi.com/?i=' + idfilm 
           
            r = requests.get(url)
            json_object = r.json()
            parsed_data = json.dumps(json_object)
            lol = json.loads(parsed_data)
            
            capfilm = 'Title: ' + (lol["Title"]) + '\n' +  '\n' + 'IMDb:  ' + (lol["imdbRating"]) + '/10   (' + lol["imdbVotes"] + ' votes)'  + '\n' + 'Metacritic:  ' + (lol["Metascore"])
            result = types.InlineQueryResultPhoto(idfilm,picfilm,picfilm, caption=capfilm)
            show_list.append(result)
    else:
        r = types.InlineQueryResultArticle('1', 'Content not found in IMDb!', types.InputTextMessageContent('Content not found in IMDb!'))
        bot.answer_inline_query(inline_query.id, [r])
    try:
        bot.answer_inline_query(inline_query.id, show_list,cache_time=1)
    except Exception as e:
        print(e)
 
@bot.message_handler(commands=['start']) 
def command_bisi(m): # Definimos una función que resuelva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    bot.send_message(cid, "Just write in any Telegram chat @filmratingbot nameofthefilm to get the search")

bot.polling(none_stop=True)
while True: 
    time.sleep(300) # Hacemos que duerma durante un periodo largo de tiempo para que la CPU no esté trabajando innecesáremente.
