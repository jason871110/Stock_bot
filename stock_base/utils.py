import os

from linebot import LineBotApi, WebhookParser
from linebot.models import *
from django.conf import settings

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

def send_image_message(reply_token,image_url):
    line_bot_api.reply_message(reply_token,ImageSendMessage(original_content_url=image_url,preview_image_url=image_url))

def send_tempelate_message_choose_model(reply_token):
    line_bot_api.reply_message(  # 回復「選擇地區」按鈕樣板訊息
        reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='Stock models',
                text='請選擇股票模型',
                actions=[
                    PostbackTemplateAction(
                        label='ML Tw50',
                        text='tw50',
                        data='A&tw50'
                    ),
                    PostbackTemplateAction(
                        label='RL model',
                        text='RL',
                        data='A&RL'
                    ),
                    PostbackTemplateAction(
                        label='Back',
                        text='back',
                        data='A&back'
                    )

                ]
            )
        )
    )
def send_tempelate_message_model_info(reply_token,model_name):
    line_bot_api.reply_message(
        reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='Model info',
                text=model_name,
                actions=[
                    PostbackTemplateAction(
                        label='介紹',
                        text='intro',
                        data='intro'
                    ),
                    PostbackTemplateAction(
                        label='今日選股',
                        text='stock_list',
                        data='A&stock_list'
                    ),
                    PostbackTemplateAction(
                        label='績效',
                        text='performance',
                        data='A&performance'
                    ),
                    PostbackTemplateAction(
                        label='Back',
                        text='back',
                        data='A&back'
                    )

                ]
            )
        )
    )

