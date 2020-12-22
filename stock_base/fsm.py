from transitions.extensions import GraphMachine

from stock_base.utils import*
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
import sys,os
import numpy as np
fsm_image_url = "https://i.imgur.com/QiLXZJq.jpg"
import tensorflow as tf



class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.current_model=""
    ## For judge whitch state to go

    def going_to_state_cat(self,event):
        text = event.message.text
        return text.lower() == "cat"
    def going_to_state_cat_dog(self,event):
        text = event.message.text
        return text.lower() == "cat_dog"
    def going_to_state_fsm(self,event):
        text = event.message.text
        return text.lower() == "fsm"
    def going_to_state_stock(self,event):
        text = event.message.text
        return text.lower() == "stock"
    def going_to_state_Tw50(self,event):
        text = event.message.text
        return text.lower() == "tw50"
    def going_to_state_RL(self,event):
        text = event.message.text
        return text.lower() == "rl"

    def going_to_state_performance(self,event):
        text = event.message.text
        return text.lower() == "performance"
    def going_to_state_intro(self,event):
        text = event.message.text
        return text.lower() == "intro"
    def going_to_state_stock_list(self,event):
        text = event.message.text
        return text.lower() == "stock_list"

    def back_to_pre_state(self, event):
        text = event.message.text
        return text.lower() == "back"
    def back_to_rl(self,event):
        text = event.message.text
        return text.lower() == "back_rl"
    def back_to_tw(self, event):
        text = event.message.text
        return text.lower() == "back_tw"

    ## For action entering a state
    def on_enter_state_cat(self,event):
        print('cat')
        show_cat_menu(event.reply_token)
    def on_enter_state_cat_show(self,event):
        print('cat show')
        send_cat_picture(event.reply_token)
    def on_enter_state_cat_dog(self,event):
        print(tf.version.VERSION)
        print('cat or dog')
        text = TextSendMessage(text="請上傳一張圖片:")
        line_bot_api.reply_message(event.reply_token,text)

    def on_enter_state_judge(self,event):
        print('judge')
        file = './cat/judge.jpg'
        if os.path.exists(file):

            print("辨識中")
            net = load_model('./cat/model-resnet50-final.h5')
            cls_list = ['cats', 'dogs']
            img = image.load_img(file, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            pred = net.predict(x)[0]
            top_inds = pred.argsort()[::-1][:5]
            os.remove(file)
            print("辨識完成")
            # result=""
            for i in top_inds:
                print('    {:.3f}  {}'.format(pred[i], cls_list[i]))
            result=cls_list[0]+":"+str(round(pred[0],3))+"\n"+cls_list[1]+":"+str(round(pred[1],3))
            print(result)
            text = TextSendMessage(text=result)
            action=TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='Menu',
                    text=' ',
                    actions=[
                        MessageTemplateAction(
                            label='繼續辨識',
                            text='cat_dog',
                        ),
                        MessageTemplateAction(
                            label='Back',
                            text='back',
                        ),
                    ]
                )
            )

            line_bot_api.reply_message(event.reply_token,[text,action])
        else:
            print("no",file)

    def on_enter_state_fsm(self,event):
        print("I'm entering state_fsm")
        send_image_message(event.reply_token,fsm_image_url)
        self.go_back()
    def on_enter_state_stock(self,event):
        print("I'm entering state_stock")
        reply_token = event.reply_token
        send_tempelate_message_choose_model(reply_token)
        # send_text_message(reply_token, "Eneter stock state")


    def on_enter_state_Tw50(self,event):
        print("I'm entering Tw50")
        self.current_model="Tw50"
        reply_token = event.reply_token
        send_tempelate_message_model_info(reply_token, "ML Tw50 ensemble method")
    def on_enter_state_RL(self,event):
        print("I'm entering RL")
        self.current_model = "RL"
        reply_token = event.reply_token
        send_tempelate_message_model_info(reply_token, "Reinforcement method")



    def on_enter_state_performance(self,event):
        print("I'm entering performance",self.current_model)
        reply_token = event.reply_token
        if self.current_model=="Tw50":
            back_action = get_back_action('tw')
            text=TextSendMessage(text="這是在電機系一堂課之中的股票投資模擬績效平台，下圖的績效主要是因為目前這模型是以正反對作且以急快速停損的方式降低損失以最大化投資報酬率。實際上人類操作並沒辦法做到這種方式，所以我有特別針對這部分去做修改。所以這部分的績效圖看看就好。投資理財請謹慎小心!")
            line_bot_api.reply_message(reply_token,
                                       [text, ImageSendMessage(original_content_url="https://i.imgur.com/v9aRaUV.jpg", preview_image_url="https://i.imgur.com/v9aRaUV.jpg"),back_action])
        else:
            get_rl_performance(reply_token)
    def on_enter_state_intro(self,event):
        print("I'm entering intro",self.current_model)
        reply_token = event.reply_token
        if self.current_model=="Tw50":
            send_tw50_intro(reply_token)
        else:
            back_action = get_back_action('rl')
            text = TextSendMessage(
                text="這是一篇來自2020ICAIF的用RL做股票交易的期刊文章，把它應用在台股資料上的實作。論文名稱是Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy。\n考慮版權問題以及環境設置上會和原有環境衝突，所以這邊並不會實裝每日選股這項功能，但會在績效的地方簡單展示做出來的效果。")
            line_bot_api.reply_message(reply_token,[text,back_action])
    def on_enter_state_stock_list(self,event):
        print("I'm entering stock_list",self.current_model)
        reply_token = event.reply_token
        if self.current_model=="Tw50":
            show_stock_list_Tw50(reply_token)
        else:
            back_action = get_back_action('rl')
            text = TextSendMessage(text="to be continue")
            line_bot_api.reply_message(reply_token, [text, back_action])





