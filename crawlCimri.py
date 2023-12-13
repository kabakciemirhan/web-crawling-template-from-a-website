from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_elements(site_url, tag_name, class_name_title, class_name_div, class_name_span1):
    try:
        response = requests.get(site_url)
        response.raise_for_status()  # Hata kontrolü
        soup = BeautifulSoup(response.content, 'html.parser')

        elements = soup.find_all(tag_name, class_=class_name_title)
        data_list = []

        for element in elements:
            title = element.text.strip()

            # İkinci sütuna "div" etiketinin "top-offers" class'ını çek
            div_element = element.find_next('div', class_=class_name_div)
            div_data = div_element.text.strip() if div_element else 'N/A'

            data_list.append({'title': title, 'div_data': div_data})

        # Span data çek
        span1_elements = soup.find_all('div', class_=class_name_span1)
        span1_data_list = [span.text.strip() for span in span1_elements]

        return data_list, span1_data_list
    except Exception as e:
        return [str(e)], [], []

@app.route('/', methods=['GET', 'POST'])
def index():
    site_url = None
    tag_name = 'h3'  # İstediğiniz etiket
    class_name_title = 'z7ntrt-1 QAJfQ'  # İstediğiniz sınıf (title)
    class_name_div = 'top-offers'  # İkinci sütun için istediğiniz sınıf (div)
    class_name_span1 = 's1tg1k8o-1 iRuHoK'  # Filtre için istediğiniz sınıf

    span1_data_list = []
    data_list = []

    if request.method == 'POST':
        site_url = request.form['site_url']
        data_list, span1_data_list = scrape_elements(site_url, tag_name, class_name_title, class_name_div, class_name_span1)

    return render_template('index-filtre.html', site_url=site_url, data_list=data_list, span1_data_list=span1_data_list)

if __name__ == '__main__':
    app.run(debug=True)
