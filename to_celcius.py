#!/usr/bin/env python
import urllib2,json


def f_to_c(n):
	Celsius = (n - 32) * 5.0/9.0
	return Celsius

url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22Hyderabad%2CIndia%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"


ans = json.load(urllib2.urlopen(url))

print ans['query']['results']['channel']['item']['condition']

print  ans['query']['results']['channel']['atmosphere']

print f_to_c(int(ans['query']['results']['channel']['item']['condition']['temp']))




