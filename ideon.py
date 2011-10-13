#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Use the APIs provided by http://www.trafiklab.se
to get the busses departuring from Lund Ideon
towards malmö

Malmö Konserthuset
7415747

Lund Ideon
7421814

Lund Scheeleparken
7416946

Lund Norra Tpl
7422978
"""

import urllib2
#from BeautifulSoup import BeautifulSoup
from string import Template
import json
import time

def printheader(word):
    '''generate a nice header string'''
    out.write("\n%s\n%s\n" % (word, '-' * len(word)))

class Buss:
    def __init__(self):
        with open('key.txt') as fd:
            self.key=fd.read().strip()
        self.request_169={
           'FORMAT':'json',
           'API_KEY':self.key,
           'FROM_ID':'7421814',
           'TO_ID': '7415747',
           'SEARCH_TYPE':'F'
           }
        self.request_171={
           'FORMAT':'json',
           'API_KEY':self.key,
           'FROM_ID':'7416946',
           'TO_ID': '7415747',
           'SEARCH_TYPE':'F'
           }
        self.request_1={
           'FORMAT':'json',
           'API_KEY':self.key,
           'FROM_ID':'7422978',
           'TO_ID': '7415747',
           'SEARCH_TYPE':'F'
           }
        self.Q={
            '171':self.request_171,
            '169':self.request_169,
            '1':self.request_1,
            }

        self.url_template=Template(r'https://api.trafiklab.se/samtrafiken/resrobot/Search.$FORMAT?key=$API_KEY&searchType=$SEARCH_TYPE&fromId=$FROM_ID&toId=$TO_ID&coordSys=RT90&apiVersion=2.1')

    def get_tt(self,bus='169'):

        """get timetable
        """
        request=self.url_template.safe_substitute(self.Q[bus])
        f=urllib2.urlopen(request)
        page=f.read()
        f.close()
        j=json.loads(page)

        for i in j['timetableresult']['ttitem']:
            try:
                my_buss=i['segment']['segmentid']['carrier']['number']
                my_from=i['segment']['departure']['location']['name']
                my_departure_time=i['segment']['departure']['datetime'].split()[1]
                my_to=i['segment']['arrival']['location']['name']
                my_arrival_time=i['segment']['arrival']['datetime'].split()[1]
                print "%3s %-20s %s %s %s" % (my_buss, my_from, my_departure_time, my_to, my_arrival_time)
            except:
                pass

    def pp(self, table):
        """pretty print timetable
        """
        pass

    def show(self):
        """pp
        """
        pass

def main():
    """main
    """
    b=Buss()
    t1=time.time()
    b.get_tt('169')
    b.get_tt('171')
    b.get_tt('1')

    t2=time.time()
    print '\nrequest finished in:', round(t2-t1,3)

if __name__=='__main__':
    main()
