from flask import Flask
import os
import requests
# import pprint

app = Flask(__name__)

@app.route('/')
def get_info(word:str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 404:
        return "We are not able to provide any info about this word."
    
    data = response.json()[0]
    # pprint.pprint(data)
    message = parse(data)
    return message

def parse(data):
    word = data['word']
    meanings = '\n'
    
    meaning_count = 1
    for meaning in data['meanings']:
        meanings += 'Meaning ' + str(meaning_count) + ':\n\n'
        definition = ''
        example = ''
        antonyms = ''
        synonyms = ''
        definition_cout = 1
        for word_definition in meaning['definitions']:
            definition += '\n' + str(definition_cout) + '. ' + word_definition['definition']
            definition_cout += 1

            if 'example' in word_definition:
                example = word_definition['example'] + '\n'

        for antonym in meaning['antonyms']:
            antonyms += antonym + ', '
        for synonym in meaning['synonyms']:
            synonyms += synonym + ', '
    
        meanings += "Definition: " + definition +  '\n\n'
        if example:
            meanings += "Example: " + example + '\n'
        if synonyms:
            meanings += "synonyms: " + synonyms + '\n'
        if antonyms:
            meanings += "antonyms: " + antonyms + '\n\n'

        meaning_count += 1
    

    message = f"word: {word}\n{meanings}"
    # print(message)
    return message 

get_info('like')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5050))
    app.run(debug=True, host = '0.0.0.0', port = port)