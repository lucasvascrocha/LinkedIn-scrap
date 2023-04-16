import subprocess

def hello_http(request):
    command = f'scrapy runspider my_spider.py -O results.json'
    output = subprocess.check_output(command, shell=True)
    return output.decode()