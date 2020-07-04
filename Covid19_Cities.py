import datetime,time
import schedule
import requests
import boto3


def covid19_pull():
    url = "https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv"
    r = requests.get(url, allow_redirects=True)
    open('covid19_city.txt', 'wb').write(r.content)


def covid19_cities():
    tday = datetime.date.today()
    tdelta1 = datetime.timedelta(days=2)
    tdelta3 = datetime.timedelta(days=1)
    yday = tday - tdelta1
    rday = tday - tdelta3
    tst1 = str(yday).split("-")
    tst3 = str(tday).split("-")
    tst4 = str(rday).split("-")
    fday1 = tst1[1]+'/'+tst1[2]+'/'+tst1[0]
    fday3 = tst3[1]+'/'+tst3[2]+'/'+tst3[0]
    fday4 = tst4[1]+'/'+tst4[2]+'/'+tst4[0]

    try:
        flag = 0
        f = open("covid19_city.txt", encoding="utf8")
        for ln in f:
            t = ln.split(",")
            if t[1] == fday1 or t[1] == fday3 or t[1] == fday4:
                if t[12] == "India" and len(t[13]) is not 0:
                    flag += 1
                else:
                    continue
            else:
                continue
    except:
        print("Total records for India is: {}".format(flag))

    fh = open("covid19_city.txt", encoding="utf8")

    try:
        for line in fh:
            l = line.split(",")
            if l[1] == fday1 or l[1] == fday3 or l[1] == fday4:
                if l[12] == "India" and len(l[13]) is not 0:
                    if l[13] == 'Uttar Pradesh':
                        stat = 'UttarPradesh'
                    elif l[13] == 'Himachal Pradesh':
                        stat = 'HimachalPradesh'
                    elif l[13] == 'West Bengal':
                        stat = 'WestBengal'
                    elif l[13] == 'Andhra Pradesh':
                        stat = 'AndhraPradesh'
                    elif l[13] == 'Andaman and Nicobar Islands':
                        stat = 'AndamanandNicobarIslands'
                    elif l[13] == 'Madhya Pradesh':
                        stat = 'MadhyaPradesh'
                    elif l[13] == 'Tamil Nadu':
                        stat = 'TamilNadu'
                    else:
                        stat = l[13]
                    if len(l[14]) is not 1:
                        dic = {
                            'id': l[0],
                            'updated': l[1],
                            'confirmed': l[2],
                            'confirmedchange': l[3],
                            'deaths': l[4],
                            'deathschange': l[5],
                            'recovered': l[6],
                            'recoveredchange': l[7],
                            'latitude': l[8],
                            'longitude': l[9],
                            'iso2': l[10],
                            'iso3': l[11],
                            'country': l[12],
                            'state': stat,
                            'city': l[14].rstrip()
                             }
                        with open('covid19_India_city.txt','a') as s3_file:
                            s3_file.write('{')
                            for k,v in dic.items():
                                if k == 'city':
                                    s3_file.write('"'+k+'"'+":"+'"'+v+'"')
                                else:
                                    if type(v) == str:
                                        s3_file.write('"'+k+'"'+":"+'"'+v+'"'+",")
                                    else:
                                        s3_file.write('"'+k+'"'+":"+v+",")
                            s3_file.write('},')
                        s3_file.close()
                else:
                    continue
            else:
                continue
    except:
        print("Done")


covid19_pull()
covid19_cities()