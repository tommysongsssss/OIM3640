from flask import Flask, request, render_template_string
import os, json, urllib.parse, urllib.request
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

def find_temp(city: str):
    if not API:
        raise RuntimeError("Missing OPENWEATHER_API_KEY in .env")
    params = {
        "q": f"{city},us",   # change country if needed
        "appid": API,
        "units": "imperial"
    }
    url = "https://api.openweathermap.org/data/2.5/weather?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["main"]["temp"]

@app.route("/", methods=["GET","POST"])
def home():
    msg = ""
    city = ""
    if request.method == "POST":
        city = request.form.get("city","").strip()
        try:
            temp = find_temp(city)
            msg = f"Current temperature in {city}: {temp} °F"
        except Exception as e:
            msg = f"Error: {e}"
    return render_template_string("""
        <html>
        <body style="font-family: system-ui; max-width: 560px; margin: 2rem auto;">
          <h2>Check Temperature</h2>
          <form method="post">
            <input name="city" placeholder="City" value="{{city}}" />
            <button type="submit">Get temp</button>
          </form>
          <p>{{msg}}</p>
        </body>
        </html>
    """, msg=msg, city=city)

if __name__ == "__main__":
    app.run(debug=True)
