import os


from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

def get_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=768)
    )
    vector = response.embeddings[0].values
    return vector

print (get_embedding("Hey how are you doing"))
