import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_image_message

load_dotenv()


machine = TocMachine(
    states=["user", "state1", "state2","state3","state4","find_flight","find_flight1","find_airport","find_airport1"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
        {
            "trigger": "advance",
            "source": "state3",
            "dest": "find_flight",
            "conditions": "is_going_to_find_flight",
        },
        {
            "trigger": "advance",
            "source": "find_flight",
            "dest": "find_flight1",
            "conditions": "is_going_to_find_flight",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state4",
            "conditions": "is_going_to_state4",
        },
        {
            "trigger": "advance",
            "source": "state4",
            "dest": "find_airport",
            "conditions": "is_going_to_find_airport",
        },
        {
            "trigger": "advance",
            "source": "find_airport",
            "dest": "find_airport1",
            "conditions": "is_going_to_find_airport",
        },
        {"trigger": "cycle", "source": ["find_airport1"], "dest": "find_airport"}
        ,{"trigger": "forward_airport", "source": ["state4"], "dest": "find_airport"},
        {"trigger": "gobackitself", "source": ["find_flight1"], "dest": "find_flight"}
        ,{"trigger": "forward_flight", "source": ["state3"], "dest": "find_flight"}
        ,{"trigger": "go_back", "source": ["state1", "state2","find_flight1","find_airport1"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if event.message.text=="show-fsm":
                machine.get_graph().draw("fsm.png", prog="dot", format="png")
                send_image_message(event.reply_token,"https://airplaneinformation.herokuapp.com/show-fsm")
                #send_text_message(event.reply_token, "hi")
            else:
                send_text_message(event.reply_token, "沒有此指令\n可以使用指令:\n即時出境航班\n即時入境航班\n查詢特定航班")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
