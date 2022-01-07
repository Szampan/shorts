"""
App collecting the most commonly requested skills on NoFluffJobs.com

TODO:
- control with parameters (eg. how many top skills to show; how to show (plot, bar/ pie, print), search keywords)
- sqlite?


Done: 
- in subpage: collect items from <common-posting-requirements (no id)> and <common-posting-requirements id="posting-nice-to-have">
- create dictionary / counter: {skill: quantity} from collected data
- find and go to all subpages if "python" in <nfj-posting-item-title> or in <div class="posting-info"> 
    within <a class="posting-list-item>
- go to the next page

"""

from requests import get
from bs4 import BeautifulSoup
from collections import Counter
from matplotlib import pyplot as plt
from icecream import ic
# import pandas as pd
# import sqlite3
import time

start_time = time.time()

base_URL = "https://nofluffjobs.com"
# URL = "https://nofluffjobs.com/pl/praca-it/praca-zdalna/python?criteria=city%3Dbialystok%20seniority%3Dtrainee,junior"
URL = "https://nofluffjobs.com/pl/praca-it/python?criteria=seniority%3Dtrainee,junior"
to_exclude = ['python']    

def main():
    page = get(URL)
    URL_subpages = get_list_of_subpages(URL) # TODO: add next page functionality
    obligatory = []
    nice_to_have = []
    
    # try:

    obligatory, nice_go_have = get_skills_from_subpages(URL_subpages[:3])
    obligatory = exclude_unnecessary(obligatory, to_exclude)
    ic(obligatory)

    print('\nOBLIGATORY:')
    print_most_common(obligatory, 15)
    print('\nNICE TO HAVE:')
    print_most_common(nice_to_have, 10)     # what if there is less than 10? fix it

    plot_most_common(obligatory, 15, f"Most commonly requested skills ({len(URL_subpages)} offers)")
    # plot_most_common(nice_to_have, 15, "Nice to have skills")


    # except: 
    #     print('No subpages found')


def get_list_of_subpages(url) -> list:     # ADD FILTER ('python')
    print('\nGET LIST OF SUBPAGES')
    subpages = [] 

    while True:
        page = get(url)
        bs = BeautifulSoup(page.content, 'html.parser')
        offers = bs.body.find_all('a', class_= 'posting-list-item')
        for offer in offers:
            href = offer['href']
            subpages.append(href)

        url = get_next_page_url(bs)
        if not url:
            break
    ic(subpages)
    return subpages

def get_next_page_url(bs):
    next = bs.body.find('a', attrs={'aria-label': 'Next'})
    if next:
        ic(next['href'])
        return base_URL + next['href']
    print('NO NEXT PAGE')
    return

def get_skills_from_subpages(url_subpages) -> tuple: 
    tmp_nice_to_have = []
    tmp_obligatory = []
    for url_subpage in url_subpages:
        print('SUBPAGE:', base_URL + url_subpage)
        subpage = get(base_URL + url_subpage)
        skills = find_skills_on_subpage(subpage)
        tmp_obligatory += skills[1]
        tmp_nice_to_have += skills[0]
    
    ic(tmp_obligatory, tmp_nice_to_have)
    return(tmp_obligatory, tmp_nice_to_have)

def find_skills_on_subpage(subpage):
    bs = BeautifulSoup(subpage.content, 'html.parser')
    html_requirements_nice = []

    html_requirements_all = bs.body.find_all('common-posting-item-tag')
    html_requirements_nice_wrapper = bs.body.find('common-posting-requirements', attrs={'id': 'posting-nice-to-have'})
    if html_requirements_nice_wrapper:
        html_requirements_nice = html_requirements_nice_wrapper.find_all('common-posting-item-tag')

    requirements_all = [requirement.text for requirement in html_requirements_all]
    requirements_nice = [requirement.text for requirement in html_requirements_nice]
    requirements_obligatory = [item for item in requirements_all if item not in requirements_nice]

    return (requirements_nice, requirements_obligatory)

def print_most_common(list_of_items, number):
    for item, count in Counter(list_of_items).most_common(number):
        print(item, '->', count)
    
 
def plot_most_common(list_of_items, number, title):
    items = []
    popularity = []
    for item, count in Counter(list_of_items).most_common(number):
        items.append(item)
        popularity.append(count)

    # print('PLOT:', items, popularity)
    plt.style.use('fivethirtyeight')
    plt.title(title)

    # items.reverse()
    # popularity.reverse()
    # plt.barh(items, popularity)
    # plt.plot(items,popularity)
    # plt.xlabel("Popularity")

    # colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    font = {'family': 'normal',
            #'weight' : 'bold',
            'size': 8}
    plt.rc('font', **font)
    plt.pie(popularity, labels=items) # colors=colors)

    plt.show()

def exclude_unnecessary(lst, to_exclude):
    if to_exclude:
        for word in to_exclude:
            return list(filter(lambda x: x.lower().strip() != word.lower(), lst))
    return lst


if __name__ == "__main__":
    main()
    print("\n--- %s seconds ---" % (time.time() - start_time))