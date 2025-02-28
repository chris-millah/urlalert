import requests
import time
import threading
from flask import Flask, render_template_string
from concurrent.futures import ThreadPoolExecutor

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
    # COMMENT BACK IN IF YOU WANNA TEST FAILURE {"name": "Game of War (Invalid)", "url": "https://play.google.com/store/apps/details?id=com.machinezoneASDASD.gow"},
]

status_data = []

def check_url(item):
    try:
        response = requests.get(item["url"], timeout=5)
        status = response.status_code
    except requests.RequestException:
        status = 404
    return {"name": item["name"], "url": item["url"], "status": status}

def check_urls():
    global status_data
    while True:
        with ThreadPoolExecutor(max_workers=10) as executor:
            status_data = list(executor.map(check_url, URLS))
        time.sleep(5)  # Check every 5 seconds

@app.route('/')
def index():
    table_rows = "".join(
        f'<tr style="background-color: {"#ffcccc" if item["status"] == 404 else "#ccffcc"};">'
        f'<td>{item["name"]}</td>'
        f'<td><a href="{item["url"]}" target="_blank">{item["url"]}</a></td>'
        f'<td style="font-weight: bold; color: {"red" if item["status"] == 404 else "green"};">{item["status"]}</td>'
        f'</tr>'
        for item in status_data
    )
    
    alert_message = "".join(
        f'<p style="color:red; font-size:20px; font-weight:bold;">ALERT: {item["name"]} (404) - '
        f'<a href="{item["url"]}" target="_blank">{item["url"]}</a></p>'
        for item in status_data if item["status"] == 404
    )
    
    return render_template_string(f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="10">
            <title>URL Monitor</title>
            <style>
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body style="background-color:{'red' if any(item['status'] == 404 for item in status_data) else 'white'};">
            <h1>URL Monitor</h1>
            {alert_message if any(item['status'] == 404 for item in status_data) else '<p>All URLs are OK.</p>'}
            <table>
                <tr>
                    <th>Name</th>
                    <th>URL</th>
                    <th>Status</th>
                </tr>
                {table_rows}
            </table>
        </body>
        </html>
    """)

if __name__ == '__main__':
    threading.Thread(target=check_urls, daemon=True).start()
    app.run(host='0.0.0.0', port=3000, debug=False)
