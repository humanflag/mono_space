import csv
from bs4 import BeautifulSoup
import requests
import re

lookup_list = [
    'woman',
    'women',
    'girl',
    'girls',
    'female',
    'females',
    'masculine',
    'feminine',
    'androcentric',
    'androcracy',
    'gf',
    'chad',
    'simps',
    'whores',
    'foids',
    'her',
    'cunt',
    'pussy',
    'pussies'
]

def get_text_from_specific_div(tag):
    target_div = tag.select_one(".bbWrapper")
    if target_div:
        blockquote = target_div.find('blockquote')
        if blockquote and blockquote.next_sibling:
            return blockquote.next_sibling.get_text(strip=True)
        return target_div.get_text(strip=True)
    return 'Text not found'

def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.replace('"', "'")

def fetch_and_process_html(url):
    # Fetch the HTML content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve content: HTTP ", response.status_code)
        return

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all articles with the class 'message'
    articles = soup.find_all('article', class_='message')

    # Prepare data for CSV
    data_to_write = []
    for article in articles:
        data_author = article.get('data-author', 'Author not found')
        message_body = article.find('article', class_='message-body')
        if message_body:
            specific_text = get_text_from_specific_div(message_body)
            clean_text_final = clean_text(specific_text)
            # check if any of the lookup words are in the text
            if any(re.search(r'\b{}\b'.format(re.escape(word)), clean_text_final.lower()) for word in lookup_list):
                data_to_write.append([data_author, clean_text_final])
        # else:
        #     data_to_write.append([data_author, 'No message body found'])

    # Write data to a CSV file
    with open('output.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        #writer.writerow(['user', 'post'])
        writer.writerows(data_to_write)

    print("Data has been written to output.csv")

# URL to fetch; replace with the actual URL you need
# from 500000 to 606223
baseURL = 'https://incels.is/threads/.'
count = 581319

while count < 606223:
    url = baseURL + str(count) + '/'
    print(f"Fetching and processing {url}")
    fetch_and_process_html(url)
    count += 1



