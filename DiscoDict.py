import discord
from urllib.request import Request, urlopen
import json
import os
import io
from time import sleep

TOKEN = "INSERT DISCORD API TOKEN HERE"
DICT_TOKEN = "INSERT DICTIONARY API TOKEN HERE"

last_def_path = os.path.join(os.path.dirname(__file__), f'last_def.txt')
  
client = discord.Client()


@client.event
async def on_ready():
  print("Bot is ready to party, logged in as {0.user}.".format(client))
 
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  elif message.content.startswith("!dict"):
    try:  
      req_dict = message.content[5:].strip().lower()
      await message.channel.send(f"Defining: '{req_dict}'") ; sleep(1)
      await message.channel.send(f"One moment...") ; sleep(1)
      headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
      req_dict_rep = ""
      for x in req_dict:
        if x == " ":
          req_dict_rep += "+"
        else:
          req_dict_rep += x
      api_url = (f"https://dictionaryapi.com/api/v3/references/sd4/json/{req_dict_rep}?key={DICT_TOKEN}")
      req = Request(url= api_url, headers=headers) 
      html = urlopen(req).read().strip().decode()
      html  = json.loads(html)
      best_match = html[0]
      word_id = best_match["meta"]["id"].title()
      pron_word = repr(best_match["hwi"]["prs"][0]["mw"])
      fl_word = best_match["fl"]
      def_word = best_match["shortdef"][0]
      def_word  = def_word[0].upper() + def_word[1:] + "."
      #meta - id, hwi - prs - [0] - mw, fl, shortdef
      last_def = (f"{word_id} ~ {pron_word} ({fl_word}):\n'{def_word}'")
      with io.open(last_def_path, "w", encoding = "utf-8") as last_def_txt_w:
        last_def_txt_w.write(last_def)
      await message.channel.send(f"```{last_def}```")
    except:
      await message.channel.send(f"I can't find that word, let's see if it exists...") ; sleep(2)
      req_word = message.content[5:].strip().lower()
      lmgtfy_link = (f"https://letmegooglethat.com/?q=is+{req_word}+a+word%3F")
      lmgtfy_link_rep = ""
      for x in lmgtfy_link:
        if x == " ":
          lmgtfy_link_rep += "+"
        else:
          lmgtfy_link_rep += x
      await message.channel.send(lmgtfy_link_rep)
  elif message.content.startswith("!last def"):
    with io.open(last_def_path, "r", encoding = "utf-8") as last_def_text_r:
      read_ld = last_def_text_r.read() ; sleep(2)
      await message.channel.send(f"```{read_ld}```")  
  else:
    return

client.run(TOKEN)