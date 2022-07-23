import json
import requests
import math
import numpy

#author: Kasimir
#todo: exceptions, if return from api is 0, setsellprice, profitfunction to price dicts

tax = 0.03
sellorder = 0.015
ressourcereturnrate = 0.58
itemclass = input("itemclass (dagger, naturestaff, helmet, boots)")
discount = 0.05
spec = 0.0625
stationtax = 500
bookbase = 225
focusreduction = 40165

resprice = {}
bookprice = {}
sellprice = {}

itemvalueres = {
    2 : [4],
    3 : [8],
    4 : [16, 32, 64, 128],
    5 : [32, 64, 128, 256],
    6 : [64, 128, 256, 512],
    7 : [128, 256, 512, 1024],
    8 : [256, 512, 1024, 2048]
    }

ressourceid = ["PLANKS", "METALBAR", "LEATHER", "CLOTH"]
bookid = ["WARRIOR_FULL", "WARRIOR_EMPTY", "HUNTER_FULL", "HUNTER_EMPTY", "MAGE_FULL", "MAGE_EMPTY"]

itemiddict = {
    "dagger" : ["MAIN_DAGGER", "2H_DAGGERPAIR", "2H_CLAWPAIR"],
    "naturestaff" : ["MAIN_NATURESTAFF", "2H_NATURESTAFF", "2H_WILDSTAFF"],
    "helmet" : ["HEAD_PLATE_SET1", "HEAD_PLATE_SET2", "HEAD_PLATE_SET3"],
    "boots" : ["SHOES_PLATE_SET1", "SHOES_PLATE_SET2", "SHOES_PLATE_SET3"]
}

itemcraft = {
    "MAIN_DAGGER" : ["METALBAR", 12, "LEATHER", 12],
    "2H_DAGGERPAIR" : ["METALBAR", 16, "LEATHER", 16],
    "2H_CLAWPAIR" : ["METALBAR", 12, "LEATHER", 20],
    "MAIN_NATURESTAFF" : ["PLANKS", 16, "CLOTH", 8],
    "2H_NATURESTAFF" : ["PLANKS", 20, "CLOTH", 12],
    "2H_WILDSTAFF" : ["PLANKS", 20, "CLOTH", 12],
    "HEAD_PLATE_SET1" : ["METALBAR", 8, "", 0],
    "HEAD_PLATE_SET2" : ["METALBAR", 8, "", 0],
    "HEAD_PLATE_SET3" : ["METALBAR", 8, "", 0],
    "SHOES_PLATE_SET1" : ["METALBAR", 8, "", 0],
    "SHOES_PLATE_SET2" : ["METALBAR", 8, "", 0],
    "SHOES_PLATE_SET3" : ["METALBAR", 8, "", 0]
    }

def setressourceprice():
    ressourcejson = []
    for itemid in ressourceid:
        respricestring = "https://www.albion-online-data.com/api/v2/stats/Prices/"
        if itemid == "PLANKS":
            location = "Fort%20Sterling"
        elif itemid == "CLOTH":
            location = "Lymhurst"
        elif itemid == "METALBAR":
            location = "Thetford"
        elif itemid == "LEATHER":
            location = "Martlock"
        else:
            return 0
        for tier in range(4,9):
            for enchant in range(0,4):
                if enchant == 0:
                    enchantstr = ""
                else:
                    enchantstr = "_LEVEL" + str(enchant) + "@" + str(enchant)
                if tier == 4 and enchant == 0:
                    respricestring = respricestring + "T" + str(tier) + "_" + itemid + enchantstr
                else:
                    respricestring = respricestring + "%2CT" + str(tier) + "_" + itemid + enchantstr
        respricestring = respricestring + ".json?locations=" + location +"&qualities=0"
        response = requests.get(respricestring)
        responsejson = response.json()
        ressourcejson.extend(responsejson)
    counter = 0
    for itemid in ressourceid:
        for tier in range(4,9):
            for enchant in range(0,4):
                if enchant == 0:
                    enchantstr = ""
                else:
                    enchantstr = "_LEVEL" + str(enchant) + "@" + str(enchant)
                resstring = "T" + str(tier) + "_" + itemid + enchantstr
                resprice[resstring] = ressourcejson[counter]["sell_price_min"]
                counter = counter + 1

