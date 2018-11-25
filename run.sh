PATH_FULL=$(realpath $0)
PATH_PROJECT=$(dirname ${PATH_FULL})

if [ ! -d ${PATH_PROJECT}/venv ]; then
    cd ${PATH_PROJECT}
    virtualenv venv
    source venv/bin/activate

    # check and update pip version if needed
    PIP_VER=$(pip -V | grep -oP '^pip \K[^\.]+')
    PIP_URL="https://bootstrap.pypa.io/get-pip.py"
    if [ "${PIP_VER}" -lt "10" ]; then
        RET_CODE_CURL=$(which curl > /dev/null; echo $?)
        RET_CODE_WGET=$(which wget > /dev/null; echo $?)
        if [ "${RET_CODE_CURL}" -eq "0" ]; then
            curl ${PIP_URL}  -o get-pip.py
        elif [ "${RET_CODE_WGET}" -eq "0" ]; then
            wget ${PIP_URL} -O get-pip.py
        else
            echo "Please install curl or wget for updating pip"
            exit 1
        fi
    fi
    python get-pip.py
    rm -f get-pip.py

    pip install -r requirements.txt
    deactivate
fi

${PATH_PROJECT}/venv/bin/python ${PATH_PROJECT}/run.py > /dev/null 2>&1

