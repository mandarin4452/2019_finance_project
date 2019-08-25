from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests as req
import pandas as pd
import datetime
import sys
import traceback
from statsmodels.tsa.arima_model import ARIMA
from PIL import Image



def stock_page(code, page):
    try:
        print("Crawling processing")
        url = "http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}".format(code = code, page = page)
        res = req.get(url)
        res.encoding = 'euc-kr'
        soap = BeautifulSoup(res.text, 'lxml')
        df = pd.read_html(str(soap.find("table")), header = 0, encoding = 'euc-kr')[0]
        df = df.dropna()
        df = df[['날짜','종가']]
        return df
    except Exception as e:
        traceback.print_exc()
    return None


def analysis(code):
    code = str(code)
    print("Processing analysis")

    # 해당 코드의 주가 테이블
    chart_url = "http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}".format(code = code, page = 2)
    res = req.get(chart_url)
    res.encoding = 'euc-kr'


    # 주가 테이블 마지막 페이지 추출

    soap = BeautifulSoup(res.text, 'lxml')
    element_table_nav = soap.find("table", class_ = "Nnavi")
    element_td_last = element_table_nav.find("td", class_ = "pgRR")
    last_pg = element_td_last.a.get('href').rsplit('&')[1]
    last_pg = last_pg.split('=')[1]
    last_pg = int(last_pg)

    df_all = None
    for page in range(1,last_pg):
        df = stock_page(code,page)
        df_all = pd.concat([df_all,df])

    df_all = df_all.sort_values(by='날짜', ascending = True)
    df_all = df_all.rename(columns={"날짜" : "Date", "종가" : "Values"})
    # File store as (code).csv , and datetime as ascending
    file_name = str(code) + ".csv"
    df_all.to_csv(file_name,mode = 'w', index = False, encoding = 'euc-kr')

    
    series = pd.read_csv(file_name,header = 0, index_col = 0, squeeze = True, encoding = 'euc-kr')


    model = ARIMA(series, order = (0,1,1))
    model_fit = model.fit(trend='nc',full_output=True,disp = 1)
    model_fit.plot_predict()
    plt.title("Fitted model")
    fitted_img = code + '_fit.png'
    plt.savefig(fitted_img)
    fit_img = Image.open(fitted_img)
    fit_img = fit_img.resize((500,400))
    fit_img.save(fitted_img)

    print("Forecast processing")
    fore = model_fit.forecast(steps=7)
    today = datetime.datetime.today()
    days = []
    value = []

    for i in range(1,8):
        day = (today + datetime.timedelta(days = i)).strftime("%m %d")
        days.append(day)
        value.append(fore[2][i-1][1])

    plt.clf()
    plt.plot(days,value)
    plt.xlabel('Date (Month, Day)')
    plt.ylabel('Value')
    plt.title('Forecast')
    fore_name = code + '_forecast.png'
    plt.savefig(fore_name)
    fore_img = Image.open(fore_name)
    fore_img = fore_img.resize((500,400))
    fore_img.save(fore_name)
    #plt.show()

