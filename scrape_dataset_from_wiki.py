
# Part 1: Extraction of Links from the WHS List page
import requests
from bs4 import BeautifulSoup
import os
import shutil

def extract_links(page):
# Wikipedia page URL
    wiki_url = f"https://en.wikipedia.org/wiki/{page}"  # Replace with the actual Wikipedia page URL

    # Fetch the HTML content of the Wikipedia page
    response = requests.get(wiki_url)
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    pages = [page]
    # Find the table with the specified class and iterate through rows to extract links
    table = soup.find('table', {'class': 'wikitable'})
    if table:
        links = table.select('th[scope="row"] a')
        
        # Extract and print the href attributes (links)
        for link in links:
            href = link.get('href')
            if '%27' in href:
                href = href.replace('%27', "'")
            if 'The_Architectural_Work_of_Le_Corbusier' in href:
                href = href.replace('The_Architectural_Work_of_Le_Corbusier', 'Chandigarh_Capitol_Complex')
            if href.startswith('/wiki/'):
                pages.append(href[6:])
    else:
        print("Table not found on the Wikipedia page.") 
    return pages


# %%
#Part 2: Extracting the text from the Wikipedia pages of individual World Heritage Sites and saving it as markdown files

import wikipediaapi

def get_wikipedia_text(page_title):
    wiki_wiki = wikipediaapi.Wikipedia('wikipedia_agent_en')  # 'en' for English Wikipedia, change if needed
    page = wiki_wiki.page(page_title)

    if not page.exists():
        return "Page not found."

    return page.text

def save_as_markdown(text, folder_path, file_name):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def content_from_pages(pages):
    count = 1
    for page_title in pages:
        result = get_wikipedia_text(page_title)
        if result != "Page not found.":
            # Replace 'output.md' with your desired file path and name
            save_as_markdown(result, 'sites', page_title + '.md')
            print(f"Information about {page_title} saved as markdown file. {count} of {len(pages)} done.")
        else:
            print(result)
        count += 1

def main():
    page = 'List_of_World_Heritage_Sites_in_India'
    pages = extract_links(page)
    content_from_pages(pages)
    shutil.copy(f'general_info.md', 'sites')
    print('General Info moved to the sites dataset.')
    
if __name__ == '__main__':
    main()

