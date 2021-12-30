"""
Libraries: Beautiful Soup

TODO:
https://nofluffjobs.com/pl/praca-it/praca-zdalna/python?criteria=city%3Dbialystok%20seniority%3Dtrainee,junior&page=1
- find and go to all subpages if "python" in <nfj-posting-item-title> or in <div class="posting-info"> 
    within <a class="posting-list-item>
- create dictionary / counter: {skill: quantity} from collected data


Done: 
- in subpage: collect items from <common-posting-requirements (no id)> and <common-posting-requirements id="posting-nice-to-have">



"""

from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

start_time = time.time()
URL = "https://nofluffjobs.com/pl/praca-it/praca-zdalna/python?criteria=city%3Dbialystok%20seniority%3Dtrainee,junior&page=1"
URL_sub = "https://nofluffjobs.com/pl/job/ai-developer-sport-vision-technology-sp-k-remote-ieeun8az"
page = get(URL)
subpage = get(URL_sub)
bs = BeautifulSoup(subpage.content, "html.parser")

html_requirements_all = bs.body.find_all('common-posting-item-tag')
html_requirements_nice_wrapper = bs.body.find('common-posting-requirements', attrs={'id': 'posting-nice-to-have'})
html_requirements_nice = html_requirements_nice_wrapper.find_all('common-posting-item-tag')

requirements_all = [requirement.text for requirement in html_requirements_all]
requirements_nice = [requirement.text for requirement in html_requirements_nice]
requirements_obligatory = [item for item in requirements_all if item not in requirements_nice]

# print(requirements_all)
print(requirements_nice)
print(requirements_obligatory)



print("\n--- %s seconds ---" % (time.time() - start_time))