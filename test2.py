import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

def get_prices(search_query):
    prices = {}
    image_urls = {}

    # Flipkart
    flipkart_url = f"https://www.flipkart.com/search?q={search_query}"
    flipkart_response = requests.get(flipkart_url)
    if flipkart_response.status_code == 200:
        flipkart_soup = BeautifulSoup(flipkart_response.content, 'html.parser')
        price_elements = flipkart_soup.find_all("div", class_="_30jeq3")
        if price_elements:
            prices['Flipkart'] = price_elements[0].text.strip()
            image_url = flipkart_soup.find("img", class_="_396cs4")
            if image_url:
                image_urls['Flipkart'] = image_url['src']
            else:
                image_urls['Flipkart'] = "Image not found on Flipkart"
        else:
            prices['Flipkart'] = "Price not found on Flipkart"
            image_urls['Flipkart'] = "Product not found on Flipkart"
    else:
        prices['Flipkart'] = f"Error retrieving data from Flipkart. Status code: {flipkart_response.status_code}"
        image_urls['Flipkart'] = "Error retrieving data from Flipkart"

    # Amazon
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    amazon_url = f"https://www.amazon.in/s?k={search_query}"
    amazon_response = requests.get(amazon_url, headers=headers)
    if amazon_response.status_code == 200:
        amazon_soup = BeautifulSoup(amazon_response.content, 'html.parser')
        price_elements = amazon_soup.find_all("span", class_="a-price-whole")
        if price_elements:
            prices['Amazon'] = price_elements[0].text.strip()
            image_url = amazon_soup.find("img", class_="_396cs4")
            if image_url:
                image_urls['Amazon'] = image_url['src']
            else:
                image_urls['Amazon'] = "Image not found on Amazon"
        else:
            prices['Amazon'] = "Price not found on Amazon"
            image_urls['Amazon'] = "Product not found on Amazon"
    else:
        prices['Amazon'] = f"Error retrieving data from Amazon. Status code: {amazon_response.status_code}"
        image_urls['Amazon'] = "Error retrieving data from Amazon"

    return prices, image_urls

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search1', methods=['POST'])
def search():
    search_query = request.form['search_query']
    prices, image_urls = get_prices(search_query)
    return render_template('result.html', prices=prices, image_urls=image_urls, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)