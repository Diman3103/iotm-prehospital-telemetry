
ssh pi@raspberrypi.local

sudo apt update
sudo apt full-upgrade -y

sudo raspi-config

sudo apt install python3-pip python3-venv git -y
pip3 install smbus2 spidev fastapi uvicorn

mkdir ~/telemetria_sies
cd ~/telemetria_sies

nano database.py

python3 temperatura.py

python3 electrocardiograma.py

python3 main.py

cd ~/telemetria_sies
uvicorn api:app --host 0.0.0.0 --port 8000

sudo nano /etc/systemd/system/telemetria_sensores.service

[Unit]
Description=Servicio de Adquisicion de Sensores SIES 107
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/telemetria_sies
ExecStart=/usr/bin/python3 /home/pi/telemetria_sies/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

sudo nano /etc/systemd/system/telemetria_api.service

[Unit]
Description=Servicio de API REST FastAPI SIES 107
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/telemetria_sies
ExecStart=/usr/bin/uvicorn api:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

sudo systemctl enable telemetria_sensores.service
sudo systemctl enable telemetria_api.service
sudo systemctl start telemetria_sensores.service
sudo systemctl start telemetria_api.service

sudo systemctl status telemetria_sensores.service
sudo systemctl status telemetria_api.service