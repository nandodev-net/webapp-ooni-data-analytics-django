from apps.api.fp_tables_api.s3_ingest import request_s3_meas_data
import datetime
import time

ini_date_str = '27-09-2021'
end_date_str = '28-09-2021'


test_types = ['tor']

first_date = datetime.datetime.strptime(ini_date_str, '%d-%m-%Y').date()
first_date_ = datetime.datetime.strptime(ini_date_str, '%d-%m-%Y').date()
last_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y').date()

delta = datetime.timedelta(days=1)
time_ini = time.time()

while first_date < last_date:
    print('Getting measurements from: ', first_date, ' to: ', first_date+delta)
    request_s3_meas_data(test_types=test_types,first_date=first_date, last_date=first_date+delta, is_macro_ingest=True)
    first_date = first_date + delta
    

time_end = time.time()
print('\n\nS3 TOTAL ingest time: ', time_end-time_ini)
print(first_date_, ' ', last_date)