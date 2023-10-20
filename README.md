# trias-bi
Trias app setup with bi in local system

*Requirements

python ver >= 3

USE THESE COMMANDS TO INSTALL THE PORTABLE FILE

cd python-3.10.11-embed-amd64

python install.py

To run after first install

cd python-3.10.11-embed-amd64/Scripts

set FLASK_APP=superset

:: Load some data to play with (optional)

superset load_examples

:: Create default roles and permissions

superset init

:: Start web server on port 8088

superset run -p 8088 --with-threads --reload --debugger
