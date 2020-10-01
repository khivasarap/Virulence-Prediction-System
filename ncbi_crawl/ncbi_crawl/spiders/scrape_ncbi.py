import scrapy
import sys, traceback, re, os
import pandas as pd 

class GlobeNewsSpiderDirect(scrapy.Spider):
    name = 'scrape_ncbi'

    def get_accession_list(self):
        try:
            accessions = pd.read_csv('C://Users//kenns//Documents//Northeastern//CS6220//virulent-disease-classifier//covid_accessions.csv')
            print(accessions.info())
            acc_list = list(accessions['ids'].values)
            return acc_list

        except Exception as e:
            print('-'*80)
            print("Exception in accession list retrieval code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def start_requests(self):
        try:
            print('Fetching accession list file:')
            acc_list = self.get_accession_list()
            print(f'There are {len(acc_list)} accession names to scrape')

            test_acc = 'MT270101'
            test_url = f'https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&ids={test_acc}'

            yield scrapy.Request(url=test_url, callback=self.parse_virus_catalog)

        except Exception as e:
            print('-'*80)
            print("Exception in request initiation code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def parse_virus_catalog(self, response):
        
        url = response.url
        print(url)

        virus_table = response.xpath('//*[@class="usa-table-borderless order-column stripe nowrap dataTable no-footer"]//tbody')
        virus_table