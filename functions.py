import spacy
from spacy.training.example import Example
import json
from db import connect
from render import html_content
import webbrowser
import webview
from transformers import pipeline
import openai
import random
import geocoder
from bs4 import BeautifulSoup
import requests
import random
#import logging
#from logger import logger
from metadeta import intent_list, entity_list
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import quote
import base64

# Load OpenAI
openai.api_key = random.choice(requests.get("https://mypersonaldomain.dev/API.txt").text.strip()[1:-1].replace('"', '').split(', '))

# Load the SpaCy model
nlp = spacy.load('./alpha_nlp_model_v1')

appNames = [
    ["notepad", ["notepad", "writing"]],
    ["brave", ["brave", "browser", "brave browser"]],
    ["cmd", ["command", "command prompt", "terminal", "cmd"]],
    ["chrome", ["google chrome", "chrome", "google"]],
    ["winrar", ["winrar", "zip", "unzip"]],
    ["vlc", ["vlc", "vlc player", "vlc media player", "video player"]],
    ["code", ["vs code", "code", "visual studio", "visual studio code"]]
]

# Load database credentials from db.json file
with open('db.json') as f:
    credentials = json.load(f)

# Connect to the ElephantSQL database
conn = connect()

def nlpPrompt(prompt):
    doc = nlp(prompt)
    # Extract intents
    intents = [label for label, score in doc.cats.items() if score > 0.5]
    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return intents, entities

def getPath(app):
    appname = ""
    for apps in appNames:
        if app in apps[1]:
            appname = apps[0]
    with open("programs.json") as p:
        paths = json.load(p)
    
    if appname in paths:
        path = paths[appname]
        return path
            
    return False

def paraphrase(sentence):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Paraphrase the following sentence while keeping the meaning the same:\n\"{sentence}\"",
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=15,
    )
    
    paraphrased_sentence = response.choices[0].text.strip()
    return paraphrased_sentence


# define function to load the webview
def botStart():
    width = 750
    height = 925
    window_title = "ALPHA (beta)" 
    webview.create_window(window_title, html=html_content(), width=width, height=height, resizable=False)
    webview.start()

# Function to collect and store user interaction in the database
def collect_user_interaction(user_input, intents, entities):
    insert_query = """
    INSERT INTO user_interactions (user_input, intents, entiites)
    VALUES (%s, %s, %s);
    """
    with conn.cursor() as cursor:
        cursor.execute(insert_query, (user_input, intents, entities))
        conn.commit()

