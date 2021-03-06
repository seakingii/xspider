#coding=utf-8
from b2.stop2 import StopWords
import urllib
__ALL__ = [ "get_url_site"]

_url_protocols = StopWords(words = ["http://" , "https://" , "ftp://"] ) 

__all__ = ["get_url_protocol" ,"get_url_site","get_default","parse","urljoin"]
def get_url_protocol(url):
    """得到链接的http协议
        param:url:basestring:链接
        return:protocol:basestring:链接协议
        exception:unsupport type:TypeError:如果url不为字符串，则抛出异常
        Test:
            >>> get_url_protocol("https://wwww.baidu.com/")
            'https://'
            >>> get_url_protocol("https://githuber.cn/search?location=china")
            'https://' 
    """
    value , msg = _url_protocols.startswith(url.lower())
    return msg if value else None

def get_url_site(url):
    """得到链接站点 ， 主要是第一个/切分
        param:url:basestring:链接 
        return:site:basestring:链接的所属站点
        exception:unsupport type:TypeError:如果url不为字符串，则抛出异常
        Test:
            >>> get_url_site("http://www.test.com/index.php")
            'www.test.com'
            >>> get_url_site("https://githuber.cn/people")
            'githuber.cn'
            >>> get_url_site("123.12.21.0:81/look") 
            '123.12.21.0:81'
    """
    if url and isinstance(url,basestring):
        url = url.lower()
        value , msg = _url_protocols.startswith(url)
        url = url[value:] if value else url    
        return url.split("/")[0]
    else:
        raise TypeError("extact url site get unsupport type {} value {}".format(type(url).__name__,url))
    return None 



def join_url(parrent_protocol,parrent_site  , url):
    """站点进行补全操作
        param:parrent_protocol:basestring:前链协议头
        param:parrent_site:basestring:前链站点
        param:url:basestring:链接
        return:url:basestring:补全后的链接
        Test:
            >>> join_url("https://","githuber.cn","/people/10704521")
            'https://githuber.cn/people/10704521'
    """
    url_site = get_url_site(url)
    protocol = get_url_protocol(url)
    # 只有路径的
    if url_site == "":
        return "{protocol}{site}{url}".format(protocol = parrent_protocol ,site = parrent_site , url = url)
    # 有站点,但无协议头 
    if protocol is None:
        return "{protocol}{url}".format(protocol = parrent_protocol , url = url)
    return url



def parse(url):
    """解析链接
        param:link:basestring:链接
        return:protocol:basestring:链接协议头
        return:site:basestring:链接站点
        return:path:basestring:链接主体
        return:params:dict:链接参数
        Test:
            >>> parse("https://buyiker.com/test.html?page=1")
            ('https://', 'buyiker.com', '/test.html', {'page': '1'})
            >>> parse("buyiker.com/test.html")
            (None, 'buyiker.com', '/test.html', {})
            >>> parse("buyiker.com")
            (None, 'buyiker.com', '', {})
    """
    protocol = get_url_protocol(url)
    site = get_url_site(url)
    param_index = url.find("?")
    param_index = param_index if param_index != -1 else len(url)
    path_index = (len(protocol) if protocol else 0 ) + (len(site) if site else 0)
    path = url[path_index:param_index]
    param_dict = {}
    param_value = None 
    if param_index < len(url):
        param_value = url[param_index + 1:]
        for param in param_value.split("&"):
            key,value = param.split("=") 
            param_dict[key] = value
    return protocol,site,path,param_dict

def get_default(value , default_value):
    if value is None:
        return default_value
    return value

def urljoin(protocol,site,path,param_dict):
    """组合解析出来的链接
        param:protocol:bastring:链接协议头
        param:site:basestring:链接站点
        param:path:bastring:链接路径
        param:param_dict:dict:链接参数
        return:url:bastring:组合后的链接
        Test:
            >>> urljoin(*parse("https://buyiker.com/test.html?page=1"))
            'https://buyiker.com/test.html?page=1'
    """
    param_value = None
    if param_dict and len(param_dict) > 0:
        param_value = "?%s" % urllib.urlencode(param_dict)
    return "{protocol}{site}{path}{param_value}".format(
                protocol = get_default(protocol,""),
                site = get_default(site,""),
                path = get_default(path,""),
                param_value = get_default(param_value,""))
