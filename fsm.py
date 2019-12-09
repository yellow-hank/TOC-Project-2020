from transitions.extensions import GraphMachine
from flights import get_arrival_flight_information,get_departure_flight_information,get_specific_flight_information
from requests import request
from utils import send_text_message,send_location_message
import json


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
    def is_going_to_find_flight(self,event):
        text = event.message.text
        
        return True
    def is_going_to_find_flight1(self,event):
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
        self.forward(event)

    def on_exit_state3(self,*arg):
        print("Leaving state3")

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
        
        reply_token = event.reply_token
        #call format
        #print(get_specific_flight_information(event.message.text))
        send_text_message(reply_token, get_specific_flight_information(event.message.text))
        #print(event.message.text)
        #send_location_message(reply_token,'my location','台南',22.994821,120.196452)
        self.gobackitself(event)
        
    def on_exit_find_flight1(self,*arg):
        print("Leaving find_flight")