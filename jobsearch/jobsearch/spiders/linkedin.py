import scrapy
import time
import re


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    #allowed_domains = ['www.linkedin.com']
    #start_urls = ['https://www.linkedin.com/jobs/search?keywords=Data%20Scientist"&"location=Estados%20Unidos"&"locationId="&"geoId=103644278"&"f_TPR=r86400"&"f_JT=C%2CF"&"f_E=4"&"f_WT=2"&"position=1"&"pageNum=0']
    start_urls = ['https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Estados%20Unidos&locationId=&geoId=103644278&f_TPR=r86400&f_JT=C%2CF&f_E=4&f_WT=2&position=1&pageNum=0']


    def parse(self, response):
        
        links = response.css("a.base-card__full-link::attr(href)").getall()
        #capturing all JobIds in url link
        all_ids = []
        for l in links:
            unique_id = re.findall(r'\d{10}', l)[0]
            all_ids.append(unique_id)

        for id in all_ids:
           time.sleep(3)

           url_to_search= response.urljoin(f'https://www.linkedin.com/jobs/view/{id}')

           yield scrapy.Request(url = url_to_search, callback=self.parse_capture)

        #url_to_search= response.urljoin(f'https://www.linkedin.com/jobs/view/{all_ids[0]}')

        #yield scrapy.Request(url = url_to_search, callback=self.parse_capture)
        #yield scrapy.Request(url = 'https://www.linkedin.com/jobs/view/3338538962', callback=self.parse_capture)
    def parse_capture(self, response):

        title = response.css("h1::text").get(),
        location = response.css("span.topcard__flavor::text").getall()[2],
        company_name = response.css("a.topcard__org-name-link::text").get(),
        position_name = response.css("h1.top-card-layout__title::text").get(),
        experience_required = response.css("span.description__job-criteria-text::text").getall()[0],
        contract_type = response.css("span.description__job-criteria-text::text").getall()[1],
        function_name = response.css("span.description__job-criteria-text::text").getall()[2],
        company_sector = response.css("span.description__job-criteria-text::text").getall()[3],
        description = response.css("div.show-more-less-html__markup /*p::text").getall()

        yield{
            'title': title,
            'location': location,
            'company_name':company_name,
            'position_name': position_name,
            'experience_required': experience_required,
            'contract_type': contract_type,
            'function_name': function_name,
            'company_sector': company_sector,
            'description': description
        }
