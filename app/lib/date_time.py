from datetime import datetime
import pytz

def utc_makassar():
    utc = pytz.timezone('Asia/Makassar')
    utc_mks = datetime.now(utc)
    
    return utc_mks
