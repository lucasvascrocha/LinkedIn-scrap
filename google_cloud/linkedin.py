import scrapy
import re
import math
import pandas as pd
import time
import datetime
from google.cloud import bigquery

class ExempleSpider(scrapy.Spider):
    name = 'linkedin'
    # 24 hours ago full time
    start_urls = [
        'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&'
        'location=Estados%20Unidos&locationId=&geoId=103644278&sortBy=R&'
        'f_TPR=r86400&f_JT=F&f_WT=2&f_E=3%2C4&position=1&pageNum=0'
    ]
    def parse(self, response):
        # capture the total quantity of jobs
        total_number_of_jobs = response.css(
            ".results-context-header__job-count::text"
            ).get()
        try:
            total_number_of_jobs = int(total_number_of_jobs)
        except ImportError:
            total_number_of_jobs = 1000

        # Calculate how many pages we will need to get
        total_number_of_pages_disponible = total_number_of_jobs / 25
        total_number_of_pages_disponible = math.ceil(
            total_number_of_pages_disponible
            )

        # Create a list that have all start pages as possibles, 25 by 25
        list_of_start_number_disponible = []
        for i in range(total_number_of_pages_disponible):
            list_of_start_number_disponible.append(i * 25)

        # Get all job links disponible in an API link page
        list_of_start_number_disponible = [0, 25, 50, 75, 100, 125, 150]
        for start_page in list_of_start_number_disponible:
            url_to_search_all_links = response.urljoin(
                f'https://www.linkedin.com/jobs-guest/jobs/api'
                f'/seeMoreJobPostings/search?keywords=Data%2BScientist'
                f'&location=Estados%2BUnidos&locationId=&geoId=103644278&'
                f'sortBy=R&f_TPR=r86400&f_JT=F&f_WT=2&f_E=3%2C4&start'
                f'={start_page}'
            )
            yield scrapy.Request(
                url=url_to_search_all_links,
                callback=self.link_capture,
                meta={
                    'dont_redirect': True,
                    'handle_httpstatus_list': [301, 302, 404, 503, 429],
                    'download_delay': 10
                }
            )
            time.sleep(10)
        
    def link_capture(self, response):
        # Extract Job ID from links for acess the detailed information.
        link_job = response.css('a.base-card__full-link::attr(href)').getall()

        # Filter to get only target jobs.
        key_word_ml = 'learning'
        key_word_ds = 'scientist'

        # Check if a column contain a word
        ml_patern = re.compile(
            rf'\b{re.escape(key_word_ml)}\b', flags=re.IGNORECASE
            )        
        ds_patern = re.compile(
            rf'\b{re.escape(key_word_ds)}\b', flags=re.IGNORECASE
            )

        df_links = pd.DataFrame(link_job)
        df_links.columns = ['links']
        df_target = df_links.loc[
            (df_links['links'].str.contains(ds_patern)) |
            (df_links['links'].str.contains(ml_patern))
            ]
        # Extract id from all links
        list_of_unique_id_jobs = [
            re.findall(r'\d{10}', link)[0] for link in link_job
            ]
        # Filter ids that have job names like the target
        unique_ids_filtered = [
            list_of_unique_id_jobs[i] for i in df_target.index
            ]
        # For each unique id, acess the details page and extract details info
        for unique_id in unique_ids_filtered:
            url_to_search = response.urljoin(
               f'https://www.linkedin.com/jobs/view/{unique_id}'
            )
            yield scrapy.Request(
                    url=url_to_search,
                    callback=self.details_capture,
                    meta={
                        'dont_redirect': True,
                        'handle_httpstatus_list': [301, 302, 404, 503, 429],
                        'download_delay': 10
                    }
                )
            time.sleep(10)

    def details_capture(self, response):
        # Get data and apply some text format
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
            'now_datetime': [datetime.datetime.now()] 
        }

        df = pd.DataFrame(data)

        # Save data in BigQuery table
        project_id = 'teste-315517'
        bigquery_client = bigquery.Client(project=project_id)
        table_id = 'teste-315517.teste.raw_from_linkedin'
        df = df.astype(str)
        bigquery_client.load_table_from_dataframe(
            df, table_id
        )
        time.sleep(10)