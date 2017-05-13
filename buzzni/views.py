# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.contrib.postgres.search import SearchVector
from bs4 import BeautifulSoup
import requests
import urllib

from .models import ImageLink

def gethtml(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    return soup

def index(request):
    context = {
        'text': "text",
    }
    return render(request, 'buzzni/index.html', context)


def search(request):
    searchStr = request.GET['word']
    link = 'http://www.gsshop.com/search/main.gs?tq='+ searchStr +'&lseq=390175&pt=60&cr_yn=Y&pg=90&vt=B&is=N&ab=b#1&so=7&vt=B&pg=30&po=0'
    list = gethtml(link).find('div', attrs={'id': 'searchPrdList'}).find_all_next("li", attrs={'class': "product-item"})

    Imglink = []
    for imglist in list:
        imglist_mod = imglist.find_next("div", attrs={'class': "product-image-search"}).find('img')['src']
        hyperlink_mod = "http://www.gsshop.com"+ imglist.find_next("a")['href'][22:]
        name_mod = imglist.find("dt").contents[2].strip()
        price_mod = imglist.find("dd").find_next("span", attrs={'class': "set-price-search"}).text
        item = [imglist_mod, hyperlink_mod, name_mod, price_mod]
        Imglink.append(item)
    link = 'http://www.hnsmall.com/search/search.do?query_top=' + searchStr
    list = gethtml(link).find('div', attrs={'class': "resultFrameTV"}).find_all_next('ul', class_="goodsList")

    buffer=''
    for imglist in list:
        imglist_modlist = imglist.find_all('li')
        for data in imglist_modlist:
            imglist_buf = data.find_next('div', attrs={'class': "img"})
            if not imglist_buf:
                continue
            imglist_mod = imglist_buf.find_next('img')['src']
            hyperlink_mod = data.find_next('div', attrs={'class': "img"}).find_next('a')['href']
            name_mod = data.find_next('p', attrs={'class': "goodsName"}).find_next('a').text
            price_mod = data.find_next('p', attrs={'class': "sell"}).text.split(' ')[1]
            item = [imglist_mod, hyperlink_mod, name_mod, price_mod]
            Imglink.append(item)

    context = {
        'searchStr': searchStr,
        'link': link,
        'imageLink': Imglink,
        'LIST': buffer,
    }
    return render(request, 'buzzni/search.html', context)
