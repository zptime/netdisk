. /opt/virt/netdisk/bin/activate

# use chutianyun pypi repo to install requirements
pip install -r requirements.txt --no-index --find-links=http://192.168.100.21/pypi  --trusted-host 192.168.100.21
