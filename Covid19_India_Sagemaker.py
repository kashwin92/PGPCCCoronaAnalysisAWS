import datetime, time
import os
import subprocess
import boto3


def covid_india():
    subprocess.run('kaggle datasets download -d sudalairajkumar/covid19-in-india',shell=True)
    subprocess.run('mv covid19-in-india.zip covid_raw/',shell=True)
    os.chdir('/opt/covid_raw')
    subprocess.run('unzip covid19-in-india.zip',shell=True)
    os.remove('AgeGroupDetails.csv')
    os.remove('HospitalBedsIndia.csv')
    os.remove('ICMRTestingLabs.csv')
    os.remove('IndividualDetails.csv')
    os.remove('StatewiseTestingDetails.csv')
    os.remove('population_india_census2011.csv')
    os.remove('covid19-in-india.zip')
    os.chdir('/opt')
    subprocess.run('mv covid_raw/covid_19_india.csv .',shell=True)

def push_to_s3():
    s3 = boto3.client('s3')
    s3.upload_file('covid_19_india.csv', 'ash0192-india-data', 'covid_19_india.csv')


covid_india()
push_to_s3()
