import json
import together

client = together.Together(api_key="API-KEY-HERE")

def important_words(all_entities):
    # Serialize your dictionary to JSON string if it's not already a string
    entities_json = json.dumps(all_entities) if not isinstance(all_entities, str) else all_entities
    
    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x22B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": '''You have been provided with a Python dictionary containing keywords from 10-K filings spanning 1995 to 2023. Your task is to filter and compile a list of the top 100 keywords that are most relevant and specific to the company's unique context. Exclude all generic terms. Focus on extracting words that highlight key themes, significant people, pivotal products, notable events, and industry-specific trends that have uniquely influenced the company during the specified period. The selected keywords should be highly specific to the company, potentially including buzzwords, legislation, and individual figures directly linked to the company's operations. The goal is to ensure that these keywords, when visualized in a word cloud using frequency data, clearly depict the most critical aspects of the company's history and industry footprint. Also omit words associated with 10-K filings. All of these words must be diverse and not similar to each other. This reponse must be a JSON desponse, such that it can directly used as a json without a need for any more preporcessing'''},
                {"role": "user", "content": entities_json}
            ]
        )
        # Extracting and returning the response in a JSON format
        # print(response)
        keywords = response.choices[0].message.content
        return keywords

    except Exception as e:
        print(f"Failed to generate keywords due to: {e}")
        # Return error in JSON format
        return json.dumps({"error": str(e)})
    
def text_generation(response):
    # Serialize your dictionary to JSON string if it's not already a string
    
    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x22B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are given a set of most important words or higlights for a given company based on the 10-K filing. The has been created into a eork clooud and displayed on the screen. You have anlayse them and tell them why the give a good insight and why using a word cloud is a good choice. Also touch on some of words and give insigths about them"},
                {"role": "user", "content": response}
            ]
        )
        # Extracting and returning the response in a JSON format
        # print(response)
        keywords = response.choices[0].message.content
        return keywords

    except Exception as e:
        print(f"Failed to generate keywords due to: {e}")
        # Return error in JSON format
        return json.dumps({"error": str(e)})
