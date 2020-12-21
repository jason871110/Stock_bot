import os

from linebot import LineBotApi, WebhookParser
from linebot.models import *
from django.conf import settings
import json
from datetime import datetime
import requests
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def show_cat_menu(reply_token):
    line_bot_api.reply_message(  # 回復「選擇地區」按鈕樣板訊息
        reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='Cat is good',
                text='請選擇貓咪服務',
                actions=[
                    MessageTemplateAction(
                        label='拿一張貓咪圖片',
                        text='cat',
                    ),
                    MessageTemplateAction(
                        label='貓狗辨識器',
                        text='cat_dog',
                    ),
                    MessageTemplateAction(
                        label='Back',
                        text='back',
                    ),
                ]
            )
        )
    )
def send_cat_picture(reply_token):
    data = requests.get('https://api.thecatapi.com/v1/images/search')
    cat_url=data.json()[0]['url']
    cat_action = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            title='貓咪狗狗一樣好',
            text=" ",
            actions=[
                MessageTemplateAction(
                    label='再一張貓咪',
                    text='cat',
                ),
                MessageTemplateAction(
                    label='Back',
                    text='back',
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token,
                               [ImageSendMessage(original_content_url=cat_url, preview_image_url=cat_url),cat_action])

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

def get_back_action(type):
    back_action = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            title=' ',
            text=" ",
            actions=[PostbackTemplateAction(
                label='Back',
                text='back_'+type,
                data='A&performance'
            )]
        )
    )
    return back_action

def send_image_message(reply_token,image_url):
    line_bot_api.reply_message(reply_token,ImageSendMessage(original_content_url=image_url,preview_image_url=image_url))

def get_rl_performance(reply_token):
    back_action = get_back_action('rl')
    money_url="https://imgur.com/8bmO0jY.jpg"
    other_url="https://imgur.com/RuI6OfS.jpg"
    money=ImageSendMessage(original_content_url=money_url, preview_image_url=money_url)
    other = ImageSendMessage(original_content_url=other_url, preview_image_url=other_url)
    money_text=TextSendMessage(text="這邊就簡單比較RL模型和台灣加權指數這一年的獲利率。藍色線是RL模型橘色線是台灣加權指，可以看到其實RL訓練出來的模型走勢根台指期非常接近。在大跌的時候會跟著大跌，大漲的時候也會大漲，比較特別的就是RL似乎可以放大波動的趨勢，簡單推測就是所學的模型為了快速最大化獲利會去選波動大的股票，像大立光這樣的股票就被長期持有。")
    line_bot_api.reply_message(reply_token,[money_text,money,other,back_action])
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
def send_tw50_intro(reply_token):
    back_action = get_back_action('tw')
    article= "ML_TW50:\nML_TW50是我將所有台灣50的成分股票以機器學習的方式分別建置50個ensemble based的模型，最後再從這些模型組出實際使用的模型來做每日交易策略的決策。\nData:\n每隻模型的training data長短其實不太一樣，是根據該支股票開始時間來做設定的。"
    article_tech="\n\n技術指標:\n這個模型比較特別的就是input有140幾種技術指標加上連續多天的資訊，所以在訓練上輸入維度會多達500多維。"
    article_model="\n\n模型:\n基礎模型我是選用Ensemble 方法中的xgboost 來做使用。主要考量是想透過boosting的概念來優化這類分類任務的效能。"
    article_work="\n\n運行:\n總共50個訓練出來的模型，我會回測2018~2020的股價資訊來看這幾隻模型的勝率和實際的效能來做實際在使用模型的時候，模型組合的選用。"
    article=article+article_tech+article_model+article_work
    line_bot_api.reply_message(reply_token, [TextSendMessage(text=article),back_action])


def show_stock_list_Tw50(reply_token):
    now = datetime.now()
    date_ = now.strftime("%Y-%m-%d")
    print(date_)
    daily_decision = json.load(open(f'strategy//{date_}_{date_}.json'))
    bad_url="https://i.imgur.com/b0G42RZ.png"
    good_url="https://i.imgur.com/FxmzScB.jpg"
    stock_li=[]
    stock_info="https://tw.stock.yahoo.com/q/bc?s="
    for stock in  daily_decision:
        stock_url=stock_info+stock['code']
        temp_token=CarouselColumn(
            thumbnail_image_url=bad_url,
            title=stock['code'],
            text='Action:'+stock['type'],
            actions=[
                URITemplateAction(
                    label='進場點:'+str(round(stock['open_price'],2)),
                    uri=stock_url
                ),
                URITemplateAction(
                    label='進損點:'+str(round(stock['close_low_price'],2)),
                    uri=stock_url
                ),
                URITemplateAction(
                    label='停利點:'+str(round(stock['close_high_price'],2)),
                    uri=stock_url
                ),
            ]
        )
        stock_li.append(temp_token)
    Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=stock_li
        )
    )

    back_action =get_back_action('tw')
    line_bot_api.reply_message(reply_token, [Carousel_template, back_action
                                             ])




