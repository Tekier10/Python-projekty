"""
Program na export základních parametrů jednotlivých nabídek pronájmu z webového portálu s uložením do xls souboru každých 24h.
"""

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import xlsxwriter
import time

def get_adverts():
    workbook = xlsxwriter.Workbook('Nabídky pronájmu.xlsx')
    worksheet = workbook.add_worksheet()
    label_list = ['Číslo inzerátu', 'Typ nabídky', 'Adresa', 'Dispozice', 'Velikost', 'Extra informace', 'Nájemné', 'Poplatky']
    worksheet.write_row(0, 0, label_list)

    doc = requests.get(f"https://www.XXXXXXXXX.cz/vypis/nabidka-pronajem/byt").text
    soup = BeautifulSoup(doc, "html.parser")

    #počet stránek s výsledky
    pages = soup.find_all("li", class_="page-item")[-2]
    page_url = pages.find("a", href=True).get("href")
    page_parsed = urlparse(page_url)
    page_path = page_parsed.query
    numb_pages = int(re.findall("\d+", page_path)[0])

    offer_type_list = []
    location_list = []
    type_list = []
    size_list = []
    tags_list = []
    rent_list = []
    apartment_fees_list = []
    offer_id_list = []

    for page in range(numb_pages):
        iter_doc = requests.get(f"https://www.XXXXXXXXX.cz/vypis/nabidka-pronajem/byt?page={page}").text
        soup2 = BeautifulSoup(iter_doc, "html.parser")
        rental_offer = soup2.find_all("article", class_="PropertyCard_propertyCard__qPQRK propertyCard PropertyCard_propertyCard--landscape__7grmL")

        for offer in rental_offer:
            offer_type = offer.find("span", class_="PropertyCard_propertyCardLabel__lnHZu mb-2 text-caption text-grey-dark fw-medium text-uppercase text-truncate").text
            location = offer.find("span", class_="PropertyCard_propertyCardAddress__yzOdb text-subheadline text-truncate").text
            type = offer.find("ul", class_="FeaturesList_featuresList__W4KSP featuresList mt-3").contents[0].text
            size = offer.find("ul", class_="FeaturesList_featuresList__W4KSP featuresList mt-3").contents[1].text
            tags = offer.find("p", class_="mt-2 mt-md-3 mb-0 text-caption text-truncate-multiple").text.replace("•",",")
            rent = offer.find("p", class_="PropertyPrice_propertyPrice__aJuok propertyPrice mb-0 mt-3").contents[0].text.strip()
            rent = rent.replace(u'\xa0', ' ')
            apartment_fees = offer.find("p", class_="PropertyPrice_propertyPrice__aJuok propertyPrice mb-0 mt-3")
            if len(apartment_fees) < 2:
                 apartment_fees = "NA"
            else:
                 apartment_fees = apartment_fees.contents[1].text.strip()
                 apartment_fees = apartment_fees.replace(u'\xa0', ' ')

            url = offer.find("a", href=True).get("href")
            parsed = urlparse(url)
            path = parsed.path
            offer_id = re.findall("\d+", path)[0]

            offer_type_list.append(offer_type)
            location_list.append(location)
            type_list.append(type)
            size_list.append(size)
            tags_list.append(tags)
            rent_list.append(rent)
            apartment_fees_list.append(apartment_fees)
            offer_id_list.append(offer_id)

    for _ in offer_id_list:
        worksheet.write_column(1, 0, offer_id_list)

    for _ in offer_type_list:
        worksheet.write_column(1, 1, offer_type_list)

    for _ in location_list:
        worksheet.write_column(1, 2, location_list)

    for _ in type_list:
        worksheet.write_column(1, 3, type_list)

    for _ in size_list:
        worksheet.write_column(1, 4, size_list)

    for _ in tags_list:
        worksheet.write_column(1, 5, tags_list)

    for _ in rent_list:
        worksheet.write_column(1, 6, rent_list)

    for _ in apartment_fees_list:
        worksheet.write_column(1, 7, apartment_fees_list)

    workbook.close()

if __name__ == "__housing_prices__":
    while True:
        get_adverts()
        time_wait = 24
        time.sleep(time_wait*60*60)

