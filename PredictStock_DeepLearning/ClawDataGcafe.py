import requests
import sys

# claw data
def claw_DataStock_Gcafe(Name, Page):
    header= {
            'Cookie': 'favorite_stocks_state=1; __UF=-1; _uidcms=1658202174129752373; __R=2; __tb=0; _gid=GA1.2.1136744825.1661092261; __RC=31; cafef.IsMobile=IsMobile=NO; _ga_D40MBMET7Z=GS1.1.1661141800.2.1.1661141969.0.0.0; _ga_860L8F5EZP=GS1.1.1661141792.3.1.1661141970.0.0.0; _ga=GA1.2.480233724.1658202174; _gat_gtag_UA_34575478_17=1; __uif=__uid%3A1375247731963110594%7C__create%3A1657524773',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            }

    playload = {
            'ctl00$ContentPlaceHolder1$ctl03$txtKeyword': Name,
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ctl03$pager2',
            '__EVENTARGUMENT': Page,
            }

    url = 'https://s.cafef.vn/Lich-su-giao-dich-'+Name+'-1.chn'
    crawl = requests.post(url, headers = header, data = playload)
    return crawl.text

def get_data(name):
    data = []
    page = 1
    print('\nĐang Chuẩn Bị Dữ Liệu...\n')
    while True:
        Is_lastPage = claw_DataStock_Gcafe(name, page)
        if Is_lastPage.find('style="font-family: Arial; font-size: 10px; font-weight: normal; background-color: #FFF;height:30px;padding-right:5px">') == -1:
            break

        fill_data = claw_DataStock_Gcafe(name, page)
        fill_data = fill_data.split('<tr')
        for data_index in range(len(fill_data)):
            if fill_data[data_index].find('<td class="Item_DateItem">') != -1:
                date  = fill_data[data_index].split('<td')[1][fill_data[data_index].split('<td')[1].find('>')+1:fill_data[data_index].split('<td')[1].find('<')].replace(',','')
                price = fill_data[data_index].split('<td')[2][fill_data[data_index].split('<td')[2].find('>')+1:fill_data[data_index].split('<td')[2].find('&')].replace(',','')
                vol   = fill_data[data_index].split('<td')[6][fill_data[data_index].split('<td')[6].find('>')+1:fill_data[data_index].split('<td')[6].find('&')].replace(',','')
                if float(price) != 0 and int(vol) != 0:
                    data.append((date, float(price), int(vol)))
                    
        page += 1

    return data