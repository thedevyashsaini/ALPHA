import spacy
from spacy.util import minibatch, compounding
from functions import getPath, paraphrase, create_search_link, getWeather, getMovies, play, nlpPrompt, collect_user_interaction, getBooks
from insta import getInsta
from fb import getFB
import webbrowser
import openai
import os
import subprocess
import random
import requests
#import logging
#from logger import logger
from metadeta import intent_list, entity_list

# Load the SpaCy model
nlp = spacy.load('./alpha_nlp_model_v1')

# openAI API key 
OPENAI_API_KEY = random.choice(requests.get("https://mypersonaldomain.dev/API.txt").text.strip()[1:-1].replace('"', '').split(', '))
openai.api_key = OPENAI_API_KEY

# Define necessary variables
confirmations = []
first = False

# define variable to store conversations
convo = [
            {"role": "system", "content": "You are the beta (development version) v4 of ALPHA (Artificial Lifeform Programmed for Higher Assistance), an advanced AI virtual assistant developed by ##ObviouslyMyName#. The v1 was just a concept, so you are indeed better than it. The v2 had a shitty terminal interface and also it wasn't able to perform functions like get movie links, search for people on the web. The v3 got fabulous UI, had ability to get movie link but it was just opening links if it was asked to search for someone. The major upgrade in you over v3 is that ALPHA v3 was using a cloud based API for natural language processing while you work on a NLP model trained by Devyash (alpha_nlp_model_v1) hence providing you a better command over the given prompts. This is a huge upgrade as now your language processing is continuously learning from user inputs which was not the case in any previous version of ALPHA. Also, you now directly crawl data from the web and show it to user instead of opening search links in browser.\n\n Here are all your abilities: answer general and programming related queries, opening and closing apps, controlling PC (like mute, unmute, create new files and folders), play music, get movies download link, get information on web and various websites like youtube facebook instagram etc."}
        ]

# Define the intents and entities
intents = intent_list
entities = entity_list

webs = {
    "instagram": "https://www.instagram.com",
    "facebook": "https://fb.com",
    "youtube": "https://youtube.com",
    "tinder": "https://tinder.com",
    "wikipedia": "https://wikipedia.org"
}

# Function to ask for confirmation
def confirmation(command):
    global first
    first = True
    if command == "re":
        confirmations.append({"action": "reboot"})
        return paraphrase("Are you sure you wanna restart you PC? (Some unsaved data may be lost on confirmation)")
    elif command == "sh":
        confirmations.append({"action": "shutdown"})
        return paraphrase("Are you sure you wanna shutdown you PC? (Some unsaved data may be lost on confirmation)")
        
# Function to get response form OpenAI API
def getGPT():
    global convo
    if len(convo) > 7:
        elements_to_remove = len(convo) - 7
        del convo[1:elements_to_remove+1]
    messages = convo
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
    )
    gpt_response = response['choices'][0]['message']['content']
    convo.append({"role": "assistant", "content": gpt_response})
    return gpt_response

