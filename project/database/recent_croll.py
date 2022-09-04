import data_search_exhibit as exhi
import data_search_festibal as seoul
import data_search_festibal_busan as busan
import data_search_festibal_etc as etc
import data_search_festibal_gyeonggi as gg
import subprocess
import time
import schedule
def recentjob():
    # subprocess.call("data_search_exhibit.py",shell=True)
    # subprocess.call("data_search_festibal_busan.py",shell=True)
    # subprocess.call("data_search_festibal_etc.py",shell=True)
    # subprocess.call("data_search_festibal_gyeonggi.py",shell=True)
    # subprocess.call("data_search_festibal.py",shell=True)
    print('잠시 운행 정지')

schedule.every().day.at("10:30").do(recentjob)

while True:
    schedule.run_pending()
    time.sleep(1)
