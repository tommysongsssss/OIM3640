from flask import Flask, render_template, request
from weather import find_temp
import requests

app = Flask(__name__)

# ---------------- existing routes ----------------
# (your homepage, hello, square, weather, etc.)
# -------------------------------------------------

@app.route("/bitcoin")
def bitcoin_price():
    """
    Calls the CoinDesk API and returns the current BTC price in USD.
    """
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"

    try:
        response = requests.get(url)
        data = response.json()

        price_usd = data["bpi"]["USD"]["rate"]
        updated_time = data["time"]["updated"]

        return render_template("bitcoin.html", price=price_usd, updated=updated_time)

    except Exception:
        return render_template("bitcoin.html", price="Error", updated="Unavailable")


if __name__ == "__main__":
    app.run(debug=True)
