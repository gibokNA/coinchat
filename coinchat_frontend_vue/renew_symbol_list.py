import json, ccxt

binance = ccxt.binance(config={
    'apiKey': "",
    'secret': "",
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

markets = binance.load_markets()
symbol_list = []

for i in markets:
    if "/USDT" in i:
        symbol_list.append(i.replace('/', ''))

symbol_list.sort()

with open('symbol_list.json', 'w', encoding="utf-8") as f:
    json.dump(symbol_list, f, ensure_ascii=False, indent="\t")