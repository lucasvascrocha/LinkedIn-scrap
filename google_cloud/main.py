import subprocess


def hello_http(request):
    """Executes a scrapy spider script via a subprocess and returns the output.

    Args:
        request (object): The request object that triggers the function.

    Returns:
        str: The output of the scrapy spider script execution, decoded to a string.
    """
    command = 'scrapy runspider my_spider.py'
    output = subprocess.check_output(command, shell=True)
    return output.decode()