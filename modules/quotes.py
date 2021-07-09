import json 
import random 

def quote_request(): 
    with open('static/quotes.json') as num:
        data = json.load(num)
    return random.choice(data['quotes']) 