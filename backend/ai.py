import os


from dotenv import load_dotenv
from google import genai
from google.genai import types
from tavily import TavilyClient
from urllib3.contrib.emscripten import response

load_dotenv()

client = genai.Client()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query:str) -> list[dict]:
    """
    Search the live web for current Indian government scheme deadlines,
    application portal URLs, or schemes not found in the local database.

    Args:
        query: Specific search query(e.g. "Mukhyamantri Mahila Udyami Yojana Bihar 2026 last date").
    """
    try:
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_domains=["gov.in", "nic.in","jansamarth.in","sidbi.in",
                             "udyamimitra.in","standupmitra.in","mudra.org.in","cgtmse.in","nabard.org","rbi.org.in","nsdcindia.org"]
        )
        results=[]
        raw_results = response.get("results", [])
        for r in raw_results:
            item = {
                "title" : r["title"],
                "url": r["url"],
                "content": r["content"],
            }
            results.append(item)
        return results
    except Exception as e:
        return [{"error": str(e)}]


SystemPrompt = ("You are an Indian Government Scheme finder for the Rural, Semi Urban and Urban Women Entrepreneur"
                "Follow the rules and then give the output user want"
                "1. Keep asking the important relevant questions to solve the user's query"
                )



def model_reply(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SystemPrompt
        )
    )
    return response.text

print(model_reply("Hey, I am a 32-year-old woman living in a semi-urban town (nagarpalika area) near Muzaffarpur, Bihar. There are 3 more women with me—we are 4 women in total, aged between 26 and 38. All four of us live in the same town in Bihar, and we want to start a brand-new food processing business together, mainly making packaged spices (masala), homemade pickles, and roasted millet snacks to sell locally and in nearby cities."
                  "We need a loan of around ₹5 lakh (total project cost will be roughly ₹5.3 to ₹5.5 lakh for grinding and packaging machines plus raw materials). Right now, we can only arrange about ₹30,000 from our own savings as our contribution, and none of us own any land or house in our name to give as bank collateral or guarantee."
                  "About our background: in our group, the highest qualification is 12th pass (one woman passed 12th, two are 8th pass, and one studied till 5th class). Two of us belong to the OBC category and two are General category. Right now we are just an informal group—we have not registered as a Self Help Group (SHG), partnership, or cooperative yet, and we don't have Udyam registration, FSSAI, or GST either, though we are ready to get whatever registrations are required. None of us or our spouses have taken any government subsidy loan before, and we have finalized a small rented workshed on a 3-year lease."
                  "Can you figure out what schemes fit our group, whether our semi-urban town counts as rural or urban for subsidy, if our education and own-money contribution are enough, and what else you need from us before matching schemes?"))


def get_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=768)
    )
    vector = response.embeddings[0].values
    return vector

print (get_embedding("Hey how are you doing"))
