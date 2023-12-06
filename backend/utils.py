from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import pandas as pd


load_dotenv()

OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_FILE_PATH = os.getenv("DEFAULT_FILE_PATH")


# Load the charity data CSV file on startup
charity_data = pd.read_csv(DEFAULT_FILE_PATH)

def lookup_ein(ein):
    """
    Looks up the given EIN in the charity data CSV file and returns the corresponding row data.

    Parameters:
    ein (str): The EIN number to look up.
    file_path (str): The path to the CSV file containing charity data.

    Returns:
    dict: A dictionary containing the data of the charity with the specified EIN, or an error message.
    """
    try:
        # Read the CSV file
        

        # Remove space and dash characters from the EIN if present
        ein = ein.replace(" ", "").replace("-", "")

        # Make sure it's a number
        if not ein.isnumeric():
            return {"error": "Invalid EIN. Must be a number."}
        
        ein = int(ein)


        # Find the row with the matching EIN
        charity_row = charity_data.loc[charity_data['EIN'] == ein]

        # Check if any row was found
        if charity_row.empty:
            return {"error": "No charity found with the given EIN."}
        else:
            # Convert the row to a dictionary
            charity_info = charity_row.to_dict(orient='records')[0]
            return charity_info
    except Exception as e:
        return {"error": str(e)}


def create_prompt(data):
    prompt = f"""
    Charity Data: {data}
    

    Can you answer the following questions in JSON format based on the data above?
    1. What is the charity's name? 
    2. What type of charity are they?
    3. What form did the charity submit?
    4. Who is the contact?
    4.1 and what is their title? 
    5. What is their salary?
    6. What is the ruling year of the charity?
    7. Where is the charity located?
    8. What is the website of the charity?
    9. What are the programs the charity has?
    10. List all financial information and the year the financial information refers to if available.

    The question number should be the key and the answer should be the value.

    """
    return prompt


def get_completion(prompt):
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        organization=OPENAI_ORG_ID
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": prompt}
    ]
    )

    return  completion


def get_response(row):
    prompt = create_prompt(row)
    completion = get_completion(prompt)
    return json.loads(completion.choices[0].message.content)


