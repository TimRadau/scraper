import requests
from bs4 import BeautifulSoup
import random
import json
from agents import userAgents
from flask import Flask, render_template, jsonify



def check_site_availability(siteindex, query):
    
    URL = f"https://www.ebay-kleinanzeigen.de/seite:{siteindex}/s-{query}/k0"
    print(URL)


    resp = requests.get(URL,headers=headers)
    if not resp:
        return False
    else:
        return resp


def get_one_site(siteindex, query, headers):

    
    URL = f"https://www.ebay-kleinanzeigen.de/seite:{siteindex}/s-{query}/k0"
    print(URL)


    resp = requests.get(URL,headers=headers)

    #resp = check_site_availability(siteindex, query)
    soup = BeautifulSoup(resp.text,"html.parser")
    
    elements = soup.find_all("div", class_="aditem-main")
    items = []

    for element in elements:
        element_soup = BeautifulSoup(str(element), "html.parser")

        # Name finden
        name = element_soup.find('a', class_="ellipsis")
        name_text = name.text.strip() if name else "Kein Name gefunden"

        # Preis finden
        price = element_soup.find('p', class_='aditem-main--middle--price-shipping--price')
        price_text = price.text.strip() if price else "Kein Preis gefunden"

        # Link finden
        link = "https://www.kleinanzeigen.de" + name.get("href") if name else "Kein Link gefunden"

        # Daten in das Dictionary einfügen
        items.append({
            "name": name_text,
            "price": price_text,
            "link": link
        })
    return items


def get_pages(query, siteindex):
    headers = {'User-Agent': random.choice(userAgents)}
    all_elements = []

    for i in range(siteindex):
        all_elements.append(get_one_site(i, query, headers))

    # Rückgabe des JSON-Objekts
    return json.dumps(all_elements, indent=2, ensure_ascii=False)


#get_pages()

app = Flask(__name__, template_folder="../templates")


@app.route("/")
def home():
    return render_template("all_elements.html")

@app.route("/get_request/<search>/<page_amount>")
def get_req(search, page_amount):
    result_json = get_pages(search, int(page_amount))

    return jsonify(json.loads(result_json))

if __name__ == "__main__":
    app.run(debug=True)
