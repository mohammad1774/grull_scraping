from datetime import datetime
import gspread
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def stock_prices_coinswitch():
    tabular_data = []
    url = 'https://coinswitch.co/coins'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(5)  # Allowing time for the page to load
    present_time = datetime.now().isoformat()
    website = 'Coin Switch'
    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.find('div', class_='cdt-prices-container')
        table_container = table.find('div', class_='small-price-container').find('div', class_='price-chart').find(
            'div', class_='coinlist-container')
        for i in range(20):
            row = table_container.find('div', class_=f'cdt-trends-div-map switch{i}')
            name = row.find('div', class_='cdt-trends-left').find('div', class_='').text
            price = row.find('div', class_='cdt-trends-right').find('div', class_='cdt-trends-top').text
            clean_row = [name, '₹' + price, website, present_time]
            tabular_data.append(clean_row)
        return tabular_data[:20]
    except Exception as e:
        print(f'Error in fetching data from CoinSwitch: {str(e)}')
    finally:
        driver.quit()

def stock_prices_mudrex():
    tabular_data = []
    url = 'https://mudrex.com/all-cryptocurrencies'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(5)  # Allowing time for the page to load
    present_time = datetime.now().isoformat()
    website = 'Mudrex'
    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table1 = soup.find('div', class_='w-full overflow-x-auto').find('table')
        tbody = table1.find('tbody', class_='table-contents')
        for row in tbody.find_all('tr'):
            name = row.find('a').text
            price = row.find('td', class_='p-6 font-medium h-8 text-sm align-middle text-right').text
            row_data = [name, price, website, present_time]
            tabular_data.append(row_data)
        return tabular_data
    except Exception as e:
        print(f'Error in fetching data from Mudrex: {str(e)}')
    finally:
        driver.quit()

def stock_prices_wazirx():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)  # Use chrome_options instead of options
    driver.get('https://wazirx.com/exchange/BTC-INR')
    time.sleep(5)  # Allow time for the page to load

    present_time = datetime.now().isoformat()
    website = 'WazirX'
    tabular_data = []
    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table_anchor = soup.find_all('a', class_='ticker-item')
        for row in table_anchor:
            name_tag = row.find('span', class_='market-name-text').text.lower()
            price = row.find('span', class_='price-text ticker-price').text
            name = name_tag.split('/')[0]
            row_data = [name, price, website, present_time]
            tabular_data.append(row_data)
        return tabular_data[:20]
    except Exception as e:
        print(f'Error in fetching data from WazirX: {str(e)}')
    finally:
        driver.quit()

if __name__ == '__main__':
    sa = gspread.service_account(filename='google_action.json')
    sh = sa.open('crypto_prices')
    wks = sh.worksheet('Sheet1')

    table_wazir = stock_prices_wazirx()
    wks.append_rows(table_wazir)
    print(table_wazir)

    time.sleep(2)
    table_mudrex = stock_prices_mudrex()
    wks.append_rows(table_mudrex[:20])
    print(table_mudrex)

    time.sleep(2)
    table_coinswitch = stock_prices_coinswitch()
    wks.append_rows(table_coinswitch)
    print(table_coinswitch)
