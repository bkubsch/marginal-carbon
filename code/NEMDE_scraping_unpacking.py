import requests
import bs4
import os

def outer_NEM_scraper():
    url_cond = []
    def NEM_scraper(urls, href_identifier=None,a=None,b=None,c=None):
        '''
        urls=[url1, urls2,...], href_identifier="href_segment_of_interest", a=start, b=end, c=step_size
        '''
        urls_scraped = []
        for url in urls:
            req = requests.get(url)
            assert req.status_code == 200
            soup = bs4.BeautifulSoup(req.content, 'html.parser')
            links = soup.find_all('a', href=True, text=href_identifier)
            links = [os.path.join(url, link.get_text())
                     for link in links[a:b:c]]
            for link in links:
                    urls_scraped.append(link)

        return urls_scraped
    years = NEM_scraper(["http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/"], a=1)
    months = NEM_scraper(years, a=1, c=2)
    NEMDE_Market_Data = NEM_scraper(months, href_identifier="NEMDE_Market_Data")
    NEMDE_Files = NEM_scraper(NEMDE_Market_Data, href_identifier="NEMDE_Files")
    final = NEM_scraper(NEMDE_Files, a=1)
    for url in final:
        if url.endswith("_xml.zip"):
            url_cond.append(url)
    return url_cond

def meh(name="Geht immer"):
    print(name)