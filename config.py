import colors
import numpy as np
import pandas as pd


screen_width = 1200
screen_height = 900
background_image = 'data/background-red.png'
center_screen_x = screen_width // 2
center_screen_y = screen_height // 2
poslistPK = np.array(["QB","RB","TE","WR","Def","PK"])
treeposlistPK = np.array(["Def","PK","QB","RB","TE","WR"])

site_templates = {"BB10 12 Team":{"scoring":1,"roundcount":20,"teamcount":12,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":3,"tecount":1,"defcount":1,"pkcount":0,"flexcount":1},
                  "BB10 6 Team":{"scoring":1,"roundcount":20,"teamcount":6,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":3,"tecount":1,"defcount":1,"pkcount":0,"flexcount":1},
             "BB10 3 Team":{"scoring":1,"roundcount":20,"teamcount":3,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":3,"tecount":1,"defcount":1,"pkcount":0,"flexcount":1},
             "FFPC Classic":{"scoring":2,"roundcount":28,"teamcount":12,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":2,"tecount":1,"defcount":1,"pkcount":1,"flexcount":2},
             "FFPC Slim":{"scoring":2,"roundcount":18,"teamcount":12,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":2,"tecount":1,"defcount":0,"pkcount":0,"flexcount":2},
             "FFPC SuperFlex":{"scoring":2,"roundcount":28,"teamcount":12,"superflex":1,"qbcount":1,"rbcount":2,"wrcount":2,"tecount":1,"defcount":1,"pkcount":1,"flexcount":2},
             "FFPC SF Slim":{"scoring":2,"roundcount":18,"teamcount":12,"superflex":1,"qbcount":1,"rbcount":2,"wrcount":2,"tecount":1,"defcount":0,"pkcount":0,"flexcount":2},
             "DK 12 Team":{"scoring":1,"roundcount":20,"teamcount":12,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":3,"tecount":1,"defcount":0,"pkcount":0,"flexcount":1},
             "UD 12 Team":{"scoring":0,"roundcount":18,"teamcount":12,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":3,"tecount":1,"defcount":0,"pkcount":0,"flexcount":1},
             "UD 6 Team":{"scoring":0,"roundcount":18,"teamcount":6,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":3,"tecount":1,"defcount":0,"pkcount":0,"flexcount":1},
             "UD 3 Team":{"scoring":0,"roundcount":18,"teamcount":3,"superflex":0,"qbcount":1,"rbcount":2,"wrcount":3,"tecount":1,"defcount":0,"pkcount":0,"flexcount":1}}

frame_rate = 2


teamcount = 12
brick_width = 74
brick_height =26
roster_brick_width1 = 30
roster_brick_width2 = 200
roster_brick_height = 20

standings_brick_width = 55
standings_brick_height = 16

brick_color = colors.WHITE
qb_color = colors.PINK
rb_color = colors.LIMEGREEN
te_color = colors.LIGHTBLUE
wr_color = colors.YELLOW1
def_color = colors.ORANGE
pk_color = colors.GOLDENROD1
team_color = colors.BLACK

grid_offset_x = 300
offset_y_start = 200
offset_y_start_header = offset_y_start -2
offset_y = 100
offset_y_header = offset_y -2

roster_offset_x1 = 10
roster_offset_x2 = roster_offset_x1 + roster_brick_width1 + 3

standings_offset_x = 40
standings_offset_y = offset_y + 22*brick_height

score_offset = 10
pick_offset = 10
pick_offset_y = 50

menu_offset_x = 10
menu_offset_y = 10
menu_button_w = 60
menu_button_h = 40
site_button_w = 100
site_button_h = 30

button_offset_x = grid_offset_x - brick_width/2
button_offset_y = offset_y_header - (menu_button_h+5)

text_color = colors.YELLOW1
pick_color = colors.BLACK
pick_button_text_color = colors.BLACK
pick_text_color = colors.WHITE


font_name = 'Arial'
font_size = 14
score_font_size = 18
roster_font_size = 12

message_duration = 1

button_text_color = colors.WHITE
button_normal_back_color = colors.BLACK
button_hover_back_color = colors.INDIANRED2
button_pressed_back_color = colors.INDIANRED3

EQUITYVALS = np.array([100,85,75,70,60,55,50,45,40,40,35,30,25,20,20,15,10,5,0,0])
draftseasons = np.array(["Feb-Apr","May-Jul","Aug-Sep"])
poslist = np.array(["Def","QB","RB","TE","WR"])

standings = pd.DataFrame({"Rk":[1,2,3,4,5,6,7,8,9,10,11,12],
                          "Team":["Team 1","Team 2","Team 3","Team 4","Team 5","Team 6","Team 7","Team 8","Team 9","Team 10","Team 11","Team 12"],
                          "Score": np.zeros(12),
                          "Week 1": np.zeros(12),
                          "Week 2": np.zeros(12),
                          "Week 3": np.zeros(12),
                          "Week 4": np.zeros(12),
                          "Week 5": np.zeros(12),
                          "Week 6": np.zeros(12),
                          "Week 7": np.zeros(12),
                          "Week 8": np.zeros(12),
                          "Week 9": np.zeros(12),
                          "Week 10": np.zeros(12),
                          "Week 11": np.zeros(12),
                          "Week 12": np.zeros(12),
                          "Week 13": np.zeros(12),
                          "Week 14": np.zeros(12),
                          "Week 15": np.zeros(12),
                          "Week 16": np.zeros(12)})

state_placeholder = [[0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0]]
