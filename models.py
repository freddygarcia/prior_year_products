import requests
import urllib.parse as parse_url
import os
import argparse

from json import loads as to_json
from pandas import DataFrame, concat as concat_df
from bs4 import BeautifulSoup as Soup
from urllib.request import urlretrieve
from pathlib import Path


class IRSFinder():

    URL = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?'

    def __init__(self):
        self.page_offset = 0
        self.page_size = 100
        self.soup = None
        self.criteria = ''

    @staticmethod
    def download(url: str, path_to: str):
        try:
            urlretrieve(url, path_to)
        except Exception as ex:
            print(ex)

    @staticmethod
    def get_download_path(form_name, year: int):
        curr_dir = os.path.abspath(os.getcwd())
        target_path = os.path.join(curr_dir, form_name)
        Path(target_path).mkdir(parents=True, exist_ok=True)

        filename = f'{form_name} - {year}.pdf'
        path_to = os.path.join(target_path, filename)
        return path_to

    def get_soup(self) -> Soup:
        '''
            Return a BeautifulSoup object by doing a request to instance url
        '''
        url = self.url()
        res = requests.get(url)
        soup = Soup(res.text, features="html.parser")
        return soup

    def url(self) -> str:
        '''
            Build the url based on the object params
        '''

        params = {
            'resultsPerPage' : self.page_size,
            'sortColumn' : 'sortOrder',
            'indexOfFirstRow' : self.page_offset,
            'criteria' : 'formNumber',
            'value' : self.criteria,
            'isDescending' : 'false',
        }
        url = IRSFinder.URL + parse_url.urlencode(params)
        return url

    def has_next(self) -> bool:
        '''
            Checks if there is pagination on the search form by 
            counting the pagination list in the top right corner
        '''

        a_list = self.soup.select('.NumPageViewed a')

        self.page_offset += self.page_size
        self.soup = self.get_soup()

        return len(a_list) > 0

    def get_taxes_df(self) -> DataFrame:
        '''
            Parse the search form results into a Dataframe
        '''

        self.soup = self.get_soup()
        table = self.soup.find('table', {"class" : "picklist-dataTable"})
        rows = table.find_all('tr')

        taxes_list = { 'url_file' : [], 'form_number' : [], 'form_title' : [], 'year' : []}

        while True:

            # skips header
            for row in rows[1:]:
                product_td, title_td, year_td = row.find_all('td')

                product = product_td.text.strip()
                title = title_td.text.strip()
                year = int(year_td.text.strip())
                file_url = product_td.a.get('href', '')

                # check exact match
                if product == self.criteria:
                    taxes_list['url_file'].append(file_url)
                    taxes_list['form_number'].append(product)
                    taxes_list['form_title'].append(title)
                    taxes_list['year'].append(year)

            if not self.has_next():
                break

        df = DataFrame(taxes_list)
        return df

    def download_taxes(self, form_name: str,  year_from: int, year_to: int):

        self.criteria = form_name

        table_df = self.get_taxes_df()

        year_range = range(year_from, year_to)
        filtered_df = table_df[table_df["year"].isin(year_range)]
        
        for index, row in filtered_df.iterrows():
            form_number = row['form_number']
            download_url = row['url_file']
            year = row['year']

            path_to = IRSFinder.get_download_path(form_number, year)
            IRSFinder.download(download_url, path_to)

    def get_taxes_json(self, form_names: list) -> dict:

        taxes_df = None
        for form_name in form_names:
            self.criteria = form_name
            self.page_offset = 0

            df = self.get_taxes_df()

            if taxes_df is None:
                taxes_df = df
            else:
                taxes_df = concat_df([taxes_df, df], ignore_index=True)

        group_by = (taxes_df.groupby(['form_number',
                                    'form_title'])
                            .agg(min_year=('year','min'),
                                max_year=('year','max'))
                            .reset_index())
        group_by_dict = group_by.to_json(orient='records')
        json = to_json(group_by_dict)
            

        return json
