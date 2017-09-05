PATH_FULL=$(realpath $0)
PATH_PROJECT=$(dirname ${PATH_FULL})

if [ ! -d ${PATH_PROJECT}/venv ]; then
    cd ${PATH_PROJECT}
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi

${PATH_PROJECT}/venv/bin/python ${PATH_PROJECT}/run.py > /dev/null 2>&1 &


