from app import app 

@app.template_filter('fdate_indo')
def format_date_indo(date):
    WEEKDAYSLIST = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    MONTHLIST= ('Januari', 'Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember')
    
    hari = WEEKDAYSLIST[date.weekday()]
    tgl = date.day
    bulan = MONTHLIST[date.month -1]
    tahun = date.year
    format_indo = hari +', '+ str(tgl)+'-'+ bulan +'-'+ str(tahun)
    return format_indo