import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import webbrowser
import os

'''
This is a web scraper tool to download/analyze text in response to the NTIA AI Accountability RFC that 
closed on 6/12/2023
https://ntia.gov/press-release/2023/ntia-seeks-public-input-boost-ai-accountability

Used https://github.com/upenndigitalscholarship/regulations-gov-comment-scraper as a starting point,
but realized this only works for data sets uploaded at data.gov
'''

# Change this number to download files starting from 1
num_files = 10

# Configure download location
download_loc = "/Users/anitarao/TechCongress/ntia_ai_rfc_parser/NTIA_RFC_Files"

def make_urls():
    comments = ["{0:04}".format(i) for i in range(1,num_files+1)]
    return [url.format(c)
            for c in comments]

def download_files():
    urls = make_urls()
    for u in urls:
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            driver = webdriver.Chrome(options=op)
            driver.get(u)
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')    
            try:
                body = soup.find_all('section', class_="section-page-views mb-6")
                body1 = body[0].find_all('a', class_ = "btn btn-default btn-block")[0].get("href") 
                webbrowser.open(body1)
            except:
                body = soup.find('div', class_="px-2")

                file_name = u.split('/')[-1]
                words = [download_loc, file_name, ".txt"]
                outFileName="".join(words)
                outFile=open(outFileName, "w")
                outFile.write(body.text)
                outFile.close()

def main():
    download_files()


if __name__ == '__main__':
    main()
