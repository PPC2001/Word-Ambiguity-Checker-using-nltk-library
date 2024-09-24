from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import nltk
from nltk.corpus import wordnet
from fastapi.responses import HTMLResponse

# Downloading the necessary wordnet data for the first time
nltk.download('wordnet')
nltk.download('omw-1.4')

# Create an instance of the FastAPI application
app = FastAPI()

# Serve static files from the 'static' directory at the '/static' path
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic model for the request body
class WordRequest(BaseModel):
    word: str  # The word for which we want to check ambiguity

# API endpoint to check word ambiguity
@app.post("/check_ambiguity/")
async def check_ambiguity(word_request: WordRequest):
    word = word_request.word  # Get the word from the request body
    syssets = wordnet.synsets(word)  # Get possible meanings (synsets) for the word
    result = {"word": word, "meanings": []}  # Initialize the result dictionary

    # If the word has more than one meaning, it's considered ambiguous
    if len(syssets) > 1:
        result["message"] = f"Ambiguity Detected. The word '{word}' has {len(syssets)} meanings."
        # Append each meaning to the result
        for syn in syssets:
            result["meanings"].append(syn.definition())
    else:
        # If only one meaning is found, return that meaning
        result["message"] = f"The word '{word}' has only one meaning."
        if syssets:
            result["meanings"].append(syssets[0].definition())

    # Return the result as a JSON response
    return result

# Serve the HTML homepage at the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    # Open and read the 'index.html' file from the 'static' folder
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())  # Return the HTML content as the response
