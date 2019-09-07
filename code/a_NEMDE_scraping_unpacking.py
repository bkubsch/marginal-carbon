import requests
import bs4
import os

import logging
import sys
import zipfile


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



def extract_zip_from_url(url, output_path):
    month = url[-17:-8]
    output_folder = os.path.join(output_path, month)
    os.makedirs(output_folder, exist_ok=True)
    logging.info('downloading {}'.format(url))
    mms = os.path.join(output_folder, 'mmsdm.zip')
    with open(mms, 'wb') as f:
        response = requests.get(url, headers=header, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write('\r {}% [{}{}]'.format(2*done, '+'*done, ' '*(50-done)))
                sys.stdout.flush()

    logging.info('extracting {}'.format(url))
    
    #unzipping of zip from previous block
    with zipfile.ZipFile(mms, 'r') as my_zipfile:
        my_zipfile.extractall(output_folder)