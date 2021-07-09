import secret
import requests
import datetime
import calendar

def oura_ring():
    api_key = secret.oura_api_key

    oura_base_url = "https://api.ouraring.com/v1/sleep?access_token={}"

    response = requests.get(oura_base_url.format(api_key)).json()
    

    if response['sleep']: 
        day = response['sleep'][-1]['summary_date']
        sleep_night = datetime.datetime.strptime(day, "%Y-%m-%d")
        
        oura = {
                'sleep_date': calendar.day_name[sleep_night.weekday() + 1],
                'sleep_score': response['sleep'][-1]['score'],
                'sleep_duration': round((response['sleep'][-1]['total'] / 3600), 2)
            }
    
    else: 
        oura = {
                'sleep_date': "Sleep Date",
                'sleep_score': "0",
                'sleep_duration': "0"
            }
            
    return oura