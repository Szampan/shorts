# coding=utf-8

"""
App collecting the most commonly requested skills on NoFluffJobs.com

TODO:
- sqlite?
- UI?
"""
 
from requests import get
from bs4 import BeautifulSoup
from collections import Counter
from dataclasses import dataclass
from matplotlib import pyplot as plt
from icecream import ic
# import pandas as pd
# import sqlite3
import time

start_time = time.time()

@dataclass
class Config:
    keywords: str = "python junior trainee zdalnie"               
    obligatory_print_num: int = 20
    obligatory_plot_num: int = 15           
    nice_to_have_print_num: int = 15        
    subpages_parse_num: int = None             # For testing. None if parse all
    to_exclude: tuple = ("python",)           
    base_URL: str = "https://nofluffjobs.com"
    available_requirements = ["java", "python", ".net", "javascript", "php", "react", "angular", "android", "c++", "ios", "node.js", "sql", "golang", "ruby on rails", "scala", "aws", "azure", "c"]
    available_localizations = "Zdalnie, Warszawa, Kraków, Wrocław, Gdańsk, Poznań, Trójmiasto, Katowice, Śląsk, Łódź, Białystok, Gdynia, Lublin, Rzeszów, Bydgoszcz, Gliwice, Częstochowa, Szczecin, Sopot".lower().split(", ")
    available_seniorities = "Trainee, Stażysta, Mid, Junior, Senior, Expert".lower().split(", ")

def main():
    URL = generate_URL(Config.keywords)
    URL_subpages = get_list_of_subpages(URL)
    obligatory = []
    nice_to_have = []
    obligatory, nice_to_have = get_skills_from_subpages(URL_subpages[:Config.subpages_parse_num]) 
    obligatory = exclude_unnecessary(obligatory, Config.to_exclude)

    print('\nOBLIGATORY:')
    print_most_common(obligatory, Config.obligatory_print_num)
    print('\nNICE TO HAVE:')
    print_most_common(nice_to_have, Config.nice_to_have_print_num)     # what if there is less than 10? fix it

    plot_most_common(obligatory, 15, f"Most commonly requested skills. \nKeywords:  {Config.keywords}  \n({len(URL_subpages)} offers)")
    # plot_most_common(nice_to_have, 15, "Nice to have skills")
    
def generate_URL(keywords):
    keywords = keywords.lower().split()
    print(keywords)
    
    available_requirements = Config.available_requirements
    available_localizations = Config.available_localizations
    available_seniorities = Config.available_seniorities
    interfix = "/pl/praca-it"

    localizations = [normalize_localization(localization) for localization in available_localizations if localization in keywords]
    requirements = [requirement for requirement in available_requirements if requirement in keywords]
    seniorities = [seniority for seniority in available_seniorities if seniority in keywords]

    for keyword in keywords:        # EXCEPTION
        if keyword not in available_requirements + available_localizations + available_seniorities:
            print(f'ERROR: wrong keyword ({keyword})')
            # raise WrongKeyword(f'Wrong keyword: {keyword}')
        
    main_localization = get_first_if_possible(localizations)
    main_requirement = get_first_if_possible(requirements)
    criteria_suffix = get_criteria_suffix(localizations, requirements, seniorities)

    link = Config.base_URL + interfix + main_localization + main_requirement + criteria_suffix
    return link

def normalize_localization(word: str) -> str:      
    if word == "zdalnie":
        return "praca-zdalna"
    return remove_accents(word)

def remove_accents(input_text) -> str:
    strange=           'ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
    ascii_replacements='UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'
    translator=str.maketrans(strange,ascii_replacements)
    return input_text.translate(translator)

def get_first_if_possible(items: list) -> str:        
    if items:
        return f"/{items[0]}"
    return ""

def get_criteria_suffix(loc, reqs, seniorities):
    ic(loc, reqs, seniorities)
    
    if len(loc) > 1 or len(reqs) > 1 or seniorities:
        crit_city = get_crit_city_if_possible(loc)   
        crit_req = get_crit_req_if_possible(reqs)
        crit_seniority = get_crit_seniority_if_possible(seniorities) 

        criteria = [crit_city, crit_seniority, crit_req]
        criteria_suffix = "?criteria=" + "%20".join(filter(None, criteria))
        return criteria_suffix
    return ""

def get_crit_city_if_possible(loc: list) -> str:
    if len(loc) > 1:
        return "city%3D" + get_later_if_possible(loc)
    return

def get_crit_req_if_possible(reqs: list) -> str:
    if len(reqs) > 1:
        return "requirement%3D" + get_later_if_possible(reqs)
    return

def get_later_if_possible(items: list) -> str:
    if len(items) > 1:
        return ",".join(items[1:])
    return
    
def get_crit_seniority_if_possible(seniorities: list) -> str:
    if seniorities:
        return "seniority%3D" + ",".join(seniorities)
    return 


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
        return Config.base_URL + next['href']
    print('NO NEXT PAGE')
    return

def get_skills_from_subpages(url_subpages) -> tuple: 
    # test_obligatory = ['lulz', 'kicks', 'phun', 'kek', 'kek']       # for tests only
    # test_nice_to_have = ['a', 'b', 'c']
    # return (test_obligatory, test_nice_to_have)
    tmp_nice_to_have = []
    tmp_obligatory = []
    for url_subpage in url_subpages:
        print('SUBPAGE:', Config.base_URL + url_subpage)
        subpage = get(Config.base_URL + url_subpage)
        skills = find_skills_on_subpage(subpage)
        tmp_obligatory += skills[1]
        tmp_nice_to_have += skills[0]
    
    return (tmp_obligatory, tmp_nice_to_have)

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

def print_most_common(list_of_items: list, number: int):
    for item, count in Counter(list_of_items).most_common(number):
        print(item, '->', count)
 
def plot_most_common(list_of_items, number, title):
    items = []
    popularity = []
    for item, count in Counter(list_of_items).most_common(number):
        items.append(item)
        popularity.append(count)

    plt.style.use('fivethirtyeight')
    plt.title(title)

    # items.reverse()
    # popularity.reverse()
    # plt.barh(items, popularity)
    # plt.plot(items,popularity)
    # plt.xlabel("Popularity")

    # colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    font = {#'family': 'normal',
            #'weight' : 'bold',
            'size': 8}
    plt.rc('font', **font)
    plt.pie(popularity, labels=items) # colors=colors)

    plt.show()

def exclude_unnecessary(lst: list, to_exclude: list) -> list:
    if to_exclude:
        for word in to_exclude:
            ic(word)
            lst = list(filter(lambda x: x.lower().strip() != word.lower(), lst))
    ic(lst)
    return lst

# class WrongKeyword(Exception):
#     pass


if __name__ == "__main__":
    main()
    print("\n--- %s seconds ---" % (time.time() - start_time))