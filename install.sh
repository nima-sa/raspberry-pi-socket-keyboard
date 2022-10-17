mv ~/Desktop/raspberry-pi-socket-keyboard ~/Desktop/rpiKeyboard
python3 -m pip install --upgrade pip virtualenv
echo export PATH="/home/pi/.local/bin:$PATH" > ~/.bashrc
source ~/.bashrc
cd ~/Desktop/rpiKeyboard
virtualenv rpienv
source rpienv/bin/activate
pip install -r requirements.txt
sudo cp rpikeyboard.service /lib/systemd/system/rpikeyboard.service
systemctl enable rpikeyboard
systemctl start rpikeyboard
