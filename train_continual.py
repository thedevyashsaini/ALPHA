import spacy
from spacy.training.example import Example
import json
from db import connect
from transformers import pipeline
import random

# Define the intents and entities
intent_list = [
    'open_app',
    'close_app',
    'mute',
    'unmute',
    'reboot',
    'shutdown',
    'create_file',
    'rename_file',
    'create_folder',
    'rename_folder',
    'search_movie',
    'find_person',
    'get_weather',
    'play_music',
    'confirmation',
    'denial',
]

entity_list = [
    'app_name', 
    'file_name', 
    'folder_name', 
    'old_name', 
    'new_name', 
    'filefolderlocation', 
    'location', 
    'person_name', 
    'movie_name',
    'additional',
]

conn = connect()

# Function to perform continual learning
def train_continual_learning():
    # Retrieve stored user interaction data from the database
    select_query = "SELECT id, user_input, intents, entiites FROM user_interactions WHERE valid = 'true' AND user != 'true';"
    with conn.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    try: 
        # Prepare the training data
        training_data = []
        for row in rows:
            id, user_input, intents, entities  = row
            input_data = [user_input, {'intent': intents, 'entities': entities}]
            intent_l = eval(input_data[1]['intent'])
            intent = intent_l if intent_l else []
            output_data = [input_data[0],{"intent": intent,"entities": [list(item) for item in eval(input_data[1]['entities'])]}]
            training_data.append(output_data)
    
        print("Step 1: Loading ALPHA's language model...")
        nlp = spacy.load("./alpha_nlp_model_v1")
        
        print("Step 2: Creating the TextCategorizer component for intent classification...")
        #nlp.add_pipe("textcat_multilabel", name="textcat")
        textcat = nlp.get_pipe("textcat")
        
        print("Step 3: Adding the intents as labels to the TextCategorizer component...")
        for intent in intent_list:
            textcat.add_label(intent)
        
        print("Step 4: Creating the EntityRecognizer component for entity recognition...")
        ner = nlp.get_pipe("ner")
        #nlp.add_pipe("ner")
        
        print("Step 5: Adding the entities as labels to the EntityRecognizer component...")
        for entity in entity_list:
            ner.add_label(entity)
        
        print("Step 6: Loading the training data and converting it into spaCy Example objects...")
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
        
        print("Step 7: Disabling unnecessary pipeline components for training...")
        pipe_exceptions = ["textcat", "ner"]
        unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        
        print("Step 8: Training the model...")
        with nlp.disable_pipes(*unaffected_pipes):
            optimizer = nlp.begin_training()
            for epoch in range(12):
                random.shuffle(train_data)
                losses = {}
                for example in train_data:
                    nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
                print("Epoch:", epoch+1, "Losses:", losses)
        
        print("Step 10: Saving the trained model...")
        nlp.to_disk("./alpha_nlp_model_v1")
    except Exception as e:
        print(f"ERROR :: {e}")
    
    update_query = "UPDATE user_interactions SET used = 'true' WHERE id = %s;" 

    with conn.cursor() as cursor:
        for row in rows:
            id_value = row[0]  
            cursor.execute(update_query, (id_value,))
    
        conn.commit()

train_continual_learning()