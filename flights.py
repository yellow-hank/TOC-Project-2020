from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
import os
import json
from pandas.io.json import json_normalize
import pandas as pd


app_id =os.getenv("APP_ID", None)
app_key =os.getenv("APP_KEY", None)
class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

def format_arrival_flight_information(inform):
    #formatted ="飛行日期:"+inform['FlightDate']
    formatted="航班編號:"+inform['AirlineID']+inform['FlightNumber']
    formatted+="\n出發地:"+inform['DepartureAirportID']
    formatted+="\n目的地:"+inform['ArrivalAirportID']
    formatted+="\n預定抵達時間:"+inform['ScheduleArrivalTime']
    formatted+="\n預估抵達時間:"+inform['EstimatedArrivalTime']
    formatted+="\n飛機狀態:"+inform['ArrivalRemark']
    formatted+="\n航廈:"+inform['Terminal']
    formatted+="\n登機門:"+inform['Gate']
    return formatted
def format_departure_flight_information(inform):
    #formatted ="飛行日期:"+inform['FlightDate']
    formatted="航班編號:"+inform['AirlineID']+inform['FlightNumber']
    formatted+="\n出發地:"+inform['DepartureAirportID']
    formatted+="\n目的地:"+inform['ArrivalAirportID']
    formatted+="\n預定出發時間:"+inform['ScheduleDepartureTime']
    formatted+="\n預估出發時間:"+inform['EstimatedDepartureTime']
    formatted+="\n飛機狀態:"+inform['DepartureRemark']
    formatted+="\n航廈:"+inform['Terminal']
    formatted+="\n登機門:"+inform['Gate']

    return formatted
def format_specific_flight_information(inform):
    formatted=""
    if(inform['DepartureAirportID']=="TPE"):
        formatted="航班編號:"+inform['AirlineID']+inform['FlightNumber']
        formatted+="\n出發地:"+inform['DepartureAirportID']
        formatted+="\n目的地:"+inform['ArrivalAirportID']
        formatted+="\n預定出發時間:"+inform['ScheduleDepartureTime']
        formatted+="\n預估出發時間:"+inform['EstimatedDepartureTime']
        formatted+="\n飛機狀態:"+inform['DepartureRemark']
        formatted+="\n航廈:"+inform['DepartureTerminal']
        formatted+="\n登機門:"+inform['DepartureGate']
    if(inform['ArrivalAirportID']=="TPE"):
        formatted="航班編號:"+inform['AirlineID']+inform['FlightNumber']
        formatted+="\n出發地:"+inform['DepartureAirportID']
        formatted+="\n目的地:"+inform['ArrivalAirportID']
        formatted+="\n預定抵達時間:"+inform['ScheduleArrivalTime']
        formatted+="\n預估抵達時間:"+inform['EstimatedArrivalTime']
        formatted+="\n飛機狀態:"+inform['ArrivalRemark']
        formatted+="\n航廈:"+inform['ArrivalTerminal']
        formatted+="\n登機門:"+inform['ArrivalGate']
    return formatted
def get_departure_flight_information():
    a = Auth(app_id, app_key)
    current_date=datetime.now().date()
    current_time=datetime.now().time()
    request_web='https://ptx.transportdata.tw/MOTC/v2/Air/FIDS/Airport/Departure/TPE?$filter=date(ScheduleDepartureTime)%20ge%20'+str(current_date)+'%20and%20time(ScheduleDepartureTime)%20ge%20'+str(current_time)+'&$top=30&$format=JSON'
    response = request('get', request_web, headers= a.get_auth_header())
    p=json.loads(response.content)
    total_information =""
    
    for i in range(10):
        total_information += format_departure_flight_information(p[i])
        if(i!=9):
            total_information += "\n\n"
        
    return total_information
def get_arrival_flight_information():
    a = Auth(app_id, app_key)
    current_date=datetime.now().date()
    current_time=datetime.now().time()
    request_web='https://ptx.transportdata.tw/MOTC/v2/Air/FIDS/Airport/Arrival/TPE?$filter=date(ScheduleArrivalTime)%20ge%20'+str(current_date)+'%20and%20time(ScheduleArrivalTime)%20ge%20'+str(current_time)+'&$top=30&$format=JSON'
    response = request('get', request_web, headers= a.get_auth_header())
    p=json.loads(response.content)
    total_information =""
    for i in range(10):
        total_information += format_arrival_flight_information(p[i])
        if(i!=9):
            total_information += "\n\n"
        
    return total_information

def get_specific_flight_information(flight_no):
    a = Auth(app_id, app_key)
    current_date=datetime.now().date()
    current_time=datetime.now().time()
    request_web='https://ptx.transportdata.tw/MOTC/v2/Air/FIDS/Flight/'+str(flight_no)+'?$top=30&$format=JSON'
    response = request('get', request_web, headers= a.get_auth_header())
    p=json.loads(response.content)
    total_information =""
    for i in range(len(p)):
        total_information += format_specific_flight_information(p[i])
        if(i!=len(p)-1):
            if(not(p[i]['DepartureAirportID']=="TPE" or p[i]['ArrivalAirportID']=="TPE")):
                continue
            total_information += "\n\n"
    return total_information
"""if __name__ == '__main__':
    a = Auth(app_id, app_key)
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v2/Air/FIDS/Airport/Arrival/TPE?$top=10&$format=JSON', headers= a.get_auth_header())
    
    #print (json.dumps(response.content, sort_keys=True, indent=4, separators=(',', ': ')))
    
    df = pd.read_json(response.content)
    #dataframe = pd.DataFrame(df)
    #p=json.loads(response.content)
    print(df)
    #for i in range(10):
        #print(p[i]['FlightDate'])
    #print(response.content["FlightDate"])
"""