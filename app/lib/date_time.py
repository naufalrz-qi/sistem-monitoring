from datetime import datetime
import pytz
import time

def utc_makassar():
    utc = pytz.timezone('Asia/Makassar')
    utc_mks = datetime.now(utc)
    
    return utc_mks

def today_():
    week_days = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu']
    local_time = time.localtime()
    today = local_time.tm_wday
    return week_days[today] 


def tomorrow_():
    week_days = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu']
    local_time = time.localtime()
    tomorrow = local_time.tm_wday
    return week_days[tomorrow + 1]

def day_now_indo():
    WEEKDAYSLIST = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    MONTHLIST= ('Januari', 'Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember')
    
    now = time.localtime()
    
    hari = WEEKDAYSLIST[now.tm_wday]
    tgl = now.tm_mday
    bulan = MONTHLIST[now.tm_mon -1]
    tahun = now.tm_year
    format_indo = hari, tgl, bulan, tahun
    return format_indo