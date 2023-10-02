# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsearchItem(scrapy.Item):
    """Storing information about individual Linkedin.

    Args:
        title (Field): 
        location (Field): 
        company_name (Field): 
        position_name (Field): 
        experience_required (Field): 
        contract_type (Field): 
        function_name (Field): 
        company_sector (Field): 
        description (Field): 
        link (Field): 
    """

    title = scrapy.Field()
    location = scrapy.Field()
    company_name = scrapy.Field()
    position_name = scrapy.Field()
    experience_required = scrapy.Field()
    contract_type = scrapy.Field()
    function_name = scrapy.Field()
    company_sector = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
