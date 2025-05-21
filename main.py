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
        <img src="https://i.ibb.co/nvzcqdh/481763241-970223151881676-1859266586914038652-n.jpg" alt="Banner">
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
    app.run(host='0.0.0.0', port=5000)
