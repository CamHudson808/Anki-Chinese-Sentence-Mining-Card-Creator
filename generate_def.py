from google import genai
from dotenv import load_dotenv
import os

class Generate_Def:
    def __init__(self, hanzi):

        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)


        english_res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Break down the sentence {hanzi}. Do not use quotes, bold, or italicize anything. Format should be [definiton of sentence] \\n [word] - [definition] \\n [word] - [definition] \\n etc. A newline should be between the definition and each word+def pair in the word breakdown"
        )
        self.defn = english_res.text
        print("gemini generated def:", english_res.text)
        # Properly format
        