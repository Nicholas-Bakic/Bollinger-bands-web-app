import talib
import ta 
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.pyplot import figure
import base64
from io import BytesIO
from flask import Flask, request, render_template, Response
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    Timeline = request.form['Timeline']
    stock_symbol = text.upper()
    return graph(stock_symbol, Timeline)


def graph(stock_symbol, Timeline):
    # Generate the figure **without using pyplot**.
    msft = yf.Ticker(stock_symbol).history(period=Timeline).reset_index()[["Date", "Close"]]
    bol = ta.volatility.BollingerBands(msft["Close"], window=14)
    msft["lband"] = bol.bollinger_lband() 
    msft["hband"] = bol.bollinger_hband()
    msft["SMA20"] = talib.SMA(msft["Close"], timeperiod = 20)
    fig = Figure(figsize=(18,10))
    ax = fig.subplots()
    ax.plot(msft["Date"], msft["Close"], label="Stock closing price")
    ax.plot(msft["Date"], msft["lband"], label="Lower band")
    ax.plot(msft["Date"], msft["hband"], label="Higher band")
    ax.plot(msft["Date"], msft["SMA20"], label="SMA 20")
    ax.fill_between(msft["Date"], msft["lband"], msft["hband"], alpha = 0.2)
    ax.legend(loc="upper left")
    ax.set(title="Bollinger Bands around stock price", xlabel="Time", ylabel="Price ($)")

    
  

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"



if __name__ == "__main__":
    app.run(debug=True)