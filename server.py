from flask import Flask, Response
import os
import time

app = Flask(__name__)
# ВАЖНО: Проверь, что в docker-compose путь именно такой
IMAGE_PATH = "/home/jovyan/work/output_viz/live_stream.jpg"

def generate_frames():
    while True:
        if not os.path.exists(IMAGE_PATH):
            # Если файла нет - пишем в консоль докера!
            print(f"❌ ФАЙЛ НЕ НАЙДЕН ПО ПУТИ: {IMAGE_PATH}")
            time.sleep(1)
            continue
        
        try:
            with open(IMAGE_PATH, 'rb') as f:
                frame = f.read()
            
            if len(frame) < 100: # Слишком маленький файл (битый)
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"⚠️ Ошибка чтения: {e}")
            continue
        
        time.sleep(0.04)

@app.route('/video_feed')
def video_feed():
    print("✅ КТО-ТО ПОДКЛЮЧИЛСЯ К ПОТОКУ!")
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Ставим debug=True, чтобы видеть всё в логах
    app.run(host='0.0.0.0', port=5000, threaded=True)