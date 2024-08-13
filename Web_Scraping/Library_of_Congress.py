import os
import requests
from bs4 import BeautifulSoup

# Step 1: Extract hrefs from the list items
def extract_urls_from_html(html_content, seen_urls):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.select('li.item a')
    new_urls = []
    for link in links:
        href = link.get('href')
        if href and href not in seen_urls:
            seen_urls.add(href)
            new_urls.append(href)
    return new_urls

# Step 2: Extract image src URLs from the provided page
def extract_image_src_from_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.select('img.iconic.screen-dependent-image')
        image_srcs = [img['src'] for img in images if 'src' in img.attrs]
        return image_srcs
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Step 3: Download images from the extracted URLs
def download_image(img_url, folder):
    try:
        image_name = os.path.basename(img_url.split('#')[0])
        if not os.path.exists(folder):
            os.makedirs(folder)
        image_path = os.path.join(folder, image_name)
        response = requests.get(img_url)
        response.raise_for_status()
        with open(image_path, 'wb') as image_file:
            image_file.write(response.content)
        print(f"Image downloaded and saved as {image_path}")
    except Exception as e:
        print(f"An error occurred while downloading {img_url}: {e}")

def main():
    base_url = 'https://www.loc.gov/photos/?c=150&dates=1800/1899&fa=online-format:image'
    max_pages = 3
    seen_urls = set()  # Track seen URLs to avoid duplicates

    for page_number in range(1, max_pages + 1):
        paginated_url = f'{base_url}&sp={page_number}&st=list'
        print("URL being Processed : : ", paginated_url)
        html_content = requests.get(paginated_url).text
        urls = extract_urls_from_html(html_content, seen_urls)

        for page_url in urls:
            image_srcs = extract_image_src_from_webpage(page_url)
            for img_src in image_srcs:
                download_image(img_src, 'images')

if __name__ == '__main__':
    main()
