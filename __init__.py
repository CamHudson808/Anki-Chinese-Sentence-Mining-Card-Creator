import sys
import generate_audio
import generate_def
import generate_pinyin
import upload_card

# Error handling with list of args
args = sys.argv
print(args)
if len(args) != 3:
    print("Format of call is: ./__init__.py [deck name] [txt file or chinese sentence]")
# Should first check if a file
else:
    deck_name = args[1]
    print(f"uploading cards to deck {deck_name}")
    file_parts = args[2].split(".")
    if file_parts and file_parts[-1] == "txt":
        # Then treat as a text file
        with open(f'{args[2]}', 'r') as file:
            for line in file:
                hanzi = line
                pinyin = generate_pinyin.Generate_Pinyin(hanzi).pinyin
                audio = generate_audio.Generate_Audio(hanzi)
                defn = generate_def.Generate_Def(hanzi).defn
                upload_card.Upload_Card(defn, hanzi, pinyin, audio.url, audio.filename, deck_name)
    else:
        # Treat as one off sentence
        hanzi = args[2]
        pinyin = generate_pinyin.Generate_Pinyin(hanzi).pinyin
        audio = generate_audio.Generate_Audio(hanzi)
        defn = generate_def.Generate_Def(hanzi).defn
        upload_card.Upload_Card(defn, hanzi, pinyin, audio.url, audio.filename, deck_name)
    
