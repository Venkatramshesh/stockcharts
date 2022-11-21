#STOCK = "IBM"
#COMPANY_NAME = "TESLA"
import requests
import smtplib
import os
import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from flask import Flask, render_template, request
from form import SubmitForm
from flask_bootstrap import Bootstrap
import time

matplotlib.use('agg')

API_skey= "xxxxx"  #os.environ("API_skey")   #stock market key
STOCK_Endpoint = "https://www.alphavantage.co/query?"

application = Flask(__name__)
Bootstrap(application)
application.config['SECRET_KEY'] = 'jCOo4PAnmU6A0j2lpKeI-A'



@application.route('/',methods=["GET","POST"])
def home():
    form = SubmitForm()

    if form.validate_on_submit():
        STOCK=form.tickersymbol.data

        parameters_stock = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": STOCK,
            "apikey": API_skey,
            "interval": "60min",
            "datatype": "csv"
        }
        path = os.path.join("Stockcharts/", f"{STOCK}")

        stockfile = open(path, mode="a")
        writer = csv.writer(stockfile)

        response = requests.get(STOCK_Endpoint, params=parameters_stock)

        response_content = response.content.decode('utf-8')
        cr = csv.reader(response_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            writer.writerow(row)
        stockfile.close()

        df_stock = pd.read_csv(path, nrows=7)
        df_stock = df_stock[::-1]

        plt.plot(df_stock.timestamp, df_stock.open, '#FFA500', lw=1.5, linestyle='-')
        plt.title(f"{STOCK} Opening Price Vs Day", fontsize=14)
        plt.xticks(rotation=45)

        # plt.xticks(fontsize=14)
        # plt.yticks(fontsize=14)
        #plt.xlabel('Date')
        plt.ylabel(f'{STOCK} Open Price($)')

        newpath = os.path.join("static/img/", f"{STOCK}.jpeg")
        plt.savefig(newpath,bbox_inches='tight')
        time.sleep(1)
        plt.clf()
        # plt.show()

        return render_template('stock.html',stock=STOCK, url=newpath)

    return render_template('index.html',form=form)

if __name__=="__main__":
     application.run(debug=True)
