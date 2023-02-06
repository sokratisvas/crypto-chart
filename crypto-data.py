import requests
import json
import datetime
import matplotlib.pyplot as plt
from typing import List, Dict


def pprint(data_struct) -> None:
    print(json.dumps(data_struct, indent=4))


def get_all_coins() -> List[Dict[str, str]]:
    return json.loads(requests.get("https://api.coingecko.com/api/v3/coins/list").text)


def get_all_coin_ids() -> List[str]:
    coins = get_all_coins()
    return [coin["id"] for coin in coins]


def get_supported_vs_currencies():
    return json.loads(requests.get("https://api.coingecko.com/api/v3/simple/supported_vs_currencies").text)


def get_coin_id(coin_name: str, available_coins: List[Dict[str, str]]) -> str:
    return next(coin for coin in available_coins if coin["name"] == coin_name)["id"]


def get_coin_symbol(coin_name: str, available_coins: List[Dict[str, str]]) -> str:
    return next(coin for coin in available_coins if coin["name"] == coin_name)["symbol"]


def plot_coin_chart(coin_id: str, vs_currency: str, num_of_days: str) -> None:
    if vs_currency not in get_supported_vs_currencies():
        raise ValueError(f"error: {vs_currency} is not a supported vs currency.")

    if coin_id not in get_all_coin_ids():
        raise ValueError(f"error: {coin_id} is not a supported coin id.")

    coin_data_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/?vs_currency={vs_currency}&days={num_of_days}"
    json_coin_data = requests.get(coin_data_url)
    coin_data = json.loads(json_coin_data.text)

    date_stamps = [
        datetime.datetime.fromtimestamp(stamp[0] / 1000)
        for stamp in coin_data["prices"]
    ]
    coin_value = [stamp[1] for stamp in coin_data["prices"]]

    plt.plot(date_stamps, coin_value)
    plt.title(f"{coin_id} vs {vs_currency}")
    plt.xlabel(f"Last {num_of_days} Days")
    plt.ylabel(f"{vs_currency}")
    plt.xlim([min(date_stamps), max(date_stamps)])
    plt.ylim([min(coin_value), max(coin_value)])
    plt.show()


def main() -> None:
    coins = get_all_coins()
    coin_name = "Bitcoin"
    vs_currency_id = "usd"
    num_of_days = 10
    plot_coin_chart(get_coin_id(coin_name, coins), vs_currency_id, num_of_days)
    

if __name__ == "__main__":
    main()
