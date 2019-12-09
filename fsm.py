from transitions.extensions import GraphMachine
from flights import get_arrival_flight_information,get_departure_flight_information,get_specific_flight_information,get_specific_airport_information
from requests import request
from utils import send_text_message,send_location_message
import json
import os
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,LocationSendMessage

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "即時入境航班"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "即時出境航班"

    def is_going_to_state3(self,event):
        text = event.message.text
        return text.lower() == "查詢特定航班"
    def is_going_to_state4(self,event):
        text = event.message.text
        return text.lower() == "查詢特定機場"
    def is_going_to_find_flight(self,event):
        
        
        return True
    def is_going_to_find_flight1(self,event):
        text = event.message.text
        
        return text.lower()!=""
    def is_going_to_find_airport(self,event):
        
        
        return True
    def is_going_to_find_airport1(self,event):
        text = event.message.text
        
        return text.lower()!=""
    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        
        arrival_flight_information = get_arrival_flight_information()
        send_text_message(reply_token,arrival_flight_information )
        
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")
        
        reply_token = event.reply_token
        departure_flight_information = get_departure_flight_information()
        send_text_message(reply_token, departure_flight_information)
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
    def on_enter_state3(self, event):
        print("I'm entering state3")
        
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入航班編號\n若想離開此模式請輸入“離開”")
        #send_location_message(reply_token,'my location','台南',22.994821,120.196452)
        self.forward_flight(event)

    def on_exit_state3(self,*arg):
        print("Leaving state3")

    def on_enter_state4(self, event):
        print("I'm entering state4")
        
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入機場名稱(英文簡稱)")
        #send_location_message(reply_token,'my location','台南',22.994821,120.196452)
        self.forward_airport(event)

    def on_exit_state4(self,*arg):
        print("Leaving state4")

    def on_enter_find_flight(self, event):
        print("I'm entering find_flight")
        
        #reply_token = event.reply_token
        #send_text_message(reply_token, event.message.text)
        #print(event.message.text)
        #send_location_message(reply_token,'my location','台南',22.994821,120.196452)
        #self.gobackitself(event)
        
    def on_exit_find_flight(self,*arg):
        print("Leaving find_flight")
    def on_enter_find_flight1(self, event):
        print("I'm entering find_flight")
        
        if(event.message.text=="離開"):
            self.go_back()
        #userid=event.source.user_id
        reply_token = event.reply_token
        #call format
        #print(get_specific_flight_information(event.message.text))
        send_text_message(reply_token, get_specific_flight_information(event.message.text))
        #channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
        #line_bot_api = LineBotApi(channel_access_token)
        #line_bot_api.push_message(userid, TextSendMessage(text='https://zh-tw.flightaware.com/live/flight/SWA2542/history/20191209/'))
        #print(event.message.text)
        #send_location_message(reply_token,'my location','台南',22.994821,120.196452)
        self.gobackitself(event)
        
    def on_exit_find_flight1(self,*arg):
        print("Leaving find_flight")
    
    def on_enter_find_airport(self, event):
        print("I'm entering find_flight")
        
        #reply_token = event.reply_token
        #send_text_message(reply_token, event.message.text)
        #print(event.message.text)
        #send_location_message(reply_token,'my location','台南',22.994821,120.196452)
        #self.gobackitself(event)
        
    def on_exit_find_airport(self,*arg):
        print("Leaving find_flight")
    def on_enter_find_airport1(self, event):
        print("I'm entering find_flight")
        
        
            
        #userid=event.source.user_id
        reply_token = event.reply_token
        #call format
        #print(get_specific_airport_information(event.message.text))
        send_text_message(reply_token, get_specific_airport_information(event.message.text))
        #channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
        #line_bot_api = LineBotApi(channel_access_token)
        #line_bot_api.push_message(userid, TextSendMessage(text='https://zh-tw.flightaware.com/live/flight/SWA2542/history/20191209/'))
        #print(event.message.text)
        #send_location_message(reply_token,'my location','台南',22.994821,120.196452)
        self.go_back()
        
    def on_exit_find_airport1(self,*arg):
        print("Leaving find_flight")