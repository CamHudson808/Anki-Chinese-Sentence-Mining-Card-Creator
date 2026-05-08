import json
import urllib.request

class Upload_Card:
    def __init__(self, defn, hanzi, pinyin, url, filename, deck_name):
        upload(defn, hanzi, pinyin, url, filename, deck_name)

createModelParams = {
    "modelName":"AnkiSentenceGen2",
    # "inOrderFields": ["Simp_Hanzi", "Trad_Hanzi", "Pinyin", "Definition"],
    # Instead, used card_creator to create the html for the front and the back
    "inOrderFields": ["English", "Pinyin", "Hanzi"],
    "isCloze": False,
    "cardTemplates": [
        {
            "Front": "{{Pinyin}}",
            "Back": "{{English}}<br>{{Pinyin}}<br>{{Hanzi}}"
        }
    ]
}

def upload(defn, hanzi, pinyin, url, filename, deck_name):
    # First, create the deck with name deck_name if deck_name doesn't exist with correct model, otherwise add to the deck deck_name
    createDeck = invoke("createDeck", deck=f"{deck_name}")
    print("createDeck res:", createDeck)
    try:
        createModel = invoke('createModel', **createModelParams)
        print("createModel res:", createModel)
    except Exception as e:
        print("this error occured when making model:", e)
        print("don't need to do anything if we already have model")
        pass
    # Should be able to then garuantee that the deck_name exists

    addCard = {
                "deckName":deck_name,
                "modelName":"AnkiSentenceGen2",
                "fields": {
                    "English": defn,
                    "Pinyin": pinyin,
                    "Hanzi": hanzi,
                },
                "audio": [{
                    "url": url,
                    "filename": filename,
                }]
            }
    canAdd = invoke("canAddNotesWithErrorDetail", notes=[addCard])
    print("canAdd return:", canAdd)

    if(canAdd[0]['canAdd']):
        invoke('addNote', note=addCard)
        print("added sentence:", hanzi)

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']