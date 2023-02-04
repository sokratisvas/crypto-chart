import requests
import json
import datetime
import matplotlib.pyplot as plt


def get_all_coins() -> None:
    list_of_coins_url = "https://api.coingecko.com/api/v3/coins/list"
    json_list_of_coins_url = requests.get(list_of_coins_url)
    coins = json.loads(json_list_of_coins_url.text)

    with open("coins.json", "w") as f:
        f.write(json.dumps(coins, indent=4))


def get_coin_data(coin_id) -> None:
    coin_data_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    json_coin_data = requests.get(coin_data_url)
    coin_data = json.loads(json_coin_data.text)

    with open("{coin_id}-data.json", "w") as f:
        f.write(json.dumps(coin_data, indent=4))


def get_coin_data_range(coin_id: str, vs_currency: str, num_of_days: str) -> None:
    coin_data_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/?vs_currency={vs_currency}&days={num_of_days}"
    json_coin_data = requests.get(coin_data_url)
    coin_data = json.loads(json_coin_data.text)

    date_stamps = [
        datetime.datetime.fromtimestamp(stamp[0] / 1000)
        for stamp in coin_data["prices"]
    ]
    coin_value = [stamp[1] for stamp in coin_data["prices"]]
    print(max(coin_value))

    with open(f"{coin_id}-upto-{num_of_days}-days.json", "w") as f:
        f.write(json.dumps(coin_data, indent=4))

    plt.plot(date_stamps, coin_value)
    plt.title(f"{coin_id} vs {vs_currency}")
    plt.xlabel(f"Last {num_of_days} Days")
    plt.ylabel(f"{vs_currency}")
    plt.xlim([min(date_stamps), max(date_stamps)])
    plt.ylim([min(coin_value), max(coin_value)])
    plt.show()


if __name__ == "__main__":
    get_all_coins()
    get_coin_data_range("ethereum", "usd", 10)
