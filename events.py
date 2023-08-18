#pylint:disable=E0001
from datetime import datetime
from fbchat import Client, Message, ThreadType
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time 
#import get_commandz as namez
import requests
import textwrap
import urllib.parse
import json
#from agent import main
def get_gpt_response(q):
    prompt = q.replace("gpt ","")
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://gptgo.ai/?q={encoded_prompt}&hl=en&hlgpt=en#gsc.tab=0&gsc.q={encoded_prompt}&gsc.page=1"

    response = requests.get(url)
    data = response.text

    token = data.split('renderUI("')[1].split('")')[0]

    token_url = f"https://gptgo.ai/action_ai_gpt.php?token={token}"

    response = requests.get(token_url)
    resp = response.text

    lines = resp.split("\n")
    content = ""

    for line in lines:
        if "content" in line:
            line_data = json.loads(line.split('data: ')[1])
            content += line_data["choices"][0]["delta"]["content"]
    content = content.split("[DONE]")[0]
    return content

def get_pokemon_info(pokemon_name):
    base_url = "https://pokeapi.co/api/v2"
    species_url = f"{base_url}/pokemon-species/{pokemon_name.lower()}"
    
    response = requests.get(species_url)
    if response.status_code == 200:
        species_data = response.json()
        info = []
        
        info.append(f"Name: {species_data['name'].capitalize()}")
        info.append(f"ID: {species_data['id']}")
        info.append(f"Base Happiness: {species_data['base_happiness']}")
        info.append(f"Capture Rate: {species_data['capture_rate']}")
        info.append(f"Color: {species_data['color']['name'].capitalize()}")
        info.append(f"Egg Groups: {', '.join([group['name'].capitalize() for group in species_data['egg_groups']])}")
        info.append(f"Habitat: {species_data['habitat']['name'].capitalize()}")
        
        flavor_text_entries = []
        for entry in species_data['flavor_text_entries']:
            if entry['language']['name'] == 'en':
                flavor_text = textwrap.fill(entry['flavor_text'], width=80, initial_indent="- ", subsequent_indent="  ")
                flavor_text_entries.append(flavor_text)
        info.append("Flavor Text Entries:")
        info.extend(flavor_text_entries)
        
        info.append(f"Generation: {species_data['generation']['name'].capitalize()}")
        info.append(f"Growth Rate: {species_data['growth_rate']['name'].capitalize()}")
        info.append(f"Has Gender Differences: {species_data['has_gender_differences']}")
        info.append(f"Hatch Counter: {species_data['hatch_counter']}")
        info.append(f"Is Baby: {species_data['is_baby']}")
        info.append(f"Is Legendary: {species_data['is_legendary']}")
        info.append(f"Is Mythical: {species_data['is_mythical']}")
        info.append(f"Order: {species_data['order']}")
        
        pal_park_encounters = []
        for encounter in species_data['pal_park_encounters']:
            pal_park_encounters.append(f"- Area: {encounter['area']['name'].capitalize()}\n  Rate: {encounter['rate']}")
        info.append("Pal Park Encounters:")
        info.extend(pal_park_encounters)
        
        pokedex_numbers = []
        for pokedex_number in species_data['pokedex_numbers']:
            if pokedex_number['pokedex']['name'] == 'national':
                pokedex_numbers.append(f"- Number: {pokedex_number['entry_number']}")
        info.append("Pokedex Numbers:")
        info.extend(pokedex_numbers)
        
        info.append(f"Shape: {species_data['shape']['name'].capitalize()}")
        
        varieties = []
        for variety in species_data['varieties']:
            varieties.append(f"- Name: {variety['pokemon']['name'].capitalize()}")
        info.append("Varieties:")
        info.extend(varieties)
        
        return "\n".join(info)
    else:
        return f"Pokemon '{pokemon_name}' not found."










def startEventListining(email, password, session_cookies=None):
    
    class EventHandler(Client):
        from datetime import datetime
        from fbchat import Message, ThreadType
        def onPeopleAdded(self, added_ids, author_id, thread_id, **kwargs):
            if author_id != self.uid:
                for added_id in added_ids:
                    if added_id != self.uid:
                        user = self.fetchUserInfo(added_id)[added_id]
                        name = user.name
        
                        group_info = self.fetchGroupInfo(thread_id)
                        if thread_id in group_info:
                            participants = group_info[thread_id].participants
                            participant_count = len(participants)
        
                            message = f"Welcome to the group, {name}!\nID: {added_id}\nJoined at: {datetime.now()}\nmembers: {participant_count}"
                            self.send(Message(text=message), thread_id=thread_id, thread_type=ThreadType.GROUP)
        
                        group_info = self.fetchGroupInfo(thread_id)
        
                        if thread_id in group_info:
                            participants = group_info[thread_id].participants
                    elif added_id==self.uid:
                            self.changeNickname('bot', user_id=self.uid, thread_id=thread_id, thread_type=ThreadType.GROUP)

