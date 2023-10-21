cd Scripts
set FLASK_APP=superset
superset init
superset run -p 8088 --with-threads --reload --debugger