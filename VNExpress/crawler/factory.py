from .vnexpress import VNExpressCrawler

WEBNAMES = {"vnexpress": VNExpressCrawler}

def get_crawler(webname, **kwargs):
    crawler = WEBNAMES[webname](**kwargs)
    return crawler