def setsellprice():
    sellpricejson = []
    for itemid in itemiddict[itemclass]:
        sellpricestring = "https://www.albion-online-data.com/api/v2/stats/Prices/"
        for tier in range(4,9):
            for enchant in range(0,4):
                if enchant == 0:
                    enchantstr = ""
                else:
                    enchantstr = "@" + str(enchant)
                if tier == 4 and enchant == 0:
                    sellpricestring = sellpricestring + "T" + str(tier) + "_" + itemid + enchantstr
                else:
                    sellpricestring = sellpricestring + "%2CT" + str(tier) + "_" + itemid + enchantstr
        sellpricestring = sellpricestring + ".json?locations=" + "Blackmarket&qualities=1,2,3,4,5"
        response = requests.get(sellpricestring)
        responsejson = response.json()
        sellpricejson.extend(responsejson)
    counter = 0
    for itemid in itemiddict[itemclass]:
        for tier in range(4,9):
            for enchant in range(0,4):
                if enchant == 0:
                    enchantstr = ""
                else:
                    enchantstr = "@" + str(enchant)
                itemidstring = "T" + str(tier) + "_" + itemid + enchantstr
                qualitylist = []
                for x in range(0,5):
                    qualitylist.append(sellpricejson[counter + x]["sell_price_min"])
                qualitylistnozero = []
                for ele in qualitylist:
                    if ele != 0:
                        qualitylistnozero.append(ele)
                if len(qualitylistnozero) == 0:
                    sellprice[itemidstring] = 0
                elif len(qualitylistnozero) == 1:
                    sellprice[itemidstring] = qualitylistnozero[0]
                else:
                    sellprice[itemidstring] = min(qualitylistnozero)
                print(qualitylist)
                counter = counter + 5
    
def setbookprice():
    #warrior full 4-8, warrior empty 4-8, hunter full 4-8, hutner empty 4-8, mage full 4-8, mage empty 4-8
    bookjson = []
    for itemid in bookid:
        bookpricestring = "https://www.albion-online-data.com/api/v2/stats/Prices/"
        for tier in range(4,9):
            if tier == 4:
                bookpricestring = bookpricestring + "T" + str(tier) + "_JOURNAL_" + itemid 
            else:
                bookpricestring = bookpricestring + "%2CT" + str(tier) + "_JOURNAL_" + itemid
        bookpricestring = bookpricestring + ".json?locations=Lymhurst&qualities=0"
        response = requests.get(bookpricestring)
        responsejson = response.json()
        bookjson.extend(responsejson)
    counter = 0
    for itemid in bookid:
        for tier in range(4,9):
             bookstring = "T" + str(tier) + "_JOURNAL_" + itemid
             bookprice[bookstring] = bookjson[counter]["sell_price_min"]
             counter = counter + 1
    
def amountmaterials(itemid):
    amount = (itemcraft[itemid][1] + itemcraft[itemid][3])
    return amount

def craftingfame(itemid, tier, enchant):
    if tier == 4:
        tierfactor = 22.5
    elif tier == 5:
        tierfactor = 90
    elif tier == 6:
        tierfactor = 270
    elif tier == 7:
        tierfactor = 645
    elif tier == 8:
        tierfactor = 1395
    materials = amountmaterials(itemid)
    base = materials * tierfactor
    fame = 1.5 * (base + enchant*(base - 7.5 * materials))
    return fame

def bookfame(tier):
    fame = bookbase * 2 ** tier
    return fame

def itemvalue(itemid, tier, enchant):
    value = amountmaterials(itemid) * itemvalueres[tier][enchant]
    return value

def blackmarketpricedict(itemid):
    #legacy
    #needs the itemid as a string and pulls minimum sell price on blackmarket for tiers 4-8 with all enchantmentlevels. returns dictionary with tiers as key and prices for all enchantments as a list as value%
    pricedict = {
        4 : [],
        5 : [],
        6 : [],
        7 : [],
        8 : []
        }
    for i in range(4,9):
        for j in range (0,4):
            if j == 0:
                enchant = ""
            else:
                enchant = "@" + str(j)
            response = requests.get("https://www.albion-online-data.com/api/v2/stats/Prices/T" + str(i) + "_" + itemid + enchant + ".json?locations=Blackmarket&qualities=0")
            responsejson = response.json()
            price = responsejson[0]["sell_price_min"]
            pricedict[i].append(price)
    return pricedict