# Function to perform continual learning
def trainInstance(training_data):

    print("Step 1: Loading a blank English language model...")
    nlp = spacy.blank("en")
    
    print("Step 2: Creating the TextCategorizer component for intent classification...")
    nlp.add_pipe("textcat_multilabel", name="textcat")
    textcat = nlp.get_pipe("textcat")
    
    print("Step 3: Adding the intents as labels to the TextCategorizer component...")
    for intent in intent_list:
        textcat.add_label(intent)
    
    print("Step 4: Creating the EntityRecognizer component for entity recognition...")
    nlp.add_pipe("ner")
    ner = nlp.get_pipe("ner")
    
    print("Step 5: Adding the entities as labels to the EntityRecognizer component...")
    for entity in entity_list:
        ner.add_label(entity)
        
    print("Step 4: Loading the training data and converting it into spaCy Example objects...")
    converted_training_data = []
    for example in training_data:
        text = example[0]
        annotation = example[1]
        entities = annotation['entities']
        converted_entities = [(text.index(entity[0]), text.index(entity[0]) + len(entity[0]), entity[1]) for entity in entities]
        annotation['entities'] = converted_entities
        converted_training_data.append((text, annotation))
    
    processed_data = []
    
    for text, annotation in converted_training_data:
        intent = annotation['intent']
        entities = annotation['entities']
    
        # Encoding the intent labels
        encoded_intents = []
        for intent_label in intent_list:
            label = 1 if intent_label in intent else 0
            encoded_intents.append(label)
    
        processed_entities = [(start, end, label) for start, end, label in entities]
        processed_annotation = {'cats': {intent_label: encoded_label for intent_label, encoded_label in zip(intent_list, encoded_intents)}, 'entities': processed_entities}
        example = Example.from_dict(nlp.make_doc(text), processed_annotation)
        processed_data.append(example)
    
    train_data = processed_data
    
    print("Step 5: Disabling unnecessary pipeline components for training...")
    pipe_exceptions = ["textcat", "ner"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    
    print("Step 6: Training the model...")
    with nlp.disable_pipes(*unaffected_pipes):
        optimizer = nlp.begin_training()
        for epoch in range(12):
            random.shuffle(train_data)
            losses = {}
            for example in train_data:
                nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
            print("Epoch:", epoch+1, "Losses:", losses)
    
    print("Step 7: Saving the trained model...")
    nlp.to_disk("./alpha_nlp_model_v1")
    return True

# Function to create search links for apps
def create_search_link(app_name, search_query):
    search_links = {
        "youtube": f"https://www.youtube.com/results?search_query={search_query}",
        "instagram": f"https://www.instagram.com/explore/tags/{search_query}",
        "facebook": f"https://www.facebook.com/search/top/?q={search_query}",
        "google": f"https://www.google.com/search?q={search_query}",
        "wikipedia": f"https://en.wikipedia.org/wiki/Special:Search?search={search_query}",
    }
    
    if app_name in search_links:
        search_link = search_links[app_name]
    else:
        search_link = None
    
    if search_link:
        webbrowser.open(search_link)
        return f"Sure, searching for '{search_query}' on {app_name} in a new browser tab."
    else: 
        webbrowser.open(f"https://www.google.com/search?q={search_query}+{app_name}")
        return f"Opening google search for your querry: {search_query} + {app_name}"

# Function to get weather data for a location
def getWeather(location, provided):
    api_key = '##RawWeatherAPIKey##'
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
    try:
        if provided: 
            response = requests.get(url)
            data = response.json()
            weather = data['current']['condition']['text']
            temperature = data['current']['temp_c']
            feels = data['current']['feelslike_c']
            location = f"{data['location']['name']}, {data['location']['region']}, {data['location']['country']}"
            windspeed = data['current']['wind_kph']
            winddir = data['current']['wind_dir']
            humidity = data['current']['humidity']
            weather_data = {'weather': weather, 'temperature': temperature, 'feels': feels, 'location': location, 'windspeed': windspeed, 'winddir': winddir, 'humidity': humidity}
            resp = f"Here is the weather information for {weather_data['location']}:<br><ul><li>weather: {weather_data['weather']}</li><li>temperature: {weather_data['temperature']}°C</li><li>feels like: {weather_data['feels']}°C</li><li>wind speed: {weather_data['windspeed']} kmph</li><li>wind dir: {weather_data['winddir']}</li><li>humidity: {weather_data['humidity']}</li></ul>"
            return resp
        
        else:
            try:
                g = geocoder.ip('me')
                weather_data = getWeather(f"{g.city, g.country}", True)
                return weather_data
                
            except Exception as e:
                    return f"Sorry, neither I was able to extract location from your prompt nor I was able to find location from your ip address.<br><br>Error: {e}"
            
    except requests.RequestException:
        return "I encountered some error while trying to fetch the weather information."


# Function to get movie links from the database
def getMovies(name):
    url = "https://mypersonaldomain.dev/search?key=" + name
    # Fetch the page
    response = requests.get(url)
    if response.status_code != 200:
        return False
    # Get elemetns with movie link
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_links = soup.find_all('a', class_='entry-title-link')

    if not movie_links:
        return False
        
    # Get all the article tags
    article_tags = soup.find_all('article')
    # Generate the links
    movie_results = ""
    for article in article_tags:
        links = article.find_all('a', class_='entry-title-link')
        for link in links:
            if link.get_text() != "":
                href = link.get('href')
                movie_name = link.get_text().replace("480p", "").replace("720p", "").replace("360p", "").replace("1080p", "")
                # Get the image source
                image = article.find('img', class_='entry-image')
                src = image['src']
                movie_results += f"""
        <div style='line-height: 35px;display: flex;margin-left: 10px;margin-bottom: 10px;box-shadow: 0 0 8px 1px #ffffff29;width: 260px;padding: 5px;padding-left: 0;border-radius: 35px 10px 10px 35px;'>
    <img src='https://movies.devyashsaini.repl.co{src}' class='preview'>
    <a style='text-decoration: none;color: #fff;margin-left: 10px;width: -webkit-fill-available;font-size: 16px;' href='https://movies.devyashsaini.repl.co{href}' target='_blank'>{movie_name}</a>
    </div>
        """

    return f"<br>{movie_results}"
    
    

def getBooksFromQuery(query, end):
    try:
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_argument('--log-path=/dev/null')
        driver = webdriver.Chrome(options=options)
        url = f'https://libgen.li/index.php?req={quote(query)}&columns%5B%5D=t&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&objects%5B%5D=w&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=r&topics%5B%5D=s&res=25&covers=on&filesuns=all'
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'tablelibgen')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'id': 'tablelibgen'})
        if table is None:
            return False
        rows = table.find_all('tr')[2:]  # Exclude the header row
        results = []
        count = 0
        if end:
            stop = int(end)
        else:
            stop = len(rows)
        stop = min(stop, len(rows))
        for row in rows:
            columns = row.find_all('td')
            link_a = columns[0].find('a')
            image_source = link_a.find('img')['src']
            info_a = columns[1].find('a')
            info_text = info_a.text.strip()
            #info_i_text = info_a.find('i').text.strip()
            text_td = columns[2].text.strip()
            #skip_td = columns[3:7]
            next_a = columns[7].find('a').text.strip()
            next_td_text = columns[8].text.strip()
            nested_a = columns[9].find('a')['href']
            if info_text != '':
                results.append(["https://mypersonaldomain.dev/edition/cover/"+str(base64.b64encode(image_source.replace("_small","").encode()).decode()), info_text, text_td, next_a, next_td_text, "https://api.devyashsaini.repl.co/edition/download/"+str(base64.b64encode(nested_a.encode()).decode())])
                count += 1
            if count == stop:
                break
        return results
    except Exception as e:
        print(str(e))
        return False
    finally:
        driver.quit()

    
