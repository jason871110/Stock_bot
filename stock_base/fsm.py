from transitions.extensions import GraphMachine

from stock_base.utils import*

fsm_image_url = "https://i.imgur.com/A7LYm3K.jpg"


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.current_model=""
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
            text=TextSendMessage(text="這是在電機系一堂課之中的股票投資模擬績效平台，下圖的績效主要是因為目前這模型是以正反對作且以急快速停損的方式降低損失以最大化投資報酬率。實際上人類操作並沒辦法做到這種方式，所以我有特別針對這部分去做修改。所以這部分的績效圖看看就好。投資理財請謹慎小心!"
                                      "")
            line_bot_api.reply_message(reply_token,
                                       [text,ImageSendMessage(original_content_url="https://i.imgur.com/v9aRaUV.jpg", preview_image_url="https://i.imgur.com/v9aRaUV.jpg")])
    def on_enter_state_intro(self,event):
        print("I'm entering intro",self.current_model)
        reply_token = event.reply_token
        if self.current_model=="Tw50":
            send_tw50_intro(reply_token)
    def on_enter_state_stock_list(self,event):
        print("I'm entering stock_list",self.current_model)
        reply_token = event.reply_token
        if self.current_model=="Tw50":
            show_stock_list_Tw50(reply_token)




