import requests
from flask import Flask, request, render_template_string
import re
import json

app = Flask(__name__)

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <title>Legends Token & Cookie Checker</title>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: monospace;
            margin: 0;
            padding: 0;
        }
        header img {
            width: 100%;
            max-height: 250px;
            object-fit: cover;
        }
        h1 {
            text-align: center;
            color: red;
            margin: 20px 0;
        }
        form {
            text-align: center;
            margin: 20px;
        }
        input, textarea {
            padding: 10px;
            margin: 5px;
            width: 300px;
            background: #111;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 5px;
        }
        input[type=submit] {
            background: red;
            color: white;
            cursor: pointer;
        }
        table {
            width: 95%;
            margin: 20px auto;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #00ff00;
            padding: 8px;
            text-align: center;
        }
        .copy-btn {
            padding: 5px 10px;
            background: lime;
            color: black;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
    <script>
        function copyToClipboard(id) {
            const el = document.getElementById(id);
            el.select();
            document.execCommand("copy");
            alert("Copied!");
        }
    </script>
</head>
<body>
    <header>
        <img src="https://wallpapercave.com/wp/wp9461089.jpg" alt="Banner">
    </header>
    <h1>LEGENDS FACEBOOK TOKEN/COOKIE CHECKER</h1>
    <form method="post" enctype="multipart/form-data" action="/check">
        <input type="text" name="input" placeholder="Enter Token or Cookie"><br>
        OR Upload File (.txt)<br>
        <input type="file" name="file"><br>
        <input type="submit" value="Check">
    </form>
    {% if results %}
    <table>
        <tr>
            <th>Token</th>
            <th>UID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Created At</th>
            <th>Cookie</th>
            <th>Status</th>
        </tr>
        {% for res in results %}
        <tr>
            <td>
                <textarea id="token{{ loop.index }}" rows="2" readonly>{{ res.token }}</textarea>
                <button class="copy-btn" onclick="copyToClipboard('token{{ loop.index }}')">Copy</button>
            </td>
            <td>{{ res.uid }}</td>
            <td>{{ res.name }}</td>
            <td>{{ res.email }}</td>
            <td>{{ res.created_at }}</td>
            <td>
                <textarea id="cookie{{ loop.index }}" rows="2" readonly>{{ res.cookie }}</textarea>
                <button class="copy-btn" onclick="copyToClipboard('cookie{{ loop.index }}')">Copy</button>
            </td>
            <td>{{ res.status }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>'''

def extract_token_from_cookie(cookie):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": cookie
        }
        response = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token = re.search(r'"EAAG\w+?"', response.text)
        return token.group(0).replace('"', '') if token else None
    except:
        return None

def get_info(token):
    try:
        info = requests.get(f"https://graph.facebook.com/me?fields=id,name,email&access_token={token}").json()
        if 'error' in info:
            return None
        created = requests.get(f"https://graph.facebook.com/{info['id']}?fields=created_time&access_token={token}").json()
        return {
            "uid": info.get("id", "N/A"),
            "name": info.get("name", "N/A"),
            "email": info.get("email", "N/A"),
            "created_at": created.get("created_time", "N/A"),
            "token": token,
            "status": "Valid"
        }
    except:
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check():
    inputs = []

    if 'input' in request.form and request.form['input'].strip():
        inputs.append(request.form['input'].strip())

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            lines = file.read().decode().splitlines()
            inputs.extend([line.strip() for line in lines if line.strip()])

    results = []

    for inp in inputs:
        token = inp
        cookie = ""
        is_cookie = 'c_user=' in inp and 'xs=' in inp
        if is_cookie:
            cookie = inp
            token = extract_token_from_cookie(cookie)

        if token:
            info = get_info(token)
            if info:
                info["cookie"] = cookie if cookie else "N/A"
                info["token"] = token
                results.append(info)
            else:
                results.append({
                    "uid": "N/A", "name": "N/A", "email": "N/A",
                    "created_at": "N/A", "token": token,
                    "cookie": cookie, "status": "Invalid"
                })
        else:
            results.append({
                "uid": "N/A", "name": "N/A", "email": "N/A",
                "created_at": "N/A", "token": "N/A",
                "cookie": cookie, "status": "Token Not Found"
            })

    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

import re

app = Flask(__name__)

# Stylish HTML in Legends style
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FB Token/Cookie Checker | Legends UI</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
  <style>
    body {
      background-color: #0f0f0f;
      color: #00ff88;
      font-family: 'Orbitron', sans-serif;
      text-align: center;
      padding: 40px;
      animation: fadeIn 1s ease-in-out;
    }

    h1, h2 {
      text-shadow: 0 0 10px #00ff88;
    }

    textarea, button {
      width: 80%;
      max-width: 600px;
      padding: 15px;
      margin: 15px 0;
      background: #1c1c1c;
      border: 1px solid #00ff88;
      color: #00ff88;
      font-size: 16px;
      border-radius: 8px;
      outline: none;
      transition: 0.3s;
    }

    textarea:focus, button:hover {
      border-color: #ffffff;
      background-color: #121212;
    }

    button {
      cursor: pointer;
      font-weight: bold;
    }

    .result {
      background: #111;
      border: 1px solid #00ff88;
      box-shadow: 0 0 15px #00ff88;
      padding: 20px;
      margin-top: 30px;
      border-radius: 12px;
      max-width: 700px;
      margin-left: auto;
      margin-right: auto;
      text-align: left;
      animation: glowIn 1s ease-in-out;
    }

    a {
      color: #00ff88;
      text-decoration: none;
    }

    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    @keyframes glowIn {
      from {
        box-shadow: 0 0 0px #00ff88;
      }
      to {
        box-shadow: 0 0 15px #00ff88;
      }
    }
  </style>
</head>
<body>
  <h1>💀 Legends FB Tool 💀</h1>
  <h2>Token / Cookie Info Extractor</h2>

  <form method="POST" action="/check">
    <textarea name="input_data" rows="6" placeholder="Paste Facebook Token or Cookie here..." required></textarea><br>
    <button type="submit">🚀 Start Check</button>
  </form>

  {% if result %}
  <div class="result">
    {{ result|safe }}
  </div>
  {% endif %}

  <p style="margin-top: 40px; color: #666;">
    &copy; 2025 SarFu Rullex | For Educational Use Only
  </p>
</body>
</html>
'''

# Function to extract token from Facebook cookie
def get_token_from_cookie(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie
    }
    try:
        res = requests.get("https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed", headers=headers)
        token = re.search(r'EAAA\w+', res.text)
        return token.group(0) if token else None
    except:
        return None

# Estimate account creation year from UID
def estimate_creation(uid):
    try:
        uid = int(uid)
        if uid < 1000000000: return "Before 2012"
        if uid < 2000000000: return "2012 - 2015"
        if uid < 3000000000: return "2015 - 2018"
        if uid < 4000000000: return "2018 - 2021"
        return "After 2021"
    except:
        return "Unknown"

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/check", methods=["POST"])
def check():
    input_data = request.form["input_data"].strip()
    token = input_data

    if "c_user=" in input_data:
        token = get_token_from_cookie(input_data)
        if not token:
            return render_template_string(HTML_TEMPLATE, result="<p style='color:red;'>❌ Invalid or expired Cookie</p>")

    url = f"https://graph.facebook.com/me?fields=id,name,email,birthday&access_token={token}"
    try:
        res = requests.get(url)
        data = res.json()
        if 'error' in data:
            return render_template_string(HTML_TEMPLATE, result="<p style='color:red;'>❌ Invalid or expired Token</p>")

        uid = data.get("id", "N/A")
        name = data.get("name", "N/A")
        email = data.get("email", "N/A")
        birthday = data.get("birthday", "N/A")
        creation = estimate_creation(uid)

        html_result = f"""
        <h3 style='color:lime;'>✅ Valid Token Detected</h3>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>UID:</strong> {uid}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Birthday:</strong> {birthday}</p>
        <p><strong>Estimated Account Creation:</strong> {creation}</p>
        <p><strong>Access Token:</strong><br>{token}</p>
        """
        return render_template_string(HTML_TEMPLATE, result=html_result)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE, result=f"<p style='color:red;'>⚠️ Error: {str(e)}</p>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
