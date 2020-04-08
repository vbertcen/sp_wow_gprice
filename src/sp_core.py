# coding=utf-8
import requests
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import pymysql
from decimal import Decimal as d
from apscheduler.schedulers.blocking import BlockingScheduler

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116", }
dd373_url = 'https://www.dd373.com/s/eja7u2-0r2mut-haf682-vphv2u-0-0-jk5sj0-0-0-0-0-su-0-0-0.html'
uu898_url = 'http://www.uu898.com/newTrade.aspx?gm=1512&area=3631&srv=41836&cmp=60&c=-3&o=5&sa=0&p=1'
w7881_url = 'https://search.7881.com/list.html?pageNum=1&gameId=G5569&gtid=100001&carrierId=0&groupId=G5569P002&serverId=G5569P002031&mobileGameType=&faceId=&tradeType=&tradePlace=&shopSortTypeCode=1&sortType=orderbypriceunitasc&listSearchKeyWord=&mainSearchKeyWord=&minPrice=&maxPrice=&otherFilterValue=313346%3D%E8%81%94%E7%9B%9F&rentalByHourStart=&rentalByHourEnd=&propertiess=&chiledPropertiess=&platformId=&platformName=&order=&loginMethod=&rGameId=&tagName=&priceTag=&instock=false&quickChoose='

tmp = '1.单价：%s，售价：%s\n' \
      '2.单价：%s，售价：%s\n' \
      '3.单价：%s，售价：%s\n' \
      '4.单价：%s，售价：%s\n' \
      '5.单价：%s，售价：%s\n'
mail_host = "smtp.163.com"
mail_user = "vbertcenhz@163.com"
mail_pass = "NIPNFZBDAXPDZZEY"
sender = "vbertcenhz@163.com"
receiver = "vbertcenhz@163.com"
interval = 3
threshold = d(0.97)


def data_core():
    uu898_html = requests.get(url=uu898_url, headers=headers)
    uu898_selector = etree.HTML(uu898_html.content)

    uu898_unit_price_i = uu898_selector.xpath(
        '/html/body/form/div[8]/div[4]/div[14]/div[4]/div[4]/div[5]/ul[1]/li[4]/h6/span[2]')
    uu898_price_i = uu898_selector.xpath(
        '/html/body/form/div[8]/div[4]/div[14]/div[4]/div[4]/div[5]/ul[1]/li[2]/span')
    uu898_1 = uu898_unit_price_i[0].text.replace("元/金", '').strip()
    uu898_2 = uu898_price_i[0].text.strip()

    dd373_html = requests.get(url=dd373_url, headers=headers)
    dd373_selector = etree.HTML(dd373_html.content)

    dd373_unit_price_i = dd373_selector.xpath('//*[@id="biz_content_1"]/div[3]/div[5]/div[1]/p[2]')
    dd373_price_i = dd373_selector.xpath('//*[@id="biz_content_1"]/div[3]/div[2]/div/strong/span')
    dd373_1 = dd373_unit_price_i[0].text.replace("元/金", '').strip()
    dd373_2 = dd373_price_i[0].text.strip()

    return {(uu898_1, uu898_2, 'uu898'), (dd373_1, dd373_2, 'dd373')}


def send_mail(msg, title):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = "cenhz<vbertcenhz@163.com>"
    message['To'] = "cenhz<vbertcenhz@163.com>"
    message['Subject'] = Header("%s ( %s ) " % (now, title), 'utf-8')

    # try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receiver, message.as_string())
    #     print("success!")
    # except smtplib.SMTPException:
    #     print("Error!")


def start():
    conn = pymysql.connect(host='127.0.0.1', user='root', port=3306, password='1a2s3d4f', database='spider_core')
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    result = data_core()
    flag = False
    subject = ''
    cursor = conn.cursor()
    cursor.execute(
        "select avg(unit_price) from gprice_list  where rec_time>=date_sub(rec_time,INTERVAL %d HOUR)" % interval)
    gprice_avg = cursor.fetchall()[0][0]

    for i in result:
        unit_price = i[0]
        sale_price = i[1]
        platform = i[2]
        sql = "insert into gprice_list values(null,'%s',%s,%s,now())" % (platform, unit_price, sale_price)
        cursor.execute(sql)

        if d(unit_price) < d(gprice_avg) * threshold:
            print("%s, 有低价！！！金额=%s元/G" % (now, unit_price))
            if subject == '':
                subject = '平台%s: %s元/G，价格%s元' % (platform, unit_price, sale_price)
            else:
                subject = subject + '; ' + '平台%s: %s元/G，价格%s元' % (platform, unit_price, sale_price)
            flag = True
        else:
            print("%s,金额=%s,平台=%s,近期均价=%s,阈值=%d" % (now, unit_price, platform, gprice_avg, threshold))

    if flag is True:
        send_mail("DD373_Lowest_Realtime_Price", subject)

    cursor.close()
    conn.commit()
    conn.close()


# start()
schedualer = BlockingScheduler()
schedualer.add_job(start, 'cron', hour='8-23', minute='*/3')
schedualer.start()
