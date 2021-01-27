import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from tqdm import tqdm


def main(max_pages=20):

    """
    Scrap the title of each page and it's category


    param:
        max_pages(int): number of max pages to scrap, default is 10
    return:
        pandas dataframe with two columns 'Titles' and 'Categories'
    """
    # initialize empty lists where we store our data
    titles = []
    categories = []

    # get the list of pages scraped from the previous program

    pages = [line.strip() for line in open('www.depensez.com_internal_links.txt', 'r')]

    for i, page in tqdm(enumerate(pages[:max_pages])):

        soup = BeautifulSoup(requests.get(page).text, 'html.parser')
        try:
            container = soup.find('div', class_='entry-header')
            titles.append(container.h1.text)
            categories.append(container.h5.a.text)
            sleep(5)
        except:
            pass


    results = pd.DataFrame({
        'Titles': titles,
        'Categories': categories
    })

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Title scraper")
    parser.add_argument("-m", "--max-pages", help="Number of max URLs to crawl, default is 10.", default=10, type=int)

    args = parser.parse_args()
    max_pages = args.max_pages
    final_result = main(max_pages)

    # save the result in csv file for further processing
    final_result.to_csv('www.depensez.com_page_classification.csv')
