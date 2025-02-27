import requests
import time
from flask import Flask, render_template_string

app = Flask(__name__)

URLS = [
    {"name": "Clue Master – Logic Puzzle", "url": "https://play.google.com/store/apps/details?id=com.luwukmeliana.lexicard"},
    {"name": "The Superhero League 2", "url": "https://play.google.com/store/apps/details?id=com.onebutton.mrsuper2"},
    {"name": "Serenity's Spa: Beauty Salon", "url": "https://play.google.com/store/apps/details?id=co.gxgames.spa"},
    {"name": "Hexa Sort", "url": "https://play.google.com/store/apps/details?id=com.gamebrain.hexasort"},
    {"name": "Bloom Sort", "url": "https://play.google.com/store/apps/details?id=com.bloom.sort"},
    {"name": "Family Tree! – Logic Puzzles", "url": "https://play.google.com/store/apps/details?id=com.luwukmeliana.familytree"},
    {"name": "Sticker Book Puzzle", "url": "https://play.google.com/store/apps/details?id=com.game5mobile.sticker"},
    {"name": "Cake Sort Puzzle 3D", "url": "https://play.google.com/store/apps/details?id=com.gamebrain.piesort"},
    {"name": "Coin Sort", "url": "https://play.google.com/store/apps/details?id=com.MoodGames.CoinSort"},
    {"name": "Wordscapes", "url": "https://play.google.com/store/apps/details?id=com.peoplefun.wordcross"},
    {"name": "Ink Inc.", "url": "https://play.google.com/store/apps/details?id=com.srgstudios.inkinc"},
    {"name": "Matchington Mansion", "url": "https://play.google.com/store/apps/details?id=com.matchington.mansion"},
    {"name": "Game of War", "url": "https://play.google.com/store/apps/details?id=com.machinezone.gow"},
]

alerts = []

def check_urls():
    global alerts
    while True:
        alerts.clear()
        for item in URLS:
            try:
                response = requests.get(item["url"], timeout=5)
                if response.status_code == 404:
                    alerts.append({"name": item["name"], "url": item["url"]})
            except requests.RequestException:
                alerts.append({"name": item["name"], "url": item["url"]})
        time.sleep(3)  # Check every 60 seconds

@app.route('/')
def index():
    alert_html = "".join(
        f'<p style="color:red; font-size:20px;">ALERT: {a["name"]} (404) - <a href="{a["url"]}" target="_blank">{a["url"]}</a></p>'
        for a in alerts
    )
    return render_template_string(f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="10">
            <title>URL Monitor</title>
        </head>
        <body style="background-color:{'red' if alerts else 'white'};">
            <h1>URL Monitor</h1>
            {alert_html if alerts else '<p>All URLs are OK.</p>'}
        </body>
        </html>
    """)

if __name__ == '__main__':
    import threading
    threading.Thread(target=check_urls, daemon=True).start()
    app.run(host='0.0.0.0', port=3000, debug=False)