#                self.send(Message(text='connected!!!!!'), thread_id=thread_id, thread_type=ThreadType.GROUP)                
    
        def onPersonRemoved(self, mid=None, removed_id=None, author_id=None, thread_id=None, ts=None, msg=None):
            user = self.fetchUserInfo(removed_id)[removed_id]
            name = user.name
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            
            msg = f"""REMOVAL UPDATE\n\nremoved user:{name}\n\nremoved by:{author_name}\n\n{datetime.now()}"""
            self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
    
        def onAdminAdded(self, mid=None, added_id=None, author_id=None, thread_id=None, thread_type=ThreadType.GROUP, ts=None, msg=None):
            user = self.fetchUserInfo(added_id)[added_id]
            name = user.name
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            
            msg = f"""
                ADMIN UPDATED\nnew admin:{name}\nadded by:{author_name}\n\n{datetime.now()}
                """
            self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
    
        def onAdminRemoved(self, mid=None, removed_id=None, author_id=None, thread_id=None, thread_type=ThreadType.GROUP, ts=None, msg=None):  
            user = self.fetchUserInfo(removed_id)[removed_id]
            name = user.name
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            
            msg = f"""
                ADMIN UPDATED\admin removed:{name}\n removed by:{author_name}\n\n{datetime.now()}
                """
            self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
    
        def onApprovalModeChange(self, mid=None, approval_mode=None, author_id=None, thread_id=None, thread_type=ThreadType.GROUP, ts=None, msg=None):   
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            
            msg = f"""
                APPROVAL UPDATE\n\nstatus:{approval_mode}\n\nby:{author_name}\n\n{datetime.now()}
                """
            self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
    
        def onNicknameChange(self, mid=None, author_id=None, changed_for=None, new_nickname=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
            user = self.fetchUserInfo(changed_for)[changed_for]
            name = user.name
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            if author_id !=self.uid:
                    msg = f"""
                    NICKNAME UPDATED\n\nnickname of:{name}\n\nnickname:{new_nickname}\n\nby:{author_name}\n\n{datetime.now()}
                    """
                    self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
        
        def onTitleChange(self, mid=None, author_id=None, new_title=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            msg = f"""TITLE/GROUP NAME UPDATE\n\n current name:{new_title}\n\nby:{author_name}\n\n{datetime.now()}"""
            self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
    
        def onEmojiChange(self, mid=None, author_id=None, new_emoji=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):         
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            msg = f"""EMOJI UPDATE\n\ncurrent emoji:{new_emoji}\n\nby:{author_name}\n\n{datetime.now()}"""
            self.send(Message(text=msg), thread_id=thread_id, thread_type=thread_type)
    
        def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None): 
            author = self.fetchUserInfo(author_id)[author_id]
            author_name = author.name
            msg = f"""COLOR/THEME UPDATED\n\n current color/theme:{new_color}\n\nby:{author_name}\n\n{datetime.now()}"""
            self.send(Message(text=msg), thread_id=thread_id, thread_type=ThreadType.GROUP)
    
        def onPendingMessage(self, thread_id=None, thread_type=None, metadata=None, msg=None):
            thread_info = self.fetchThreadInfo(thread_id)[thread_id]
            group_name = thread_info.name 
    
        def friendConnect(self, friend_id):
            data = {"to_friend": friend_id, "action": "confirm"}
            j = self._payload_post("/ajax/add_friend/action.php?dpr=1", data)
    
        def onFriendRequest(self, from_id=None, msg=None):
            def friendConnect(self, friend_id):
                data = {"to_friend": friend_id, "action": "confirm"}
                j = self._payload_post("/ajax/add_friend/action.php?dpr=1", data)
            self.send(Message(text="""friend request received"""), thread_id=from_id)
    
        def onCallStarted(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None):
            pass
    
   
   
   
   
   
   
   
   
   
   
   
    
        def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
            print(message_object)      
            def sendMsg():
                if author_id != self.uid:
                    self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
    
            try:
                msg = str(message_object).split(",")[15][14:-1]
                print(msg)
                message_object.split(",")[0]
                if "//video.xx.fbcdn" in msg:
                    msg = msg
                else:
                    msg = str(message_object).split(",")[19][20:-1]
            except:
                try:
                    msg = message_object.text.lower()
                    print(msg)
                except:
                    pass
    
            if author_id != self.uid:
                lower_msg = msg.lower()
                
                if lower_msg.startswith('ai'):
                    reply="processing please wait......."
                    sendMsg()
                    reply=get_gpt_response(lower_msg)
                    sendMsg()
                   
             
                 
            
                elif    lower_msg.startswith("gpt"): 
                             q=lower_msg.replace("gpt ",'').replace(' ','+')
                             a=requests.get(f'https://gpt.irateam.ir/api/web.php?apikey=ThaN95311420779906mkjfh&type=freegpt5&question={q}').json()['results']['answer']
                             reply = a
                             sendMsg()
                             
                             
                                    
                elif lower_msg.startswith("asura-search"):
                        
                        try:
                            a = lower_msg
                            name = a.replace("asura-search ", "")
                            res=requests.get(f"https://asura.jemcarl.repl.co/asura-search?query={name}").text
                            j=eval(res)
                            result=""
                            r=""
                            n=0
                            for i in j:
                                r =f"""image:{i["image"]} \n\nlink:{i["link"]}\n\ntitle:{i["title"]}\n\nchapters:{i["chapter"]}\n\nratings:{i['ratings']}\n"""+"="*25
                                result = result + r +'\n'*2
                                if n==2:
                                	break
                                n+=1
                            reply = result
                            sendMsg() 
                       
                        except Exception as e :
                                     reply=e
                                     sendMsg()
                elif lower_msg.startswith("asura-read"):
                	
                	a = message_object.text
                	url = a.replace("asura-read ", "")
                	res=requests.get(f"https://asura.jemcarl.repl.co/asura-read?url={url}").text
                	api_response = json.loads(res)
                	imgs=api_response["imageUrls"]
                	self.sendRemoteFiles(imgs, message=url, thread_id=thread_id, thread_type=thread_type)
                	

                	
                	                           
                elif lower_msg.startswith("asura-view"):
                	
                	a = message_object.text
                	removepre = a.replace("asura-view ", "")
                	res = requests.get(f"https://asura.jemcarl.repl.co/asura-view?url={removepre}").text
                	api_response = json.loads(res)
                	r=""
                	res=''
                	n=0
                	for item in api_response:
                		r=f""" Link:{item["link"]}\nNumber :{item["num"]}\nDate:{item["date"]}\n\n"""
                		res+=r
                		if n==100:
                			reply=res
                			sendMsg()
                			res=""
                			n=0
            
                		n+=1
                	reply=res
                	sendMsg()
                		
                elif lower_msg.startswith("pinterest"):
                    try:
                            a = lower_msg
                            removepre = a.replace("pinterest ", "")
                            sp = removepre.split(" ")
                            n = int(sp[len(sp) - 1].replace("-", ""))
                            rvc = removepre.replace(sp[len(sp) - 1], "")
                            url = f"https://sim.ainz-project.repl.co/search/pinterest?search={rvc}"
                            res = requests.get(url).json()["data"][:n]
                            self.sendRemoteFiles(res, message=lower_msg, thread_id=thread_id, thread_type=thread_type)
                    except Exception as e:
                        reply = e
                        sendMsg()

                elif lower_msg.startswith('img'): 
                 	v=lower_msg.replace('img ','').replace(' ','+')
                 	url = f"https://testapi.heckerman06.repl.co/api/search/google-image?query={v}&apikey=buynew"
                 	lk=[]
                 	response = requests.get(url)
                 	data = response.json()
                 	if response.status_code == 200 and 'data' in data:
                 		links = data['data']
                 		for link in links[:5]:
                 			lk.append(link)
                 	else:
                 	      reply="Error: Failed to retrieve data from the API"
                 	      sendMsg()
                 	self.sendRemoteFiles(lk, message=v, thread_id=thread_id, thread_type=thread_type)
                 	lk.clear()     	    	
                
                elif lower_msg.startswith('pokemon-info'):
                    if lower_msg=='pokemon-info':
                        reply='usage:pokemon-info name/id\n\nex/pokemon-info pikachu\n\nmax id:1010:usage:pokemon-info 25'
                        sendMsg()
                    else:
                        pokemon_info = get_pokemon_info(lower_msg.replace('pokemon-info ',''))
                        reply=pokemon_info
                        sendMsg()

                
                    
    bot = EventHandler(email, password, session_cookies=session_cookies)
    try:
        bot.listen()
    except Exception as e:
         print(e)
         time.sleep(30)
         bot.listen()