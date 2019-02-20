# -*- coding: utf-8 -*-
import re
import demjson
import urllib3
from bs4 import BeautifulSoup
import time


class Parse:
    '''
    解析网页信息
    '''

    def __init__(self, htmlCode):
        self.htmlCode = htmlCode
        self.json = demjson.decode(htmlCode)
        pass

    def parseTool(self, content):
        '''
        清除html标签
        '''
        if type(content) != str: return content
        sublist = ['<p.*?>', '</p.*?>', '<b.*?>', '</b.*?>', '<div.*?>', '</div.*?>',
                   '</br>', '<br />', '<ul>', '</ul>', '<li>', '</li>', '<strong>',
                   '</strong>', '<table.*?>', '<tr.*?>', '</tr>', '<td.*?>', '</td>',
                   '\r', '\n', '&.*?;', '&', '#.*?;', '<em>', '</em>']
        try:
            for substring in [re.compile(string, re.S) for string in sublist]:
                content = re.sub(substring, "", content).strip()
        except:
            raise Exception('Error ' + str(substring.pattern))
        return content

    def parsePage(self):
        '''
        解析并计算页面数量
        :return: 页面数量
        '''

        totalCount = self.json['content']['positionResult']['totalCount']  # 职位总数量
        resultSize = self.json['content']['positionResult']['resultSize']  # 每一页显示的数量
        pageCount = int(totalCount) // int(resultSize) + 1  # 页面数量
        return pageCount

    def parseInfo(self):
        '''
        解析信息
        '''
        info = []
        for position in self.json['content']['positionResult']['result']:
            i = {}
            id = position['positionId']
            url = 'https://www.lagou.com/jobs/'+str(id)+'.html'
            print('url',url)
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            soup = BeautifulSoup(response.data)
            rawdetail = soup.find("div", class_="job-detail")
            detailinfo = ""
            if rawdetail!= None:
                detailinfo = rawdetail.get_text()
                detailinfo = detailinfo.replace('   ', '')
                detailinfo = detailinfo.replace(' ', '')
                detailinfo = detailinfo.replace('\n', '')


            rawaddr = soup.find("div", class_="work_addr")
            addrinfo = ""
            if rawaddr!= None:
                addrinfo = rawaddr.get_text()
                addrinfo = addrinfo.replace('   ', '')
                addrinfo = addrinfo.replace(' ', '')
                addrinfo = addrinfo.replace('\n', '')
            i['companyName'] = position['companyFullName']
            i['companyShortName'] = position['companyShortName']
            i['companySize'] = position['companySize']
            i['createTime'] = position['createTime']
            i['companyDistrict'] = position['district']
            i['positionEducation'] = position['education']
            i['companyStage'] = position['financeStage']
            i['positionType'] = position['firstType']
            i['companyType'] = position['industryField']
            i['jobNature'] = position['jobNature']
            i['positionAdvantage'] = position['positionAdvantage']
            i['positionLables'] = position['positionLables']
            i['positionName'] = position['positionName']
            i['positionSalary'] = position['salary']
            i['secondType'] = position['secondType']
            i['skillLables'] = position['skillLables']
            i['thirdType'] = position['thirdType']
            i['positionWorkYear'] = position['workYear']
            i['positionDetail'] = detailinfo
            i['positionAddress'] = addrinfo
            info.append(i)
            time.sleep(3)
        return info
