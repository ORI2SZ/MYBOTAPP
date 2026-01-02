from flask import Flask, request
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BOT_TOKEN = "8546530820:AAFgLVnbTqg1q2kHubrcLOAyxixS2MIGw9c" 

@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video part", 400

    file = request.files['video']
    user_id = request.form.get('user_id')

    if file.filename == '':
        return "No selected file", 400

    if file and user_id:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath) 

        send_video_to_telegram(user_id, filepath)

        os.remove(filepath) 

        return "File uploaded and sent to Telegram", 200

def send_video_to_telegram(chat_id, video_path):
    url = f"api.telegram.org{BOT_TOKEN}/sendVideo"
    files = {'video': open(video_path, 'rb')}
    data = {'chat_id': chat_id, 'caption': f"אימות וידאו חדש מהמשתמש {chat_id}, מספר 6869"}
    requests.post(url, files=files, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
