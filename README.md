# LinkedIn-scrap
Scraping details of jobs and developing a personal filter for better matches  
Link to solution: https://job-analyser.streamlit.app/ 

- [About](#About)
- [Files in the repository](#Files-in-the-repository)
- [Questions that helped with the architecture and scope phase](#Questions-that-helped-with-the-architecture-and-scope-phase)


# About

* Used in this solution:  
Scrapy | nltk | Spacy | google cloud function | google workflows | Streamlit |    
NLP | Ruled-based extraction entities (NER)   

* Context:   
Given the significant number of jobs on the LinkedIn site, it isn't easy to do an accurate search.  
The search needs to be more precise, even with the site's filters.  
With this, we captured this data to develop more precise ways of searching for the perfect match job.  

* Solution:  
Scrap all job data on the LinkedIn site automatically. 
After collecting the data, use a filter strategy to optimize the search.  

* Challenge:  
There is not a single page with all opportunities.  
The generation of new content is automatically generated by scrolling through JAVASCRIPT.  
JAVASCRIPT generates the detailed content of each job after clicking on each unique opportunity.  

* Strategy adopted:    
It was possible to capture the API link triggered with the mouse scroll.  
This avoided the need for more robust technologies, such as selenium.  
With this, it was possible to go through all the job pages that contained the generic information of each job.  
With the captured generic information, it was possible to capture the unique ID of each job.  
With the unique ID of each job, it was possible to access a detail page from where all the project information was extracted.  
Personalized NER using spacy and nltk library was used to extract valuable entities from the description and make them a field to apply filters.    


* Architecture and operation flowchart:  
The arctechture choiced was google GCP.  
For processing the scrapy library and all Python processes and treatment, the google cloud function, a serverless solution, was used to run the pipeline.  
The cloud function was started and scheduled by workflows programmed to start the scrapy pipeline once daily.  
Cloud function was set to save the scraped data and entities extracted in the big query database already cleaned.  
The app used here for deployment was streamlit, which access big query to get the data already processed and show it to the final user.  
The final user can access all the data scraped and apply several filters to improve your search job.  
A technique of spacing requests every 10 seconds was used to avoid the necessity to use proxy services.  
In this way, the total daily processing time cost generated a lower price than hiring a proxy provider service guaranteeing the scraping of all data needed.  

![alt text](https://github.com/lucasvascrocha/LinkedIn-scrap/blob/main/LinkedIn_03.jpg)   


# Files in the repository
Repository structure:

- app
  - .steamlit  
    - config.toml  
  - images 
    - 01.jpg  
  - mypages  
    - historical_page.py
    - how_it_works.py
  - utils  
    - functions.py
    - login.py
    - style.py
  - .gitignore 
  - App.py
  - Procfile
  - README.md
  - requirements.txt
  - setup.sh
- google-cloud
  - analysis.ipynb
  - linkedin.py
  - main.py
  - personalized_ner.py
  - personalized_ner.jsonl
  - linkedin_requirements.txt
  - personalized_ner_requirements
- jobsearch
  - jobsearch
    - spiders
        - __init__.py
        - linkedin.py
    - __init__.py
    - items.py
    - middlewares.py
    - pipelines.py
    - settings.py
  - scrapy.cfg
- .gitignore
- README.md
- requirements.txt

* NER analyze example:  

![alt text](https://github.com/lucasvascrocha/LinkedIn-scrap/blob/main/LinkedIn_04.jpg)   


# Questions that helped with the architecture and scope phase

### **Step 1:** Define your data requirements

### ****The business need****

1. **What is your business goal, what are you trying to achieve?**
    
    The goal is to have data from the jobs posted on LinkedIn daily that are most related to my claims to sort out the most relevant ones and save time on applications.  
    
2. **How can web data play a role in achieving this goal?**
    
    LinkedIn is a site that carries the job openings of companies with a lot of information, and having a more accurate filter of what is relevant would optimize a candidate's time.  
    
3. **What type of web data do you need? From which websites would you like to obtain this data?**
    
    Tabular data brings information about job opportunities—LinkedIn website. 
    
4. **How will you use this data to achieve your business goals?**
    
    With the data collected, it will be possible to analyze and understand the patterns of vacancies that have the most to do with each application objective. With this, it will be possible to classify the opportunities from the most relevant to the least appropriate.  
    
5. **How often would you like to extract this data? Daily, weekly, monthly, once-off, etc.?**
    
    Daily.  
    
6. **How do you want to consume the data?**
    
    In a structured table.  
    
7. **How will you verify that the extracted data is accurate? i.e. matches exactly the data on the target websites?**
    
    They are manually checking a few samples through manual random sample arrivals.  
    
8. **How would you like to interact with the solution? i.e would you just like to receive data at a predefined frequency, or would you like to have control over the entire web scraping infrastructure and the associated source code?**
    
    I want to receive a daily table with the opportunity fields extracted in a structured way that makes it possible to apply filters. In addition to sorting the opportunities by order of relevance to each application goal.  
    

### ****Technical requirements****

### Data discovery

1. **Do you know which sites have suitable data to extract?**
    
    Yes, LinkedIn site.  
    
2. **How will the crawler navigate to the data? I.e. how will be crawler find the data on the website.**
    
    Through the Jobs page, you can access all the necessary information.  
    
3. **Do you need to login to access the desired data?**
    
    No login is needed.
    
4. **Do you need to input any data to filter the data on the website before extraction?**
    
    Yes.
    
5. **Do you need to access this website from a certain location to see the correct data?**
    
    No need.
    

### Data extraction

 ![alt text](https://github.com/lucasvascrocha/LinkedIn-scrap/blob/main/LinkedIn_01.jpg)  
 ![alt text](https://github.com/lucasvascrocha/LinkedIn-scrap/blob/main/LinkedIn_02.jpg)  

1. **What data fields do I want extracted?**  
    1. job title  
    2. Time of posting  
    3. Location  
    4. Experience level  
    5. Job type  
    6. Function  
    7. Sectors  
    8. Show more   
2. **Do I want to extract any images on the page?**  
    No  
3. **Do I want to download any files (PDFs, CSVs, etc)?**  
    No  
4. **Do I want to take a screenshot of the page?**  
    No  
5. **Do I need the data formatted into a different format (e.x. the currency signs removed from product prices)?**  
    No  
6. **Is all the desired data available on a single web page?**  
    Yes  

### Extraction scale

1. **Number of websites**
    
    One
    
2. **Number of records being extracted from each website**
    
    +- 150 rows per target per day we will have +- 100 targets, so 15,000 rows per day
    
3. **Frequency of the data extraction crawls**
    
    1. Daily  
    2. Window:  in the end of the day will be good  
    
4. **Deltas & incremental crawls**
Extract only data that match with pre defined filter  
    1. Extract all the available data every single time the site is crawled?  
        No  
    2. Only extract the deltas or changes to the data available on the website.?  
        Yes  
    3. Extract and monitor all the changes that occur to the available data (data changes, new data, data deletions, etc.).?  
        No    
        

### Data output

how do you want to interact with the web scraping solution along with how do you want the data delivered?

- **Data Formats** - CSV
- **Data Delivery -** GCP BigQuery

### **Step 2:** Conduct a legal Review

1. **Personal data** - will your web scraping project require you to extract personal data? If yes, where do these people reside? Are you complying with the local regulations? GDPR comes to mind.
    
    No.
    
2. **Copyrighted data** - is the data being extracted subject to copyright? If so, are there any exceptions to copyright that you may avail of ex (Articles,Videos,Pictures,Stories,Music,Databases)
    
    No.
    
3. **Database data** - a subset of copyright, does the website the data is being extracted from have database rights?
    
    No.
    
4. **Data behind a login** - to extract the data do you need to scrape behind a login? What do the website’s terms and conditions state regarding web scraping?
    
    No.
    

### **Step 3:** Evaluate the technical Feasibility

### Data discovery

The first step of the technical feasibility process is investigating whether it is possible for your crawlers to accurately discover the desired data as defined in the project requirements.

1. **you know which websites contain your desired data?**
    
    Yes.
    
2. **can you filter the data on the target websites to only extract the desired data?**
    
    Yes
    

### Data extraction

1. **JavaScript/AJAX -** as modern websites are increasingly using JavaScript and AJAX to dynamically display data on web pages there might be a requirement to use a headless browser to render this data for the crawlers or develop custom code to execute parts of the JavaScript without using a headless browser. The solution architect will run a series of tests to determine if the target data is rendered using JavaScript or AJAX.
    
    The target website use **JavaScript/AJAX.** but we can use the API that renders the information.  
    
2. **The number of steps required to extract the data -** in some cases all the target data isn’t available on a single page, instead, it requires the crawler to make multiple requests to obtain the data. In cases like these, the solution architect will determine the number of requests that will need to be made which will determine the amount of infrastructure the project will require.
    
    (one page for checking all unique opportunities) + (JavaScript API for getting a unique ID for each job) + (personal page with detailed info about each job)
    
    1 + 1 + 1 = 3 requests for each job ID information, usually LinkedIn can bring 100 jobs information per day for the filter needed, so 100*3 = 300 requests/day  
    
3. **The complexity of iterating through records -** certain sites have more complex pagination (infinite scrolling pages, etc.) or formatting structures that can require a headless browser or complex crawl logic. The solution architect will determine the type of pagination and crawl logic required to access all the available records.
    
    In this case, it will be necessary to use API generated by scroll to iterate through all pages.  
    
4. **Data validation -** a key component to every web scraping project is maintaining high data quality and coverage. As a result, before the project event starts our solution architect will make an assessment of the complexity of guaranteeing perfect data quality and coverage as the project scales.
Manually checking a few samples. And some logic metrics can be applied to guaranty the match.

5. **Difficulty to maintain -** not only will the solution architect evaluate the difficulty of extracting the target data for the current website, but they will also look at the website's history and the trends in that industry to determine the likelihood of disruptive website changes occurring that would break the crawlers.

### Extraction scale

1. **Test Crawls -** our solution architect will typically run a series of test crawls to investigate whether there will be any bottlenecks regarding maximum crawl speeds. This can often be an issue for smaller websites or when the project requires a tight time window to complete the data extraction but there is a risk it could overload the site's servers (for example hourly crawls).  
    Since the low necessity of updates will be applied, a time sleed in the code to minimize the timing between requests.

2. **Anti-Bot Countermeasures -** our solution architect will run the target websites through our internal analysis tools to identify the presence of any anti-bot countermeasures, captchas, or CDNs that will increase the complexity of the project and limit the potential to extract the data at the required scale or frequency. The presence of these technologies can increase the risks of bans or reliability issues.

### Data output

1. **Needs to developed a personalized API?**
    
    No
    
2. **Need to use Data Science for work on data before the delivery?**
    
    Yes
    

### **Step 4:** Architect a solution & estimate resources

1. **Crawler architecture - data discovery and extraction architecture spiders.**
    
    You may need to run the data discovery crawler daily to capture the available jobs created in the last 24 hours. After pulling up this list, it may be possible to extract the information from each of them with the data extraction crawler.  
    
2. **Spider deployment**
    
    It will be deployed in an On-premise client server.
    
3. **Proxy management**
    
    It will not be necessary for the POC. The strategy will be to get time sparse requests to be unnoticed. But in the future, if these updates request changes, this will need to be reviewed.  
    
4. **Headless browser requirements**
    
    No need.
    
5. **Data quality assurance**
    
    Manually.
    
6. **Maintenance requirements**
    
    Some analysis after two months of running.
    
7. **Data post-processing**
    
    Need to build URL logic, search logic and match logic.  
    
8. **Any non-standard technologies that might be required**  
