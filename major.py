# -*- coding: utf-8 -*-
import pygal
from pygal.style import NeonStyle,DarkGreenBlueStyle
from flask import Flask, Response , render_template
import urllib2,json

#Function returns celsius from Farenheit
def f_to_c(n):
    Celsius = (int(n) - 32) * 5.0/9.0
    return Celsius
 
 
app = Flask(__name__)

url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22Hyderabad%2CIndia%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
ans = json.load(urllib2.urlopen(url))
 
def get_forecast():
    global ans
    higher,lower,days=[],[],[]
    for i in ans['query']['results']['channel']['item']['forecast']:
        higher.append(f_to_c(i['high']))
        lower.append(f_to_c(i['low']))
        days.append(i['date'])
    return lower,higher,days



def get_details():
    global ans
    return ans['query']['results']['channel']['item']['condition']

def get_humidity():
    global ans
    return float(ans['query']['results']['channel']['atmosphere']['humidity'])

def get_pressure():
    global ans
    return float(ans['query']['results']['channel']['atmosphere']['pressure'])


@app.route('/')
def index():
    """ render svg on html """
    return render_template('index.html')
 
 
#To display forecast frame
@app.route('/forecast/')
def forecast():
    """ render svg graph """
    bar_chart = pygal.StackedBar(style=NeonStyle)
    bar_chart.title = "Hyderabad Forecast"
    lower,higher,days = get_forecast()
    bar_chart.add('Kanishtam', lower)
    bar_chart.add('Garishtam', higher)
    bar_chart.x_labels = days
    return Response(response=bar_chart.render(), content_type='image/svg+xml')

#To display Humidity frame
@app.route('/humidity/')
def humidity():
    """ render svg graph """
    pie_chart = pygal.Pie(style=DarkGreenBlueStyle)
    pie_chart.title = 'Humidity'
    humidity = get_humidity()
    pie_chart.add('Filled', humidity)
    pie_chart.add('Unfilled', 100 - humidity)
    pie_chart.render()
    return Response(response=pie_chart.render(), content_type='image/svg+xml')

#To display Pressure frame
@app.route('/pressure/')
def pressure():
    """ render svg graph """
    pie_chart = pygal.Pie(style=DarkGreenBlueStyle)
    pie_chart.title = 'Pressure'
    pressure = get_pressure()
    pie_chart.add('Filled', pressure)
    pie_chart.add('Unfilled', 100 - pressure)
    pie_chart.render()
    return Response(response=pie_chart.render(), content_type='image/svg+xml')
 
if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
