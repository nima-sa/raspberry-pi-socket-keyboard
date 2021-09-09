import os

os.environ['DISPLAY'] = ':0'

from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
import pyperclip
import platform
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


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

    print('kbhit: ', k)


@socketio.on('spec')
def handle_message(data):
    k = data['key']
    pyautogui.press(k)
    print('kbhit: ', k)


@socketio.on('mouse_t')
def handle_message(data):
    x, y = data['x'], data['y']

    x = x * 50 if 1 != math.fabs(x) else x
    y = y * 50 if 1 != math.fabs(y) else y

    try:
        pyautogui.moveRel(x, y)
    except pyautogui.FailSafeException:
        pass

    print('mouse: ', (x, y))


@socketio.on('clk')
def handle_message(data):
    key = data['key']
    if key == 'r':
        pyautogui.rightClick()
    elif key == 'l':
        pyautogui.leftClick()
    elif key == 'l2':
        pyautogui.doubleClick()

    print('click: ', key)


@socketio.on('scroll')
def handle_message(data):
    x, y = data['x'], data['y']
    x, y = x * 5, y * 5
    # x = x * 2 if 1 != math.fabs(x) else x
    # y = y * 2 if 1 != math.fabs(y) else y
    if y != 0:
        pyautogui.scroll(-y)
    if x != 0:
        pyautogui.hscroll(-x)

    print('scroll: ', (x, y))


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', '5000')