def price(itemid, tier, enchant, location):
    #returns the minimum sell price for an item%
    if enchant == 0:
        enchantstr = ""
    else:
        enchantstr = "@" + str(enchant)
    response = requests.get("https://www.albion-online-data.com/api/v2/stats/Prices/T" + str(tier) + "_" + itemid + enchantstr + ".json?locations=" + location + "&qualities=0")
    responsejson = response.json()
    price = responsejson[0]["sell_price_min"]
    return price

def ressourceprice(itemid, tier, enchant):
    #returns price of material (quantity 1). uses sell price minimum in corresponding royal city%
    #if itemid == "PLANKS":
    #    location = "Fort%20Sterling"
    #elif itemid == "CLOTH":
    #    location = "Lymhurst"
    #elif itemid == "METALBAR":
    #    location = "Thetford"
    #elif itemid == "LEATHER":
    #    location = "Martlock"
    #else:
    #    return 0
    #if enchant == 0:
    #    enchantstr = ""
    #else:
    #    enchantstr = "_LEVEL" + str(enchant) + "@" + str(enchant)
    #response = requests.get("https://www.albion-online-data.com/api/v2/stats/Prices/T" + str(tier) + "_" + itemid + enchantstr + ".json?locations=" + location + "&qualities=0")
    #responsejson = response.json()
    if enchant == 0:
        enchantstr = ""
    else:
        enchantstr = "_LEVEL" + str(enchant) + "@" + str(enchant)
    price = resprice["T" + str(tier) + "_" + itemid + enchantstr]
    return price

def bookprofit(itemid, tier, enchant):
    if itemclass == "dagger" or itemclass == "naturestaff":
        booktype = "HUNTER"
    elif itemclass == "helmet" or itemclass == "boots":
        booktype = "WARRIOR"
    pricefull = bookprice["T" + str(tier) + "_JOURNAL_" + booktype + "_FULL"]
    priceempty = bookprice["T" + str(tier) + "_JOURNAL_" + booktype + "_EMPTY"]
    profit = craftingfame(itemid, tier, enchant) / bookfame(tier) * (pricefull - tax * pricefull - sellorder * pricefull - priceempty)
    return profit
                  
def buyprice(itemid, tier, enchant):
    resprice1 = ressourceprice(itemcraft[itemid][0], tier, enchant)
    if itemcraft[itemid][2] == "":
        resprice2 = 0
    else:
        resprice2 = ressourceprice(itemcraft[itemid][2], tier, enchant)
    price = resprice1 * itemcraft[itemid][1] + resprice2 * itemcraft[itemid][3]
    return price

def focuscost(itemid, tier, enchant):
    #probably inaccurate formula
    focus = 2 * itemvalue(itemid, tier, enchant) / (2 ** (focusreduction/10000))
    return focus
                              
def profit(itemid, tier, enchant):
    #taxes, ressourcereturnrate, books and so on
    #sellprice = price(itemid, tier, enchant, "Blackmarket")
    #craftprice = buyprice(itemid, tier, enchant)*(1-discount)*(1-ressourcereturnrate) + 2 ** (tier + enchant) * 0.1125 * 0.01 * stationtax
    #profit = sellprice - tax * sellprice - sellorder * sellprice - craftprice + bookprofit(itemid, tier, enchant)
    if enchant == 0:
        enchantstr = ""
    else:
        enchantstr = "@" + str(enchant)
    itemidstring = "T" + str(tier) + "_" + itemid + enchantstr
    sellprice2 = sellprice[itemidstring]
    craftprice = buyprice(itemid, tier, enchant)*(1-discount)*(1-ressourcereturnrate) + 2 ** (tier + enchant) * 0.1125 * 0.01 * stationtax
    profit = sellprice2 - tax * sellprice2 - sellorder * sellprice2 - craftprice + bookprofit(itemid, tier, enchant)
    return profit

def profitperfocus(itemid, tier, enchant):
    ppf = profit(itemid, tier, enchant) / focuscost(itemid, tier, enchant)
    return ppf

def profitperfocusdict(itemid):
    ppfdict = {}
    for i in range(4,9):
        for k in range(0,4):
            ppfdict[str(i) + "." + str(k)] = profitperfocus(itemid, i, k)
    return ppfdict

def profitperpremiummonth(itemid, tier, enchant):
    profit = 30 * 10000 * profitperfocus(itemid, tier, enchant)
    return profit

def master():
    setressourceprice()
    setbookprice()
    setsellprice()
    for itemid in itemiddict[itemclass]:
        print(itemid)
        print(profitperfocusdict(itemid))
