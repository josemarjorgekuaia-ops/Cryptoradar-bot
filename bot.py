def get_price(coin):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin, "vs_currencies": "usd"}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    return data.get(coin, {}).get("usd", None)

def get_rsi(coin):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
        params = {"vs_currency": "usd", "days": "14"}
        r = requests.get(url, params=params, timeout=10)
        prices = [p[1] for p in r.json().get("prices", [])]

        if len(prices) < 2:
            return None

        gains, losses = [], []

        for i in range(1, len(prices)):
            diff = prices[i] - prices[i-1]
            if diff > 0:
                gains.append(diff)
            else:
                losses.append(abs(diff))

        if not gains and not losses:
            return None

        avg_gain = sum(gains)/len(gains) if gains else 0
        avg_loss = sum(losses)/len(losses) if losses else 0

        if avg_loss == 0:
            return 100

        rs = avg_gain/avg_loss
        return 100 - (100/(1+rs))

    except:
        return None
