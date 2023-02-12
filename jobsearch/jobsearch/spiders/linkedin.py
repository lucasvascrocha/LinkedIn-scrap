import scrapy
import time
import re
import math


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    #allowed_domains = ['www.linkedin.com']

    # Data Scientist - last week - contractor and temp - mid level and senior - remote
    # https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=Estados%20Unidos&locationId=&geoId=103644278&f_TPR=r604800&f_JT=C%2CT&f_E=4&f_WT=2&position=1&pageNum=0
    # https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist"&"location=Estados%20Unidos"&"locationId="&"geoId=103644278"&"f_TPR=r604800"&"f_JT=C%2CT"&"f_E=4"&"f_WT=2"&"position=1"&"pageNum=0
             
    #Get all ids
    # 1 week = f_TPR=r604800   
    # 24 hours ago = f_TPR=r86400      
    start_urls = ['https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=Estados%20Unidos&locationId=&geoId=103644278&f_TPR=r604800&f_JT=C%2CT&f_E=4&f_WT=2&position=1&pageNum=0']

    def parse(self, response):

        #capture the total quantity of jobs for build the logic to get all Job Ids
        total_number_of_jobs = response.css(".results-context-header__job-count::text").get()
        total_number_of_jobs = int(total_number_of_jobs)
        #each page can show 25 jobs, so we can calculate how many pages we will need to get
        total_number_of_pages_disponible = total_number_of_jobs / 25
        total_number_of_pages_disponible = math.ceil(total_number_of_pages_disponible)
        #create a list that have all start pages as possibles, 25 by 25, depending of all jobs are disponible in search link (ex if we have 100 total number of jobs, this list will be [0,25,50,75,100])
        list_of_start_number_disponible = []
        for i in range(total_number_of_pages_disponible):
            list_of_start_number_disponible.append(i * 25)
        #get all job links disponible in an API link page
        for start_page in list_of_start_number_disponible:
           url_to_search_all_links= response.urljoin(f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BScientist&location=Estados%2BUnidos&locationId=&geoId=103644278&f_TPR=r604800&f_JT=C%2CT&f_E=4&f_WT=2&start={start_page}')

           yield scrapy.Request(url = url_to_search_all_links, callback=self.link_capture)
        
    def link_capture(self, response):

        #this code will return a link for each unique job that contains de job Id. We will extract this Job ID for use later
        link_job = response.css('a.base-card__full-link::attr(href)').getall()

        #extract id from link
        list_of_unique_id_jobs = []
        for l in range(len(link_job)):
                list_of_unique_id_jobs.append(re.findall(r'\d{10}', link_job[l])[0])

        #for each unique id, acess the details page and extract details info
        for id in list_of_unique_id_jobs:
           time.sleep(2)

           url_to_search= response.urljoin(f'https://www.linkedin.com/jobs/view/{id}')

           yield scrapy.Request(url = url_to_search, callback=self.details_capture)

        
    def details_capture(self, response):

        #get data and apply some text format
        title = response.css("h1.top-card-layout__title::text").getall()[0].replace("\n", "").strip(),
        location = response.css("span.topcard__flavor::text").getall()[2].replace("\n", "").strip()
        company_name = response.css("a.topcard__org-name-link::text").get().replace("\n", "").strip()
        position_name = response.css("h1.top-card-layout__title::text").get().replace("\n", "").strip()
        experience_required = response.css("span.description__job-criteria-text::text").getall()[0].replace("\n", "").strip()
        contract_type = response.css("span.description__job-criteria-text::text").getall()[1].replace("\n", "").strip()
        function_name = response.css("span.description__job-criteria-text::text").getall()[2].replace("\n", "").strip()
        company_sector = response.css("span.description__job-criteria-text::text").getall()[3].replace("\n", "").strip()
        link_searched = response.url

        description = response.css("div.show-more-less-html__markup /*p::text").getall() 
        clean = re.compile('<.*?>')
        description = re.sub(clean, '', description[0]).replace('\n','').strip()


        yield{
            'title': title[0],
            'location': location,
            'company_name':company_name,
            'position_name': position_name,
            'experience_required': experience_required,
            'contract_type': contract_type,
            'function_name': function_name,
            'company_sector': company_sector,
            'description': description,
            'link': link_searched
        }
    