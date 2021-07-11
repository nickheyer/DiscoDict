import discord
from urllib.request import Request, urlopen
import json
import os
import io
from time import sleep

TOKEN = "ENTER TOKEN PROVIDED BY DISCORD API"
DICT_TOKEN = "ENTER TOKEN PROVIDED BY DICTIONARY API"

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
          req_dict_rep += "-"
        else:
          req_dict_rep += x
      api_url = (f"https://dictionaryapi.com/api/v3/references/sd4/json/{req_dict_rep}?key={DICT_TOKEN}")
      req = Request(url= api_url, headers=headers) 
      html = urlopen(req).read().strip().decode()
      html  = json.loads(html)
      isdef = False
      for z in html:
        if str(type(z)) != "<class 'str'>":
          isdef = True
      alt_str = ""
      if isdef == False:
        count = 1
        for ab in html:
          alt_str += (f"{count}. {ab[0].upper()}{ab[1:]}\n")
          count += 1     
        await message.channel.send(f"Definition not available, try one of these similar words: ```{alt_str}```")
        return  
      last_def_list = ""
      count = 1
      for x in html:
        word_id = x["meta"]["id"].title()
        try:  
          pron_word = repr(x["hwi"]["prs"][0]["mw"])
        except:
          pron_word = (f"*{word_id}*")
        try:
          fl_word = x["fl"]
        except:
          fl_word = "N/A"
        def_word = str(x["shortdef"]).strip("[,]")
        #meta - id, hwi - prs - [0] - mw, fl, shortdef
        if len(html) > 1:
          last_def_list += (f"{count}. {word_id} ~ {pron_word} ({fl_word}):\n{def_word}\n\n")
          count += 1
        else:
          last_def_list += (f"  {word_id} ~ {pron_word} ({fl_word}):\n{def_word}\n\n")
      with io.open(last_def_path, "w", encoding = "utf-8") as last_def_txt_w:
        last_def_txt_w.write(last_def_list)
      await message.channel.send(f"```{last_def_list}```")
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