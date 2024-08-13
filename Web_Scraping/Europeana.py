import requests
from bs4 import BeautifulSoup
import os

# Base URL for Europeana
base_url_euro = 'https://www.europeana.eu'
folder = "images"

# Function to extract hrefs from a page
def extract_hrefs(page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        item_previews = soup.find_all('div', {'data-qa': 'item preview'})
        hrefs = []
        for preview in item_previews:
            a_tag = preview.find('a')
            if a_tag:
                href = a_tag.get('href')
                if href:
                    hrefs.append(href)
        return hrefs
    return []

# Function to extract image src from a detail page
def extract_image_src(page_url):
    response = requests.get(base_url_euro + page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find('a', {'data-qa': 'download button'})
        if img_tag:
            return img_tag.get('href')
    return None

# Function to download the image
def download_image(img_url, filename):
    response = requests.get(img_url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

def main():
    # Define the base search URL with a placeholder for the page number
    base_search_url = 'https://www.europeana.eu/en/search?page={}&qf=TYPE%3A%22IMAGE%22&qf=IMAGE_SIZE%3Asmall&qf=collection%3Amigration&query=&view=list'
    num_pages = 3  # Adjust this to the number of pages you want to scrape

    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for page_number in range(1, num_pages + 1):
        # Create the URL for the current page
        page_url = base_search_url.format(page_number)
        print(f'Processing page: {page_url}')
        
        # Step 1: Extract URLs from the current page
        urls_euro = extract_hrefs(page_url)
        
        # Step 2: Extract and download images from each URL
        for url_euro in urls_euro:
            img_src = extract_image_src(url_euro)
            if img_src:
                filename = os.path.join(folder, url_euro.split('/')[-1] + '.jpg')
                download_image(img_src, filename)
                print(f'Downloaded {filename}')
            else:
                print(f'No image found for {url_euro}')

if __name__ == '__main__':
    main()
