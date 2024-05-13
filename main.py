from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime
import gspread
import pickle
import requests
import time
from scrapfly import ScrapflyClient, ScrapeConfig, ScrapeApiResponse

# 
def stock_prices_mudrex():
    url = 'https://mudrex.com/all-cryptocurrencies'
    tabular_data = []


    #session = HTMLSession()
    response = requests.get(url)


    try:
        if response.status_code == 200:
            #response.html.render()
            present_time = datetime.now()
            present_time = present_time.isoformat()
            soup = BeautifulSoup(response.text, 'lxml')
            table1 = soup.find('div',class_='w-full overflow-x-auto').find('table')
            tbody = table1.find('tbody',class_='table-contents')
            for row in tbody.find_all('tr'):
                #print(row,'\n',row.text,'\n\n\n')
                name = row.find('a').text
                price = row.find('td',class_ = 'p-6 font-medium h-8 text-sm align-middle text-right').text
                row_data = [name,price,'Mudrex',present_time]
                #print(row_data)
                tabular_data.append(row_data)
            return tabular_data
        else:
            print('connection not successful.')
            t_data = stock_prices_mudrex()
            return t_data
           # print(tbody.text)
    except:
        time.sleep(2)
        print('connection error mudrex')
        t_data = stock_prices_mudrex()
        return t_data
    

def stock_prices_wazirx():
    url = 'https://wazirx.com/exchange/BTC-INR'

    # session = HTMLSession()
    with HTMLSession() as session:
        response = session.get(url)
        tabular_data = []
        try:
            if response.status_code == 200:
                response.html.render()
                present_time = datetime.now()
                present_time = present_time.isoformat()
                soup = BeautifulSoup(response.html.html,'lxml')
                table_anchor = soup.find_all('a',class_='ticker-item')
                for row in table_anchor:
                    #print(row, '\n\n',row.text,'\n\n\n')
                    name_tag = row.find('span',class_='market-name-text').text.lower()
                    price = row.find('span',class_ = 'price-text ticker-price').text
                    #print(name)
                    name = name_tag.split('/')[0]
                    #print(name)
                    #print(price)
                    row_data = [name,price,'WazirX',present_time]
                    tabular_data.append(row_data)
                print('\n\n\n',tabular_data,'\n\n\n')
                return tabular_data[:20]
            else:
                print('connection not successful.')
                t_data = stock_prices_wazirx()
                return t_data
        except Exception as e:
            time.sleep(2)
            print('connection error wazir',e)
            t_data = stock_prices_wazirx()
            return t_data
        

def stock_wazirx():
    api = 'scp-live-b27b2bd698bb49b0a43b9b6291f0acda'
    scrapfly = ScrapflyClient(key=api)

    result = scrapfly.scrape(
    ScrapeConfig(
        url = 'https://wazirx.com/exchange/BTC-INR',
        country = 'in',
        proxy_pool = 'public_residential_pool',
        render_js=True,
        asp = True,
    
    )
)

    try:
        present_time = datetime.now()
        present_time  = present_time.isoformat()
        tabular_data = []
        table_anchor = result.soup.find_all('a',class_='ticker-item')
        for row in table_anchor:
            #print(row, '\n\n',row.text,'\n\n\n')
            name_tag = row.find('span',class_='market-name-text').text.lower()
            price = row.find('span',class_ = 'price-text ticker-price').text
            #print(name)
            name = name_tag.split('/')[0]
            #print(name)
            #print(price)
            row_data = [name,price,'WazirX',present_time]
            tabular_data.append(row_data)
        print('\n\n\n',tabular_data,'\n\n\n')
        return tabular_data[:20]
    except Exception as e:
        time.sleep(2)
        print('connection error wazir',e)
  


def stock_prices_coindcx():
    api = 'scp-live-b27b2bd698bb49b0a43b9b6291f0acda'
    scrapfly = ScrapflyClient(key=api)

    result = scrapfly.scrape(
    ScrapeConfig(
        url = 'https://coindcx.com/trade/BTCINR',
        country = 'in',
        proxy_pool = 'public_residential_pool',
        render_js=True,
        asp = True,
         js_scenario=[
        {"click": {"selector": "button.-c-tab--strong.white--text","ignore_if_not_visible": False}}]
    )
)

    try:
        tabular_data = []
        table = result.soup.find('div',class_ = 'currency-list__container').find_all('a')
        #print(table)

        present_time = datetime.now()
        present_time  = present_time.isoformat()
        for row in table:
            name = row.find('div',class_='info').find('div',class_= 'name__container stat--strong').find('span').get_text()
        #    print(name)
            price = row.find('div',class_="price -c-show-on-portrait").find('p',class_= 'converted-price stat').get_text()
        #    print(price,'\n\n')
            row_data = [name,price,'CoinDCX',present_time]
            tabular_data.append(row_data)
        return tabular_data[:20]
    except Exception as e:
        print('There is an error: ',e)
    
   


def stock_prices_coinswitch():
    api = 'scp-live-b27b2bd698bb49b0a43b9b6291f0acda'
    scrapfly = ScrapflyClient(key=api)

    result = scrapfly.scrape(
    ScrapeConfig(
        url = 'https://coinswitch.co/coins',
        country = 'in',
        proxy_pool = 'public_residential_pool',
        render_js=True,
        asp = True
    )
)
    
    present_time = datetime.now()
    present_time = present_time.isoformat()
    website = 'Coin Switch'
    try:
        tabular_data = []

        table = result.soup.find('div',class_='cdt-prices-container')
#        table = soup.find('div',class_='cdt-prices-container')
        table_container = table.find('div',class_='small-price-container').find('div',class_='price-chart').find('div',class_='coinlist-container')
        rows = []
        for i in range(20):
            row = table_container.find('div',class_=f'cdt-trends-div-map switch{i}')
            rows.append(row)
            #print('\n\n\n',row.text)
            name = row.find('div',class_='cdt-trends-left').find('div',class_ = '').text
            price = row.find('div',class_ = 'cdt-trends-right').find('div',class_='cdt-trends-top').text
            clean_row = [name,'₹'+price,website,present_time]
            tabular_data.append(clean_row)
        return tabular_data
    except Exception as e:
        time.sleep(2)
        print('connection error coinswitch',e)
   
      


if __name__ == '__main__':
    

    sa = gspread.service_account(filename='google_action.json')
    sh = sa.open('crypto_prices')
    wks = sh.worksheet('Sheet1')
    
    table_wazir = stock_wazirx()
    wks.append_rows(table_wazir)
    
    #print(table_wazir)


    time.sleep(2)
    table_mudrex = stock_prices_mudrex()
    wks.append_rows(table_mudrex[:20])
    #print(table_mudrex)

    time.sleep(2)
    table_coinswitch = stock_prices_coinswitch()
    wks.append_rows(table_coinswitch)
    #print(table_coinswitch[:20])


    time.sleep(2)
    table_coindcx = stock_prices_coindcx()
    wks.append_rows(table_coindcx)

    #wks.append_rows(table_wazir)

 
