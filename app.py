import json;
import requests as r;
from lxml import etree;
from flask import Flask;

# @helpers: global
html = r.get('https://www.cobie.de/speisekarte');
today = '(//h3[@class="dayheadline"]/parent::div)[1]';

# @helpers: parse
def parse(path):
    return etree.HTML(html.text).xpath(today + path)

# @menu_helpers: menu_net
def menu_net():
    #name
    names = parse('//div[@class="cobie-product-name"]//text()');

    # sups
    sups = parse('//sup//text()');    
    
    # price
    price = parse('//span[@class="woocommerce-Price-amount amount"]//text()')
    amounts = []
    for idx, i in enumerate(price):
        (idx % 2 != 0) and amounts.append('€' + i);

    # desc
    descs = parse('//div[@class="cobie-product-description"]//text()');

    return names, sups, amounts, descs;

# @main: menu_list
def menu_list():
    net = menu_net();
    products = []
    for idx, i in enumerate(net[0]):
        products.append(dict(
            name = i,
            sup = net[1][idx],          
            price = net[2][idx],
            desc = net[3][idx]
        ));

    return products;

# @main: app
app = Flask(__name__);

@app.route("/menu/today")
def hello():
    res = dict();
    try:
        res['menu'] = menu_list();
        res['err_msg'] = None;

        return json.dumps(res), 200;
    
    except err:
        res['err_msg'] = 'oops, ERROR!';

        return json.dumps(res), 404;
