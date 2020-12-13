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
        send_text_message(reply_token, "Eneter performance")

    def on_enter_state_intro(self,event):
        print("I'm entering intro",self.current_model)
        reply_token = event.reply_token
        send_text_message(reply_token, "Eneter intro")
    def on_enter_state_stock_list(self,event):
        print("I'm entering stock_list",self.current_model)
        reply_token = event.reply_token
        send_text_message(reply_token, "Eneter stock list")




    #
    # def on_exit_state1(self):
    #     print("Leaving state1")
    #
    # def on_enter_state2(self, event):
    #     print("I'm entering state2")
    #
    #     reply_token = event.reply_token
    #     send_text_message(reply_token, "Trigger state2")
    #     self.go_back()
    #
    # def on_exit_state2(self):
    #     print("Leaving state2")