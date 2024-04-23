import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
)

data = {
    "contents": [
        {
            "parts": [
                {"text": "Tell me a joke about HTML."}
            ]
        }
    ]
}

res = requests.post(
    URL,
    headers={
        "content-type": "application/json",
    },
    json=data,
    params={"key": os.getenv("GOOGLE_API_KEY")}
)

json_res = res.json()
pprint(json_res)

joke = json_res["candidates"][0]['content']['parts'][0]['text']
print(joke)