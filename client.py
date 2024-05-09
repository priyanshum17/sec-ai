import json
import together

# Initialize the Together API client using the provided API key.
client = together.Together(api_key="API-KEY-HERE")

def important_words(all_entities):
    """
    Identifies important keywords from a dictionary of 10-K filing terms.

    Args:
    all_entities (dict or str): A dictionary or JSON string containing keywords from 10-K filings.

    Returns:
    str: A JSON string containing the top 100 most relevant and specific keywords to the company.
    """
    # Serialize the dictionary to a JSON string if it's not already a string.
    entities_json = json.dumps(all_entities) if not isinstance(all_entities, str) else all_entities
    
    try:
        # Make an API request to generate keywords.
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x22B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": '''You have been provided with a Python dictionary containing keywords from 10-K filings spanning 1995 to 2023. Your task is to filter and compile a list of the top 100 keywords that are most relevant and specific to the company's unique context. Exclude all generic terms. Focus on extracting words that highlight key themes, significant people, pivotal products, notable events, and industry-specific trends that have uniquely influenced the company during the specified period. The selected keywords should be highly specific to the company, potentially including buzzwords, legislation, and individual figures directly linked to the company's operations. The goal is to ensure that these keywords, when visualized in a word cloud using frequency data, clearly depict the most critical aspects of the company's history and industry footprint. Also omit words associated with 10-K filings. All of these words must be diverse and not similar to each other. This reponse must be a JSON desponse, such that it can directly used as a json without a need for any more preporcessing'''},
                {"role": "user", "content": entities_json}
            ]
        )
        # Extract and return the response in JSON format.
        keywords = response.choices[0].message.content
        return keywords

    except Exception as e:
        # Handle exceptions and return an error message in JSON format.
        print(f"Failed to generate keywords due to: {e}")
        return json.dumps({"error": str(e)})
    
def text_generation(response):
    """
    Generates a text analysis based on a set of keywords.

    Args:
    response (str): A JSON string containing important keywords or highlights for a company.

    Returns:
    str: A JSON string containing an analysis of why using a word cloud is a good choice along with insights on specific words.
    """
    
    try:
        # Make an API request to generate text analysis.
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x22B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are given a set of most important words or higlights for a given company based on the 10-K filing. The has been created into a eork clooud and displayed on the screen. You have anlayse them and tell them why the give a good insight and why using a word cloud is a good choice. Also touch on some of words and give insigths about them"},
                {"role": "user", "content": response}
            ]
        )
        # Extract and return the response in JSON format.
        keywords = response.choices[0].message.content
        return keywords

    except Exception as e:
        # Handle exceptions and return an error message in JSON format.
        print(f"Failed to generate keywords due to: {e}")
        return json.dumps({"error": str(e)})