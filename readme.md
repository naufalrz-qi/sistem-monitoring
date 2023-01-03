# API & SITE SISTEM MONITORING

Flask Sistem Monitoring Siswa
Backend with flask
Frontend with flask and template AdminLTE
Frontend android with flutter

## Description

Sistem Monitoring Siswa API & Site, yang di bangun menggunan Flask Framework

## Structure Project

```
├── app/
│   ├── backend/
│   │   ├── controller/
│   │   │   ├── auth_controller.py
│   │   │   ├── data_controller.py
│   │   │   ├── download_controller.py
│   │   │   ├── guru_controller.py
│   │   │   ├── master_controller.py
│   │   │   └── siswa_controller.py
│   │   ├── lib/
│   │   │   ├── base_model.py
│   │   │   ├── custom_model_class.py
│   │   │   ├── date_time.py
│   │   │   ├── status_code.py
│   │   │   └── uploader.py
│   │   ├── models/
│   │   │   ├── data_model.py
│   │   │   ├── master_model.py
│   │   │   ├── user_detail_model.py
│   │   │   └── user_model.py
│   │   └── static/
│   │       ├── doc/
│   │       └── img/
│   │           ├── admin/
│   │           ├── guru/
│   │           └── siswa/
│   │               ├── foto/
│   │               └── qr_code/
│   ├── site/
│   │   ├── controller/
│   │   │   ├── admin_controller.py
│   │   │   ├── data_preprocessing_controller.py
│   │   │   ├── guru_controller.py
│   │   │   ├── login_controller.py
│   │   │   └── wali_kelas_controller.py
│   │   ├── forms/
│   │   │   ├── form_absen.py
│   │   │   ├── form_auth.py
│   │   │   ├── form_guru.py
│   │   │   ├── form_letter_report.py
│   │   │   ├── form_master.py
│   │   │   └── form_siswa.py
│   │   ├── lib/
│   │   │   ├── base_url.py
│   │   │   ├── json.py
│   │   │   └── template_filter.py
│   │   ├── models/
│   │   │   └── user_logi_model.py
│   │   ├── static/
│   │   ├── templates/
│   │   ├── extensions.py
│   │   └── register_app.py
│   └── __init__.py
├── env
├── migrations
├── temp
├── .env
├── data.json
├── passenger_wsgi.py
├── requirements.txt
└── settings.py
```

## Create Env

```bash
#windows
py -m venv env

#linux and macOS
python3 -m venv env
```

## Activate env

```bash
# in terminal
#
# windows terminal
env\scripts\activate
#
# git window
. env/scripts/activate
# or
source env/scripts/activate
#
# linux, macOS
. env/bin/activate

```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

## Package List

```python
# result package after installation
autopep8==2.0.0
Flask==2.2.2
Flask-Admin==1.6.0
Flask-JWT-Extended==4.4.4
Flask-Login==0.6.2
Flask-Migrate==3.1.0
Flask-SQLAlchemy==2.5.1
Flask-WTF==1.0.1
mysqlclient==2.1.1
Pillow==9.2.0
python-dotenv==0.21.0
pytz==2022.2.1
qrcode==7.3.1
requests==2.28.1
waitress==2.1.2
xlwt==1.3.0

```

## Usage

```bash
# on terminal
# step-1 : create table in the xampp or other and init database table
flask db init
flask db migrate
flask db upgrade
#
# step-2 : running flask
flask run
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
