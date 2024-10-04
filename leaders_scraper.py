from bs4 import BeautifulSoup
import requests
import re
import json

def get_leaders():
    root_url = 'https://country-leaders.onrender.com'
    with requests.Session() as session:
        cookies = session.get(f"{root_url}/cookie").cookies  # Getting the cookies
        countries = session.get(f"{root_url}/countries", cookies=cookies).json()
        leaders_per_country = {country : session.get(f"{root_url}/leaders", params={"country": country}, cookies=cookies).json() for country in countries}
    
    
        output_leader_paragraph_dict = {}
        for _, leaders in leaders_per_country.items():
            for leader in leaders:
                leader_wiki = leader['wikipedia_url']
                response = session.get(leader_wiki)
                wiki_page = BeautifulSoup(response.text, 'html.parser')
                paragraphs = wiki_page.find_all('p') # Find all paragraphs in the page
                cleaned_paragraph: str = get_first_paragraph(paragraphs)

                output_leader_paragraph_dict[f"{leader['first_name']} {leader['last_name']}"] = cleaned_paragraph
    return output_leader_paragraph_dict

def get_first_paragraph(paragraphs):
    for para in paragraphs:
        if para.find('b'):  # Check if the paragraph contains any <b> (bold) tags
            first_paragraph = para.get_text().strip()  # Get the text of the first paragraph with bold text
            cleaned_paragraph = clean_paragraph(first_paragraph)  # Clean the paragraph using regex
    return cleaned_paragraph  # Return the cleaned paragraph

def clean_paragraph(text):
    if text:  # Check if text is not None or empty
        cleaned_text = re.sub(r'\(.*?\)|\[\d+\]|<.*?>|ⓘ', '', text) # '' says replace with empty string, removing them from text
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Remove excess whitespace
    return cleaned_text

def save(leaders):
    with open('leaders.json', 'w') as json_file:
        json.dump(leaders, json_file, indent=4)

leaders = get_leaders()
save(leaders)