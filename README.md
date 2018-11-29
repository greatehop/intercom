
# Intercom

## Description

It's simple onepage webapp on Flask.

## Installation

All setup exist in run.sh, but you can do it manually

    cd /path/to/app/intercom/
    virtualenv venv
    source venv/bin/activate

    # update pip if needed
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    wget https://bootstrap.pypa.io/get-pip.py -O get-pip.py
    python get-pip.py
    rm -f get-pip.py

    pip install -r requirements.txt

## Run

### Standalone

    /path/to/app/intercom/venv/bin/python /path/to/app/intercom/run.py > /dev/null 2>&1 &

### Systemd unit

    sudo cp /path/to/app/intercom/system/intercom.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl start intercom

### Nginx WSGI module

### Docker
docker build -t intercom .

#TODO: fix it
docker run --rm -it -p 5000:5000 intercom
docker run -d -p 5000:5000 intercom
