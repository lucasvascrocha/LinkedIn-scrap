import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse

class LinkedInJobsSpider(scrapy.Spider):
    name = 'linkedin_jobs'
    allowed_domains = ['linkedin.com']
    start_urls = ['https://www.linkedin.com/jobs/search?location=United%20States']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            # Scroll down to load more job listings
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                # Check if 'Show More' button is present and click it
                show_more_button = self.driver.find_element_by_xpath('//button[contains(text(), "Show More")]')
                show_more_button.click()
            except:
                break
        source = self.driver.page_source
        response = HtmlResponse(url=response.url, body=source, encoding='utf-8')
        for job_card in response.css('.job-card'):
            yield {
                'title': job_card.css('.job-card-container h3 a span::text').get(),
                'company': job_card.css('.job-card-container h4 a span::text').get(),
                'location': job_card.css('.job-card-container h4 span:nth-child(3)::text').get(),
                'description': job_card.css('.job-card-container p span::text').get(),
            }

    def __del__(self):
        self.driver.close()
