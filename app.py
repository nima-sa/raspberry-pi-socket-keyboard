import os

os.environ['DISPLAY'] = ':0'

from flask import Flask, render_template, make_response, send_from_directory
from flask_socketio import SocketIO
import pyautogui
import pyperclip
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

pyautogui.FAILSAFE = False


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


def return_file(name):
    response = make_response(
        # send_from_directory('static', filename=f'static/{name}'))
        send_from_directory('static', filename=name, path=f'static/{name}'))
    response.headers['Content-Type'] = 'application/javascript'
    return response


@app.route('/service-worker.js')
def sw():
    return return_file('service-worker.js')


@app.route('/precache-manifest.js')
def precache():
    return return_file('precache-manifest.js')


@app.route('/manifest.json')
def manifest():
    return return_file('manifest.json')


# @app.route('/zingtouch.min.js')
# def manifest():
#     return make_file('zingtouch.min.js')


@socketio.on('kbhit')
def handle_message(data):
    k = data['key']
    o = data['o'] == 1

    if o:
        pyautogui.press(k)
    else:
        pyperclip.copy(k)

        if platform.system() == "Darwin":
            pyautogui.hotkey("command", "v")
        else:
            pyautogui.hotkey("ctrl", "v")

    # print('kbhit: ', k)


@socketio.on('spec')
def handle_message(data):
    k = data['key']
    pyautogui.press(k)
    # print('kbhit: ', k)


@socketio.on('mouse_t')
def handle_message(data):
    x, y = data['x'], data['y']
    # x, y = x * 5, y * 5
    # x = x * 50 if 1 != math.fabs(x) else x
    # y = y * 50 if 1 != math.fabs(y) else y

    try:
        pyautogui.moveRel(x, y)
    except pyautogui.FailSafeException:
        pass

    # print('mouse: ', (x, y))


@socketio.on('clk')
def handle_message(data):
    key = data['key']
    if key == 'r':
        pyautogui.rightClick()
    elif key == 'l':
        pyautogui.leftClick()
    elif key == 'l2':
        pyautogui.doubleClick()
    # print('click: ', key)


@socketio.on('scroll')
def handle_message(data):
    x, y = data['x'], data['y']
    # x, y = x * 5, y * 5
    # x = x * 2 if 1 != math.fabs(x) else x
    # y = y * 2 if 1 != math.fabs(y) else y
    if y != 0:
        pyautogui.vscroll(y)
    if x != 0:
        pyautogui.hscroll(x)


@socketio.on('restartService')
def handle_message(data):
    os.system('sudo systemctl restart rpikeyboard')


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', '5000')
