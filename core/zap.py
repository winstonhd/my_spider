import re
import requests
from core.requester import requester
from core.utils import xmlParser
from core.colors import run, good


def zap(inputUrl, archive, domain, host, internal, robots):
    """从 robots.txt和sitemap.xml文件中提取链接"""
    # 请求 robots.txt 文件
    response = requests.get(inputUrl + '/robots.txt').text
    # 确保 robots.txt不是一些花哨的404页面
    if '<body' not in response:
        matches = re.findall(r'Allow:(.*)|Disallow:(.*)', response)
        if matches:
            # 循环遍历 matches，match在这里是一个元组
            for match in matches:
                # 一个item在match中总是空的所以将两者结合起来
                match = ''.join(match)
                # 如果这个URL没有使用通配符
                if '*' not in match:
                    url = inputUrl + match
                    # 添加这个URL到 internal 列表用于爬取
                    internal.add(url)
                    # 添加这个URL到robots列表
                    robots.add(url)
            print('%s URLs retrieved from robots.txt: %s' % (good, len(robots)))
    # 请求 sitema.xml文件
    response = requester.get(inputUrl + '/sitmap.xml').text
    # 确保 sitemap.xml 不是一些花哨的404页面
    if '<body' not in response:
        matches = xmlParser(response)
        if matches:  # 如果这里有匹配上了的
            print('%s URLs retrieved from sitemap.xml: %s' % (good, len(match)))
            for match in matches:
                # 添加 match 到 internal 列表用于爬取
                internal.add(match)



