#!/usr/bin/env python
# coding: utf-8
import ssl
import sys
import os
import base64
import subprocess
from base64 import b85decode, b85encode
from urllib.request import urlopen
unverified_context = ssl._create_unverified_context()
ver = "".join(sys.version.split(".")[:2])

import urllib.error

class DownloadError(Exception):
    pass

"""Modify as needed"""
MIRROR = "https://mirrors.aliyun.com/pypi/simple/"
PASSWORD = 'admin'
USERNAME = 'admin'
FIRSTNAME = 'Trias'
LASTNAME = 'Admin'
EMAIL = 'admin@trias.in'
PORT = 8088
SUPERSET_VER = '2.1.0'

def check_os():
    if sys.platform == 'win32':
        if os.environ.get('PROGRAMFILES(X86)'):
            return True
        else:
            raise OSError('32-bit Windows not supported')
    else:
        return False

def get_filename_from_url(url):
    if "/" in url:
        filename = url.split("/")[-1]
    return filename

def download(url):
    try:
        filename = get_filename_from_url(url)
        print(f"downloading {filename}")
        if not os.path.exists(filename):
            with urlopen(url, context=unverified_context) as r:
                if r.code != 200:
                    raise DownloadError(f"Download failed, HTTP status code: {r.code}")
                with open(filename, 'wb') as f:
                    f.write(r.read())
        return True
    except Exception as ex:
        print(ex)
        return False

if os.path.exists(f"python{ver}._pth"):
    print(f"modify python{ver}._pth")
    with open(f"python{ver}._pth", "r") as f:
        txt = f.read().replace("#import", "import")

    with open(f"python{ver}._pth", "w") as f:
        f.write(txt)

url = 'https://bootstrap.pypa.io/pip/get-pip.py'
download(url)

print('installing pip...')

cmd = ['python', 'get-pip.py', '-i', MIRROR]
subprocess.run(cmd, shell=False)

def install(pkgs):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + pkgs + ['-i', MIRROR])

def install_python_geohash():
    if check_os():
        if ver not in ['38', '39', '310']:
            raise OSError('Other Python versions are not supported.')
        url = f"https://download.lfd.uci.edu/pythonlibs/archived/python_geohash-0.8.5-cp{ver}-cp{ver}-win_amd64.whl"
        download(url)
        install([f"python_geohash-0.8.5-cp{ver}-cp{ver}-win_amd64.whl"])

def install_requirements():
    install_python_geohash()
    url = f"https://raw.githubusercontent.com/apache/superset/{SUPERSET_VER}/requirements/base.txt"
    download(url)
    print("modify base.txt")
    with open("base.txt", "r") as f:
        txt = (f.read()
               .replace("-e file:.", "#-e file:.")
               .replace("pyrsistent==0.16.1", "pyrsistent==0.18.1")
               )
    with open(f"requirements.txt", "w") as f:
        f.write(txt)
    install(["-r", "requirements.txt", "sqlalchemy-drill", "flask-cors"])
    install(['apache-superset'])
    install(["mysqlclient", "pymssql", "psycopg2-binary", "clickhouse-sqlalchemy", "pillow"])

install_requirements()

def create_secret_key():
    random_bytes = os.urandom(42)
    base64_encoded = base64.b64encode(random_bytes)
    return base64_encoded.decode('utf-8')

# DATA = b'''
# Your base64 data here...
# '''

# with open('app.py', 'wb') as f:
#     f.write(b85decode(DATA.replace(b"\n", b""))

url = "https://raw.githubusercontent.com/alitrack/superset_app/master/app.py"
download(url)
url = "https://raw.githubusercontent.com/alitrack/superset_app/master/superset_config_ex.py"
download(url)

def init_db():
    subprocess.run(f'python app.py --help'.split(' '), shell=True)
    subprocess.run(f'python app.py db upgrade'.split(' '), shell=True)
    subprocess.run(f'python app.py fab create-admin --password {PASSWORD} --username {USERNAME} --firstname {FIRSTNAME} --lastname {LASTNAME} --email {EMAIL}'.split(' '), shell=True)
    subprocess.run(f'python app.py init'.split(' '), shell=True)

init_db()

run_cmd = f"""
python app.py run -p 8088 --with-threads --reload --debugger
pause
"""

with open('run.cmd', 'w') as f:
    f.write(run_cmd)
