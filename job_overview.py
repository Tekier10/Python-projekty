"""
Program na export základních parametrů pracovních pozic zveřejněných na pracovním portálu s uložením do txt souboru každých 24h.
"""

from bs4 import BeautifulSoup
import requests
import time


def find_job():

    doc = requests.get("https://www.XXXXX.cz/hledat/?searchForm%5Blocality_codes%5D=&searchForm%5Bprofs%5D=&searchForm%5Bother%5D=python&searchForm%5Bemployment_type_codes%5D%5B%5D=201300001&searchForm%5Bemployment_type_codes%5D%5B%5D=201300002&searchForm%5Bemployment_type_codes%5D%5B%5D=201300004&searchForm%5Bminimal_salary%5D=&searchForm%5Beducation%5D=&searchForm%5Bsuitable_for%5D=&searchForm%5Bsearch%5D=").text

    soup = BeautifulSoup(doc, "html.parser")

    jobs = soup.find_all("li", class_="search-result__advert")

    for index, job in enumerate(jobs):

        job_name = job.find("h3", class_="half-standalone")
        if job_name is None:
            job_name = "NA"
        else:
            job_name = job_name.strong.text

        job_company = job.find("div", class_="search-result__advert__box__item search-result__advert__box__item--company")
        if job_company is None:
            job_company = "NA"
        else:
            job_company = job_company.text.replace("•","").strip()

        job_location = job.find("div", class_="search-result__advert__box__item search-result__advert__box__item search-result__advert__box__item--location")
        if job_location is None:
            job_location = "NA"
        else:
            job_location = job_location.strong.text.replace(" ","").strip()

        job_type = job.find("div", class_="search-result__advert__box__item search-result__advert__box__item--employment-type")
        if job_type is None:
            job_type = "NA"
        else:
            job_type = job_type.text.replace("•","").strip()

        job_publish_date = job.find("span", class_="text-label text-label-serp search-result__advert__valid-from")
        if job_publish_date is None:
            job_publish_date = "NA"
        else:
            job_publish_date = job_publish_date.text

        with open(f"Jobs/{index}.txt", "w") as f:
            f.write(f"Název pozice: {job_name}\n"
                  f"Společnost: {job_company}\n"
                  f"Místo: {job_location}\n"
                  f"Druh úvazku: {job_type}\n"
                  f"Zveřejněno: {job_publish_date}")
            print(f"File saved: {index}.txt")

if __name__ == "__job_overview__":
    while True:
        find_job()
        time_wait = 24
        time.sleep(time_wait*60*60)