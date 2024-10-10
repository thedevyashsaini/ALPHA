import spacy
import random
import json
from spacy.training.example import Example
import os
import datetime
from metadeta import intent_list, entity_list



def train():
    
    print("Step 1: Loading a blank English language model...")
    nlp = spacy.blank("en")
    
    print("Step 2: Creating the TextCategorizer component for intent classification...")
    nlp.add_pipe("textcat_multilabel", name="textcat")
    textcat = nlp.get_pipe("textcat")
    
    print("Step 3: Adding the intents as labels to the TextCategorizer component...")
    for intent in intent_list:
        textcat.add_label(intent)
    
    #nlp.add_pipe(textcat)
    
    print("Step 4: Creating the EntityRecognizer component for entity recognition...")
    nlp.add_pipe("ner")
    ner = nlp.get_pipe("ner")
    
    print("Step 5: Adding the entities as labels to the EntityRecognizer component...")
    for entity in entity_list:
        ner.add_label(entity)
    
    print("Step 6: Loading the training data and converting it into spaCy Example objects...")
    with open("./trainingdata/trainingdata_4") as f:
        training_data = json.load(f)
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
        for epoch in range(15):
            random.shuffle(train_data)
            losses = {}
            for example in train_data:
                nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
            print("Epoch:", epoch+1, "Losses:", losses)
    
    print("Step 10: Saving the trained model...")
    nlp.to_disk("./alpha_nlp_model_v1")

    print("Training completed successfully!")

train()