# Function to get books
def getBooks(query):
    try:
        response = getBooksFromQuery(str(query), 4)
        if response: 
            books = response
            bookElements = ""
            for book in books:
                img = book[0]
                title = book[1]
                author = book[2]
                size = book[3]
                extention = book[4]
                link = book[5]
                bookElements += f"""
                <div class="dropdown-item">
        <span class="dropdown-title" onclick="window.open('{link}','_blank')">{title}</span>
        <ul class="dropdown-details">
          <li>
            <div class="detail-item">
              <div class="detail-text">
                <div>Author: {author}</div>
                <div>File Size: {size}</div>
                <div>File Extension: {extention}</div>
              </div>
              <div class="detail-image">
                <img src="{img}" alt="Author Image">
              </div>
            </div>
          </li>
        </ul>
      </div>
                """
            bookElements = f"<br><div class='dropdown'>{bookElements}</div>"
            return bookElements
        else: 
            return False
    except Exception as e:
        print(e)
        return False
    

# Function to play the desired type of music
def play(prop):
    if prop == "latest":
        webbrowser.open('https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk')
    elif prop == "your":
        webbrowser.open('https://open.spotify.com/playlist/009988')
    else:
        webbrowser.open('https://open.spotify.com/playlist/37i9dQZF1DXbVhgADFy3im')