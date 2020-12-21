
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from stock_base.utils import send_text_message

from stock_base.fsm import TocMachine

states = ["user","state_cat","state_cat_show","state_cat_dog","state_fsm","state_stock","state_Tw50","state_RL","state_performance","state_stock_list","state_intro"]
transitions = [
    {
        "trigger": "advance",
        "source": ["user"],
        "dest": "state_cat",
        "conditions": "going_to_state_cat",
    },
    {
        "trigger": "advance",
        "source": ["state_cat"],
        "dest": "user",
        "conditions": "back_to_pre_state",
    },
    {
        "trigger": "advance",
        "source": ["state_cat","state_cat_show"],
        "dest": "state_cat_show",
        "conditions": "going_to_state_cat",
    },
    {
        "trigger": "advance",
        "source": ["state_cat", "state_cat_dog"],
        "dest": "state_cat_dog",
        "conditions": "going_to_state_cat_dog",
    },
    {
        "trigger": "advance",
        "source": ["state_cat_show","state_cat_dog"],
        "dest": "state_cat",
        "conditions": "back_to_pre_state",
    },
    {
        "trigger":"advance",
        "source":"user",
        "dest":"state_stock",
        "conditions":"going_to_state_stock",
    },
    {
        "trigger": "advance",
        "source": "user",
        "dest": "state_fsm",
        "conditions": "going_to_state_fsm",
    },
    {
        "trigger":"advance",
        "source":"state_stock",
        "dest":"state_Tw50",
        "conditions":"going_to_state_Tw50",
    },
    {
        "trigger":"advance",
        "source":"state_stock",
        "dest":"state_RL",
        "conditions":"going_to_state_RL",
    },
    {
        "trigger": "advance",
        "source": "state_Tw50",
        "dest": "state_stock",
        "conditions":"back_to_pre_state",
    },
    {
        "trigger": "advance",
        "source": "state_RL",
        "dest": "state_stock",
        "conditions": "back_to_pre_state",
    },

    {
        "trigger": "advance",
        "source": "state_stock",
        "dest": "user",
        "conditions": "back_to_pre_state",
    },
    {
        "trigger": "go_back",
        "source": "state_fsm",
        "dest": "user",
    },
    {
        "trigger": "advance",
        "source": "state_Tw50",
        "dest": "state_performance",
        "conditions": "going_to_state_performance",
    },
    {
        "trigger": "advance",
        "source": "state_Tw50",
        "dest": "state_intro",
        "conditions": "going_to_state_intro",
    },
    {
        "trigger": "advance",
        "source": "state_Tw50",
        "dest": "state_stock_list",
        "conditions": "going_to_state_stock_list",
    },
    {
        "trigger": "advance",
        "source": ["state_performance", "state_stock_list", "state_intro"],
        "dest": "state_Tw50",
        "conditions": "back_to_tw",
    },

    {
        "trigger": "advance",
        "source": "state_RL",
        "dest": "state_performance",
        "conditions": "going_to_state_performance",
    },
    {
        "trigger": "advance",
        "source": "state_RL",
        "dest": "state_intro",
        "conditions": "going_to_state_intro",
    },
    {
        "trigger": "advance",
        "source": "state_RL",
        "dest": "state_stock_list",
        "conditions": "going_to_state_stock_list",
    },
    {
        "trigger": "advance",
        "source": ["state_performance", "state_stock_list", "state_intro"],
        "dest": "state_RL",
        "conditions": "back_to_rl",
    },
]

machine = TocMachine(states=states, transitions=transitions, initial="user", auto_transitions=False, show_conditions=True)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message,TextMessage):
                continue

            line_bot_api.reply_message(  # 回復傳入的訊息文字
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
@csrf_exempt
def send_message_test(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue
            print(f"\nFSM STATE: {machine.state}")
            print(f"REQUEST BODY: \n{body}")
            response = machine.advance(event)
            if response == False:
                send_text_message(event.reply_token, "Not Entering any State")


    return HttpResponse()