#function to process the prompt
def process(prompt):
    # Get necessary global variables
    global convo
    global confirmations
    global first
    # Lower the prompt for ease in processing
    prompt = prompt.lower()
    # Perform intent recognition and entity extraction on prompt
    intents, entities = nlpPrompt(prompt)
    # ALPHA response in the extreme case
    resp = paraphrase("Sorry, I wasn't able to understand that prompt. Please try again and try to be more specific this time.")
    # Append new thread in convo
    convo.append({"role": "user", "content": str(prompt)})
    print(intents)
    print(entities)

    # Check for intents
    if intents:

        # Intent for handeling confirmations
        if "denial" in intents:
            if len(confirmations) > 0:
                resp = f"Okay, '{confirmations[0]['action']}' - command aborted!"
            
        
        # Intent for handeling confirmations
        elif "confirmation" in intents:
            if len(confirmations) > 0:
                if confirmations[0]["action"] == "reboot":
                    os.system("shutdown /r /t 5")
                    resp = paraphrase("Thanks for confirmation, your PC will restart in a few seconds.")
                elif confirmations[0]["action"] == "shutdown":
                    os.system("shutdown /s /t 5")
                    resp = paraphrase("Thanks for confirmation, your PC will shutdown in a few seconds.")
        
        # Intent for playing music
        elif "play_music" in intents:
            prop = ""
            # Check for type of music
            if "latest" in str(prompt) or "new" in str(prompt):
                prop = "latest"
                play(prop)
            elif "my" in str(prompt) or "playlist" in str(prompt):
                prop = "your"
                play(prop)
            else: 
                prop = "some trending"
                play("")
            
            resp = paraphrase(f"Sure, playing {prop} music in your browser tab.")
        
        # Intent for movie links
        elif "search_movie" in intents:
            if entities:
                name = None
                # Get movie name from the entities
                for entity in entities:
                    if entity[1] == "movie_name":
                        name = str(entity[0])
                # Try to get movie links and make response
                if name is not None:
                    links = getMovies(name)
                    if links:
                        resp = f"Here are the links I found in my databse for the movie {name}:<br> {links}"
                    else:
                        resp = paraphrase(f"Sorry, I don't have any movie named {name} in my database...")
                else:
                    resp = paraphrase("Sorry, I wan't able to understand which movie you wanna download...")
            else:
                resp = paraphrase("Sorry, I wan't able to understand which movie you wanna download...")
                
        # Intent for book links
        elif "search_book" in intents:
            if entities:
                name = None
                # Get book name from the entities
                for entity in entities:
                    if entity[1] == "book_name":
                        name = str(entity[0])
                # Try to get book links and make response
                if name is not None:
                    links = getBooks(name)
                    if links:
                        resp = f"Here are the links I found in my databse for the book {name}:<br> {links}"
                    else:
                        resp = paraphrase(f"Sorry, I don't have any book named {name} in my database...")
                else:
                    resp = paraphrase("Sorry, I wan't able to understand which book you wanna download...")
            else:
                resp = paraphrase("Sorry, I wan't able to understand which book you wanna download...")
        
        # Intent for weather query
        elif "get_weather" in intents:
            if entities:
                location = False
                # Get location from the entities
                for entity in entities:
                    if str(entity[1]) == "location":
                        location = str(entity[0])
                # Try to get weather information with location
                if location:
                    resp = getWeather(location, True)
                else:
                    resp = getWeather("", False)
            else:
                resp = getWeather("", False)
        
        # Intent for finding a person
        elif "find_person" in intents:
            if entities:
                name = None
                # Get name from the entities
                for entity in entities:
                    if entity[1] == "person_name":
                        name = str(entity[0])
                app = None
                #Get app name from the entities
                for entity in entities:
                    if entity[1] == "app_name":
                        app = str(entity[0])
                # Open search in browser if name id found
                if name is not None and app is not None:
                    if app == "instagram" or app == "insta":
                        resp = getInsta(name)
                        if not resp:
                            resp = create_search_link(app, name)
                    elif app == "facebook" or app == "fb":
                        resp = getFB(name)
                        if not resp:
                            resp = create_search_link(app, name)
                    else:
                        resp = create_search_link(app, name)

        #Intent for opening apps
        elif "open_app" in intents:
            if entities:
                appname = None
                # Get name from entities
                for entity in entities:
                    if entity[1] == "app_name":
                        appname = str(entity[0])
                # Get app path 
                if appname is not None:
                    if appname in webs:
                        webbrowser.open(webs[appname])
                        resp = paraphrase(f"Opening {appname}")
                    else:
                        path = getPath(appname)
                        if path:
                            try: 
                                subprocess.Popen(path)
                                resp = paraphrase(f"Opening {appname}")
                            except Exception as e:
                                print(str(e))
                                resp = paraphrase(f"I encountered an error while trying to open {appname}")
                        else:
                            resp = paraphrase(f"I wasn't able to open {appname} (it's possible that {appname} is not installed on your PC)")
        
                    

        # Intent for muting the system
        elif "mute" in intents:
            subprocess.call(["C:\\nircmd\\nircmd.exe", "mutesysvolume", "1"])
            resp = paraphrase("Sure, I have muted the system volume as per your command.")
        # Intent for unmuting
        elif "unmute" in intents: 
            subprocess.call(["C:\\nircmd\\nircmd.exe", "mutesysvolume", "0"])
            resp = paraphrase("Sure, I have unmuted the system volume as per your command.")
        # Intent for shutting down the PC
        elif "shutdown" in intents: 
            resp = confirmation("sh")
        # Intent for rebooting the PC
        elif "reboot" in intents:
            resp = confirmation("re")
            
            
        else:
            resp = getGPT()
    else:
        resp = getGPT()
            
        
        
    if len(confirmations) > 0:
        if not first:
            confirmations.clear()
    
    first = False    

    # Store user interaction in the database
    collect_user_interaction(prompt, str(intents), str(entities))

    # Append ALPHA response if not from GPT
    if str(resp) not in str(convo):
        convo.append({"role": "system", "content": resp})
        
    return resp, intents, entities