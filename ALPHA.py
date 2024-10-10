import os
import spacy
import spacy.util
from flask import Flask, request, make_response, render_template, abort
import threading
import json
from functions import botStart, nlpPrompt, trainInstance
#from train import train
from processing import process
from db import connect
from urllib.parse import unquote
import glob
import sys
#import logging
#from logger import logger
from metadeta import intent_list, entity_list

conn = connect()

training_data = []

# Train the model if new training data is available
#if os.path.isfile(os.path.join(os.getcwd(), "trainingdata")):
#    train()

# Create a table to store user interactions
create_table_query = """
CREATE TABLE IF NOT EXISTS user_interactions (
    id SERIAL PRIMARY KEY,
    user_input TEXT,
    intents TEXT,
    entiites TEXT,
    valid TEXT
);
"""
with conn.cursor() as cursor:
    cursor.execute(create_table_query)
    conn.commit()

# Flask app instance
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/report')
def report():
    global training_data
    intents = unquote(request.args.get("intents")).lower()
    entities = unquote(request.args.get("entities")).lower()
    prompt = unquote(request.args.get("prompt")).lower()
    
    if intents and entities and prompt:
        intents = json.loads(intents)
        entities = json.loads(entities)
        training_data.append([prompt, {"intent": intents, "entities": entities}])
        print(training_data)
        if len(training_data) >= 4:
            file_pattern = "./trainingdata/trainingdata_*"
            file_list = glob.glob(file_pattern)
            count = len(file_list)
            with open(f"./trainingdata/trainingdata_{count}") as f:
                old_data = json.load(f)
                f.close()
            
            new_data = old_data + training_data
            print(new_data)
            
            if(trainInstance(new_data)):
                with open(f'./trainingdata/trainingdata_{count+1}', 'w') as json_file:
                    json_file.write(str(new_data))
                    json_file.close()
                    
                training_data = []
            else:
                abort(404)
        
        return "success"
    
    else: 
        abort(404)
        
@app.route('/process', methods=['POST'])
def initiateProcess():
    # Get input from the bot interface
    prompt = request.form.get('input')
    # Send it to processing and get the assistant reply from there
    text, intents, entities = process(prompt)
    response = make_response(json.dumps({"text": str(text), "intents": str(json.dumps(intents)), "entities": str(json.dumps(entities))}))

    # Set the necessary headers to allow cross-origin requests
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    response.headers['Access-Control-Allow-Methods'] = 'POST'  # Allow only POST requests
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow the Content-Type header

    return response
    
# Start Flask app in a separate thread
def run_flask_app():
    app.run()
    
def testStart():
    while True:
        prompt = input("Prompt: ")
        resp = process(prompt)
        print(f"ALPHA: {str(resp)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
            # Initiating ALPHA...
            print(" * Rendering ALPHA: true")
            # Create and start the Flask app thread
            flask_thread = threading.Thread(target=run_flask_app)
            flask_thread.start()
            # Start the interface for the bot
            botStart()

    else:
        function_name = sys.argv[1]
        if function_name == 'test':
            testStart()
        elif function_name == 'web':
            run_flask_app()
        else:
            print("Invalid function name.")