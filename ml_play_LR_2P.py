"""
The template of the script for the machine learning process in game pingpong
python MLGame.py -i ml_play_LR_1P.py -i ml_play_LR_2P.py pingpong EASY
"""

ball_position_history=[]
import random
class MLPlay:
    def __init__(self, side):
        """
        Constructor
        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        global ball_destination_2P
        import pickle
        import numpy as np
        #---------------------------------------------------------------------------'''
        filename = "C:\\Users\\bigse\\MLGame\\games\\pingpong\\LR_example_2P_right.sav"
        model_right = pickle.load(open(filename,'rb'))
        filename = "C:\\Users\\bigse\\MLGame\\games\\pingpong\\LR_example_2P_left.sav"
        model_left = pickle.load(open(filename,'rb'))
        #----------------------------------------------------------------------------'''
        hit_deep = 1
        ball_destination = 98
        if scene_info["frame"] == 0:
            ball_destination_2P = 98
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = random.choice(["SERVE_TO_LEFT","SERVE_TO_RIGHT"])
            return command
        platform2_edge_x = scene_info["platform_2P"][0]+35#Get platform2 location
        if scene_info['ball'][1]<80+1 and scene_info["ball_speed"][0] > 0 : #當球從 2P 向右出發，預測下一次球回來的位置
            inp_temp = np.array([scene_info["ball"][0]])
            input = inp_temp[np.newaxis, :]
            ball_destination_2P = model_right.predict(input)
        if scene_info['ball'][1]<80+1 and scene_info["ball_speed"][0] < 0 : #當球從 2P 向左出發，預測下一次球回來的位置
            inp_temp = np.array([scene_info["ball"][0]])
            input = inp_temp[np.newaxis, :]
            ball_destination_2P = model_left.predict(input)
        if self.side == "2P":
#========================================當球往2P移動時，計算球的落點==========================================
#====判斷因為目前計算方式與實際落點有誤差，只能維持到19的速度，若能優化落點計算方式，應該可以撐到更高的速度=========
            if scene_info["ball_speed"][1]<0:
                ball_destination = scene_info["ball"][0]+ (((80-scene_info["ball"][1])/scene_info["ball_speed"][1])*scene_info["ball_speed"][0])
                while ball_destination < 0 or ball_destination > 195:
                    if ball_destination < 0:
                        ball_destination = -ball_destination
                    if ball_destination > 195:
                        ball_destination = 195-(ball_destination-195)

#===================================當球往2P移動時，將板子往計算的落點移動=====================================
                if ball_destination < scene_info["platform_2P"][0]+hit_deep:
                    command = "MOVE_LEFT"
                elif ball_destination > platform2_edge_x-hit_deep:
                    command = "MOVE_RIGHT"
                else:
                    command = "NONE"
                return command
#===================================當球往1P時，將板子往預測的落點移動==========================================
            elif scene_info["ball_speed"][1]>0:
                if ball_destination_2P < scene_info["platform_2P"][0]+hit_deep:
                    command = "MOVE_LEFT"
                elif ball_destination_2P > platform2_edge_x-hit_deep:
                    command = "MOVE_RIGHT"
                else:
                    command = "NONE"
                return command
#=============================================================================================================
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False


