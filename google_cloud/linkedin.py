import scrapy
import re
import math
import pandas as pd
import time
import datetime

from google.cloud import bigquery
from google.cloud import bigquery
from google.oauth2 import service_account

class ExempleSpider(scrapy.Spider):
    name = 'linkedin'

    #24 hours ago full time
    start_urls =  ['https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Estados%20Unidos&locationId=&geoId=103644278&sortBy=R&f_TPR=r86400&f_JT=F&f_WT=2&f_E=3%2C4&position=1&pageNum=0']

    def parse(self, response):

        #capture the total quantity of jobs for build the logic to get all Job Ids
        total_number_of_jobs = response.css(".results-context-header__job-count::text").get()
        try:
            total_number_of_jobs = int(total_number_of_jobs)
        except:
            # to avoid simbol "+"" with number when have more than 10 k as result (2.7 hours scraping for each 1000 jobs)
            total_number_of_jobs = 1000

        #each page can show 25 jobs, so we can calculate how many pages we will need to get
        total_number_of_pages_disponible = total_number_of_jobs / 25
        total_number_of_pages_disponible = math.ceil(total_number_of_pages_disponible)

        #create a list that have all start pages as possibles, 25 by 25, depending of all jobs are disponible in search link (ex if we have 100 total number of jobs, this list will be [0,25,50,75,100])
        list_of_start_number_disponible = []
        for i in range(total_number_of_pages_disponible):
            list_of_start_number_disponible.append(i * 25)

        #get all job links disponible in an API link page
        for start_page in list_of_start_number_disponible:
            #24 full time
            url_to_search_all_links= response.urljoin(f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BScientist&location=Estados%2BUnidos&locationId=&geoId=103644278&sortBy=R&f_TPR=r86400&f_JT=F&f_WT=2&f_E=3%2C4&start={start_page}')
            
            yield scrapy.Request(url = url_to_search_all_links, callback=self.link_capture,meta={'dont_redirect': True, 'handle_httpstatus_list': [301, 302, 404, 503, 429], 'download_delay': 10})
            time.sleep(10)
        
    def link_capture(self, response):

        #this code will return a list with all links for each unique job that contains de job Id and name of position. We will extract this Job ID for acess the detailed information in next request
        link_job = response.css('a.base-card__full-link::attr(href)').getall()

        #Filter to get only the links that contain names of jobs like a target (Data Scientist and Machine Learning Engineer). This step is needed because the results have a lot of dirty data that doesn't match the target.
        key_word_ml = 'learning'
        key_word_ds = 'scientist'

        #check if a column contain a word
        ml_patern = re.compile(rf'\b{re.escape(key_word_ml)}\b', flags=re.IGNORECASE)
        ds_patern = re.compile(rf'\b{re.escape(key_word_ds)}\b', flags=re.IGNORECASE)

        df_links = pd.DataFrame(link_job)
        df_links.columns = ['links']
        #dataframe that has only targets positions searched
        df_target = df_links.loc[(df_links['links'].str.contains(ds_patern)) | (df_links['links'].str.contains(ml_patern))]

        #extract id from all links
        list_of_unique_id_jobs = []
        for l in range(len(link_job)):
            list_of_unique_id_jobs.append(re.findall(r'\d{10}', link_job[l])[0])
        
        #filter ids that have job names like the target
        unique_ids_filtered = []
        for i in range(len(df_target)):
            unique_ids_filtered.append(list_of_unique_id_jobs[df_target.index[i]])   

        #for each unique id, acess the details page and extract details info
        for id in unique_ids_filtered:
           url_to_search= response.urljoin(f'https://www.linkedin.com/jobs/view/{id}')

           yield scrapy.Request(url = url_to_search, callback=self.details_capture,meta={'dont_redirect': True, 'handle_httpstatus_list': [301, 302, 404, 503, 429], 'download_delay': 10})
           time.sleep(10)

        
    def details_capture(self, response):
        #get data and apply some text format
        title = response.css("h1.top-card-layout__title::text").getall()[0]
        location = response.css("span.topcard__flavor::text").getall()[2]
        company_name = response.css("a.topcard__org-name-link::text").get()
        position_name = response.css("h1.top-card-layout__title::text").get()
        experience_required = response.css("span.description__job-criteria-text::text").getall()[0]
        contract_type = response.css("span.description__job-criteria-text::text").getall()[1]
        function_name = response.css("span.description__job-criteria-text::text").getall()[2]
        company_sector = response.css("span.description__job-criteria-text::text").getall()[3]
        link_searched = response.url
        description = response.css("div.show-more-less-html__markup /*p::text").getall() 

        data = {
        'title': title,
        'location': location,
        'company_name': company_name,
        'position_name': position_name,
        'experience_required': experience_required,
        'contract_type': contract_type,
        'function_name': function_name,
        'company_sector': company_sector,
        'description': description,
        'link': link_searched,
        'now_datetime': [datetime.datetime.now()]  # wrap in list to create one row
        }

        df = pd.DataFrame(data)

        #save data in BigQuery table
        project_id = 'teste-315517'
        bigquery_client = bigquery.Client(project=project_id)
        table_id = 'teste-315517.teste.raw_from_linkedin'
        
        #transform everything in string for avoid problemns in bigquery writing
        df = df.astype(str)

        job = bigquery_client.load_table_from_dataframe(
        df, table_id)

        time.sleep(10)