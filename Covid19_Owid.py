import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import boto3
import ssl
import requests
import xlrd
import schedule
import time

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def covid19_owid():
    url = "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.xlsx"
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    r = requests.get(url, allow_redirects=True)
    open('covid19_owid.xlsx', 'wb').write(r.content)

    fl = "covid19_owid.xlsx"
    workbook = xlrd.open_workbook(fl)
    sheet = workbook.sheet_by_index(0)

    head = []
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            head.append(sheet.cell_value(row,col))
        with open("covid19_owid.txt", 'a') as text_file:
            for item in head:
                text_file.write(str(item)+",")
            text_file.write("\n")
        del head[:]


def push_to_s3():
    s3 = boto3.client('s3')
    s3.upload_file('covid19_owid.txt', 'ash0192-owid-data', 'covid19_global.txt')


covid19_owid()
push_to_s3()