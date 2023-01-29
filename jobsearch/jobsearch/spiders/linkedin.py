import scrapy
import time
import re


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    #allowed_domains = ['www.linkedin.com']
    #start_urls = ['https://www.linkedin.com/jobs/search?keywords=Data%20Scientist"&"location=Estados%20Unidos"&"locationId="&"geoId=103644278"&"f_TPR=r86400"&"f_JT=C%2CF"&"f_E=4"&"f_WT=2"&"position=1"&"pageNum=0']
    #start_urls = ['https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=Estados%20Unidos&locationId=&geoId=103644278&f_TPR=r86400&f_JT=C%2CT&f_E=4&position=1&pageNum=0']
    # 1 week = f_TPR=r604800               
    #need to add a scroll method for handle wirh javascript
    start_urls = ['https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=Estados%20Unidos&locationId=&geoId=103644278&f_TPR=r86400&f_JT=C%2CT&f_E=4&position=1&pageNum=2']
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

    def parse_capture(self, response):

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
    
