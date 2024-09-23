from fastapi import FastAPI

from transformers import BertTokenizerFast, BertForTokenClassification  

model = BertForTokenClassification.from_pretrained("app/model")

tokenizer = BertTokenizerFast.from_pretrained('bert-base-multilingual-cased')

app = FastAPI()

# integers back to label names
label_mapping = {0: "O", 1: "B-ROUTENUMBER", 2: "B-ROUTENAME", 3: "I-ROUTENAME", 4: "B-STOPPLACE", 5: "I-STOPPLACE"}

@app.get('/')
def reed_root():
    return {'message': 'Ankomsttider Model API'}

@app.post('/recognize')
def recognize(text: str):
    """
    INFO:
    Recognizes certain words of an end user querying for the arrival time of public transportation like bus or trams
    \n\nArgs:
        text (str): the user query in a string sentence
        e.g. "Når kommer 20 skøyen bussen på carl bernes plass?"
    \n\nReturns:
        dict: A dict containing the recognized route number, route name and stop place that the user has provided in the query 
        e.g. 
        {'data': 
            {
            'route_number': 20,
            'route_name': "skøyen",
            'stop_place': "carl bernes plass"
            }
        }
    """
    route_name, route_number, stop_place = "", 0, ""

    inputs = tokenizer(text, return_tensors="pt")

    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)

    predicted_tags = [label_mapping[label_id.item()] for label_id in predictions[0]]

    # convert token ids back to words
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
    # merge the subwords    
    merged_tokens = []
    merged_tags = []

    for token, tag in zip(tokens, predicted_tags):
        if token.startswith("##"):
            merged_tokens[-1] += token[2:] # add the subword to previous token
        elif token in ["[CLS]", "[SEP]", "[PAD]"]: 
            continue # ignore special tokens
        else:
            merged_tokens.append(token)
            merged_tags.append(tag)

    for token, tag in zip(merged_tokens, merged_tags): # merged meaning merged after possible split-ups of tokens in tokenization
        if tag == "B-ROUTENAME" or tag == "I-ROUTENAME":
            route_name = route_name + " " + token
        elif tag == "B-ROUTENUMBER":
            route_number = token
        elif tag == "B-STOPPLACE" or tag == "I-STOPPLACE":
            stop_place = stop_place + " " + token

    if route_name == "":
        route_name = "undefined"
    if stop_place == "":
        stop_place = "undefined"

    data = {'data': {
        'route_number': route_number,
        'route_name': route_name,
        'stop_place': stop_place
    }}

    return {'recognized_data': data}
