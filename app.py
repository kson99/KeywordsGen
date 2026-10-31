import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from keybert import KeyBERT


app = FastAPI()

# Load KeyBERT model once on startup
# This uses a tiny, fast model that runs locally on your CPU
kw_model = KeyBERT(model="all-MiniLM-L6-v2")

class TextPayload(BaseModel):
    text: str
    limit: int = 5 # Number of keywords to return

@app.post("/extract-keywords")
def extract_keywords(data: TextPayload):
    if not data.text.strip():
        return {"keywords": []}

    # Extract keywords/phrases
    # keyphrase_ngram_range=(1, 2) allows for single words and 2-word phrases
    # stop_words='english' filters out useless words like "the", "is", "at"
    keywords_with_scores = kw_model.extract_keywords(
        data.text,
        keyphrase_ngram_range=(1,2),
        stop_words="english",
        top_n=data.limit
    )

    # Strip out the statistical confidence scores, keep just the words
    keywords = [item[0] for item in keywords_with_scores]
    
    return {
        "keywords": keywords
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

