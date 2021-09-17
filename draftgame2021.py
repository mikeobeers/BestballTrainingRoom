import random
import math
import numpy as np
import pickle
import time
import pygame
import pandas as pd
from pandas.io.parsers import read_csv
import csv

"""Import helper files and functions"""
import config as c
from setupfunctions import Brick, Button, Game, TextObject, PickObject, scorecalcDL
import colors

"""Import scoring data and Autodraft models"""
scoring_csv =  "data/DLscoringdata2021.csv"
pkl_filename = "data/ALLsite_model_2021.pkl"
with open(pkl_filename, 'rb') as file:
    cpu_model = pickle.load(file)
    
with open(scoring_csv, 'r') as filereader:
    playerscoring = list(csv.reader(filereader))

playerscoring = np.array(playerscoring)
playerscoringPD = read_csv(scoring_csv)



class DraftGame(Game):
    def __init__(self,sitetemp = "BB10 12 Team"):
        Game.__init__(self, 'Best Ball Training Room', c.screen_width, c.screen_height, c.background_image, c.frame_rate,sitetemp = sitetemp)
        self.randomness = True
        self.score = 0
        self.rank = 0


        self.finalteam = []
        self.weekscores = []
        self.start_level = False
        self.bricks = None
        self.menu_buttons = []
        self.is_game_running = False
        self.state = []
        

        self.teamcount = 12
        self.roundcount = 20
        self.superflex = 0
        self.scoring = 1
        self.qbcount = 1
        self.rbcount = 2
        self.wrcount = 3
        self.tecount = 1
        self.defcount = 1
        self.pkcount = 0
        self.flexcount = 1
        self.half = 0
        self.ppr = 1
        self.teprem = 0

        self.allrosters = [ [] for i in range(self.teamcount) ]
        self.allteams = [ [] for i in range(self.teamcount) ]
        self.allyears = [ [] for i in range(self.teamcount) ]
        self.allplayers = [ [] for i in range(self.teamcount) ]
            
        self.flexposlist = ['RB','WR','TE']
        self.sflexposlist = ['QB','RB','WR','TE']
        
        self.allscores = []
        self.allweekscores = []
        self.standings = c.standings[c.standings['Rk']<=self.teamcount].copy()
        self.calculating = ""
        
        self.brick_height = math.ceil(c.brick_height * (20/self.roundcount))
        self.roster_brick_height = math.ceil(c.brick_height * (20/self.roundcount))
        self.points_per_brick = 1
        self.rbPressed = False
        self.wrPressed = False
        self.qbPressed = False
        self.tePressed = False
        self.defPressed = False
        self.pkPressed = False
        self.allEqVals = [100,99,98,96,95,94,92,91,90,88,87,85,85,85,84,83,82,81,80,79,78,77,76,75,75,75,75,74,74,73,73,72,72,71,71,70,70,70,69,68,67,66,65,64,63,62,61,60,60,60,60,59,59,58,58,57,57,56,56,55,55,55,55,54,54,53,53,52,52,51,51,50,50,50,50,49,49,48,48,47,47,46,46,45,45,45,45,44,44,43,43,42,42,41,41,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,39,39,38,38,37,37,36,36,35,35,35,35,34,34,33,33,32,32,31,31,30,30,30,30,29,29,28,28,27,27,26,26,25,25,25,25,24,24,23,23,22,22,21,21,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,19,19,18,18,17,17,16,16,15,15,15,15,14,14,13,13,12,12,11,11,10,10,10,10,9,9,8,8,7,7,6,6,5,5,5,5,5,5,5,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        self.EquityVals = c.EQUITYVALS[0:self.roundcount]
        
        self.totalpicks = self.teamcount * self.roundcount
        #self.dpos = random.randint(1, self.teamcount)
        self.dpos = 100
        self.draftseas = 0
        self.TFyear = 0
        self.timeframe = (self.TFyear-1)*3 + self.draftseas
        self.TFfinder = []
        self.TFtester = []
        self.playerscoring = []
        self.draftseasname = ""
        self.roster = []
        self.rosterdetail = []
        self.posadp = []
        self.allpicks = []
        self.allpicksdetail = []
        self.yourpick = 0
        self.pickmade = ''
        self.yourpicks = []
        self.thispick = 1
        self.thisround = 1
        self.roundpick = 1
        self.gridlocation = 0
        self.gridshape = (self.roundcount, self.teamcount)
        self.teamnames = []
        for team in range(1,self.teamcount+1):
            self.teamnames.insert(len(self.teamnames),"Team "+str(team))
        self.grid = np.repeat('TBD', self.totalpicks).reshape(self.gridshape)
        self.detailgrid = np.repeat('TBD', self.totalpicks).reshape(self.gridshape)
        self.create_menu()
        
    def getAIstate(self):
        teampicks = []
        for roundnum in range(1,self.roundcount+1):
            if (roundnum % 2) == 0:
                teampicks.insert(len(teampicks),self.teamcount*(roundnum-1) + ((self.teamcount+1)-(self.gridlocation+1)) - 1)
            else:
                teampicks.insert(len(teampicks),(self.gridlocation+1) + self.teamcount*(roundnum-1) - 1)
        thisequity = [self.allEqVals[i] for i in tuple(teampicks)]
        
        thisroster = [lis[self.gridlocation] for lis in self.grid]
        thisrosterVAL = np.array([lis[self.gridlocation] for lis in self.grid])
        placeholder = np.array(np.zeros(self.roundcount))
        WRroster = np.array(placeholder)
        WRroster[thisrosterVAL == "WR"] = 1
        WRequity = sum(np.array(WRroster)*thisequity)
        RBroster = np.array(placeholder)
        RBroster[thisrosterVAL == "RB"] = 1
        RBequity = sum(np.array(RBroster)*thisequity)
        QBroster = np.array(placeholder)
        QBroster[thisrosterVAL == "QB"] = 1
        QBequity = sum(np.array(QBroster)*thisequity)
        TEroster = np.array(placeholder)
        TEroster[thisrosterVAL == "TE"] = 1
        TEequity = sum(np.array(TEroster)*thisequity)
        DEFroster = np.array(placeholder)
        DEFroster[thisrosterVAL == "Def"] = 1
        DEFequity = sum(np.array(DEFroster)*thisequity)
        PKroster = np.array(placeholder)
        PKroster[thisrosterVAL == "PK"] = 1
        PKequity = sum(np.array(PKroster)*thisequity)
        
        thispick = len(self.allpicks) + 1
        thisround = math.ceil(thispick / self.teamcount)
        roundpick = thispick - (thisround-1) * self.teamcount
        nextpick = 0
        if thisround != self.roundcount:
            nextpick = (self.teamcount - roundpick)*2 + 1

        DLstate1 = [self.teamcount,self.roundcount,self.superflex,self.half,self.ppr,self.teprem,self.thisround,self.qbcount,self.rbcount,self.wrcount,self.tecount,self.defcount,self.pkcount,self.flexcount,nextpick,self.allpicks.count("WR"),self.allpicks.count("RB"),self.allpicks.count("QB"),self.allpicks.count("TE"),self.allpicks.count("Def"),self.allpicks.count("PK"),thisroster.count("WR"),thisroster.count("RB"),thisroster.count("QB"),thisroster.count("TE"),thisroster.count("Def"),thisroster.count("PK"),WRequity,RBequity,QBequity,TEequity,DEFequity,PKequity]
        self.AIstate = np.array(DLstate1)
        return self.AIstate

    def set_format(self,sitechoice):
            self.template = sitechoice
            site = c.site_templates[self.template]
            self.teamcount = site['teamcount']
            self.roundcount = site['roundcount']
            self.superflex = site['superflex']
            self.scoring = site['scoring']
            self.qbcount = site['qbcount']
            self.rbcount = site['rbcount']
            self.wrcount = site['wrcount']
            self.tecount = site['tecount']
            self.defcount = site['defcount']
            self.pkcount = site['pkcount']
            self.flexcount = site['flexcount']
            self.half = 0
            self.ppr = 0
            self.teprem = 0
            if self.scoring == 0:
                self.half = 1
            if self.scoring == 1:
                self.ppr = 1
            if self.scoring == 2:
                self.teprem = 1
            if self.superflex == 1:
                self.flexcount += -1
            self.allrosters = [ [] for i in range(self.teamcount) ]
            self.allteams = [ [] for i in range(self.teamcount) ]
            self.allyears = [ [] for i in range(self.teamcount) ]
            self.allplayers = [ [] for i in range(self.teamcount) ]
            self.standings = c.standings[c.standings['Rk']<=self.teamcount].copy()
            self.brick_height = math.ceil(c.brick_height * (20/self.roundcount))
            self.roster_brick_height = math.ceil(c.brick_height * (20/self.roundcount))
            self.EquityVals = c.EQUITYVALS[0:self.roundcount]
            self.totalpicks = self.teamcount * self.roundcount
            self.gridlocation = 0
            self.gridshape = (self.roundcount, self.teamcount)
            self.teamnames = []
            for team in range(1,self.teamcount+1):
                self.teamnames.insert(len(self.teamnames),"Team "+str(team))
            self.grid = np.repeat('TBD', self.totalpicks).reshape(self.gridshape)
            self.detailgrid = np.repeat('TBD', self.totalpicks).reshape(self.gridshape)
            

    def create_menu(self):
        
        def on_play(button):
            Game.__init__(self, 'Best Ball Training Room', c.screen_width, c.screen_height, c.background_image, c.frame_rate,self.template)
            self.dpos = random.randint(1, self.teamcount)
            self.draftseas = random.randint(1, 3)
            self.TFyear = random.randint(1,6)
            self.timeframe = (self.TFyear-1)*3 + self.draftseas
            self.TFfinder = np.array([lis[1] for lis in playerscoring])
            self.TFtester = [self.TFfinder == str(int(self.timeframe))]
            self.playerscoring = np.array(playerscoring[tuple(self.TFtester)])
            self.yourpick = self.dpos
            self.draftseasname = c.draftseasons[self.draftseas-1]
            self.create_labels()
            for roundnum in range(1,self.roundcount+1):
                if (roundnum % 2) == 0:
                    self.yourpicks.insert(len(self.yourpicks),self.teamcount*(roundnum-1) + ((self.teamcount+1)-self.dpos))
                else:
                    self.yourpicks.insert(len(self.yourpicks),self.dpos + self.teamcount*(roundnum-1))
            self.is_game_running = True
            self.start_level = True
            
        def on_restart(button):
            main(self.template)
            

        def on_quit(button):
            self.game_over = True
            self.is_game_running = False
            pygame.quit()
       

             
        def bb10_12_Button(button):
            self.template = "BB10 12 Team"
            self.set_format(self.template)
            
        def bb10_6_Button(button):
            self.template = "BB10 6 Team"
            self.set_format(self.template)
        
        def bb10_3_Button(button):
            self.template = "BB10 3 Team"
            self.set_format(self.template)
        
        def FFPC_Classic_Button(button):
            self.template = "FFPC Classic"
            self.set_format(self.template)

        def FFPC_Slim_Button(button):
            self.template = "FFPC Slim"
            self.set_format(self.template)
        
        def FFPC_SuperFlex_Button(button):
            self.template = "FFPC SuperFlex"
            self.set_format(self.template)
        
        def FFPC_SuperFlex_Slim_Button(button):
            self.template = "FFPC SF Slim"
            self.set_format(self.template)

        def UD_12_Button(button):
            self.template = "UD 12 Team"
            self.set_format(self.template)
                        
        def UD_6_Button(button):
            self.template = "UD 6 Team"
            self.set_format(self.template)

        def UD_3_Button(button):
            self.template = "UD 3 Team"
            self.set_format(self.template)
            
        def DK_Button(button):
            self.template = "DK 12 Team"
            self.set_format(self.template)
            
        sitelist = [i for i in c.site_templates]
        click_list = [bb10_12_Button,bb10_6_Button,bb10_3_Button,FFPC_Classic_Button,FFPC_Slim_Button,FFPC_SuperFlex_Button,FFPC_SuperFlex_Slim_Button,DK_Button,UD_12_Button,UD_6_Button,UD_3_Button]
        site_handlers = []
        for i in range(len(sitelist)):
            site_handlers.append((sitelist[i],click_list[i]))
        sitecolors = [colors.BLUEVIOLET,colors.BLUEVIOLET,colors.BLUEVIOLET,colors.CADMIUMORANGE,colors.CADMIUMORANGE,colors.CADMIUMORANGE,colors.CADMIUMORANGE,colors.HOTPINK,colors.BLACK,colors.BLACK,colors.BLACK]
        
        def create_site_buttons(sites):   
            for i, (text, click_handler) in enumerate((sites)):
                buttoncolor = sitecolors[i]
                b = Button(c.menu_offset_x + (c.site_button_w + 5) * i,
                           75,
                           c.site_button_w,
                           c.site_button_h,
                           text,
                           click_handler,
                           padding=5,
                           backcolor=buttoncolor,
                           font_size = 12)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
            self.selected_label = TextObject(c.menu_offset_x,
                                        125,
                                        lambda: "Selected:" + self.template,
                                        c.text_color,
                                        c.font_name,
                                        18)
            self.objects.append(self.selected_label)
                
        if len(self.allpicks) > 0 or self.is_game_running:
            for i, (text, click_handler) in enumerate((('Reset', on_restart), ('Quit', on_quit))):
                buttoncolor = c.button_normal_back_color
                b = Button(c.menu_offset_x + (c.menu_button_w + 5) * i,
                           c.menu_offset_y,
                           c.menu_button_w,
                           c.menu_button_h,
                           text,
                           click_handler,
                           padding=5,
                           backcolor=buttoncolor)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
        else:        
            for i, (text, click_handler) in enumerate((('Start', on_play), ('Quit', on_quit))):
                buttoncolor = c.button_normal_back_color
                b = Button(c.menu_offset_x + (c.menu_button_w + 5) * i,
                           c.menu_offset_y,
                           c.menu_button_w,
                           c.menu_button_h,
                           text,
                           click_handler,
                           padding=5,
                           backcolor=buttoncolor)
                self.objects.append(b)
                self.menu_buttons.append(b)
                self.mouse_handlers.append(b.handle_mouse_event)
            self.site_label = TextObject(c.menu_offset_x,
                                        50,
                                        lambda: "Choose Format:",
                                        c.text_color,
                                        c.font_name,
                                        18)
            self.objects.append(self.site_label)
            create_site_buttons(site_handlers)
    
    def create_Pickmenu(self):
        
        def rbButton(button):
            if self.is_game_running and self.thispick in self.yourpicks:
                self.rbPressed = True
            
        def wrButton(button):
            if self.is_game_running and self.thispick in self.yourpicks:
                self.wrPressed = True
        
        def qbButton(button):
            if self.is_game_running and self.thispick in self.yourpicks:
                self.qbPressed = True
        
        def teButton(button):
            if self.is_game_running and self.thispick in self.yourpicks:
                self.tePressed = True
        
        def defButton(button):
            if self.is_game_running and self.thispick in self.yourpicks:
                self.defPressed = True
        def pkButton(button):
            if self.is_game_running and self.thispick in self.yourpicks:
                self.pkPressed = True

        
        RBcount = self.allpicks.count("RB") + 1
        WRcount = self.allpicks.count("WR") + 1
        QBcount = self.allpicks.count("QB") + 1
        TEcount = self.allpicks.count("TE") + 1
        DEFcount = self.allpicks.count("Def") + 1
        PKcount = self.allpicks.count("PK") + 1
        
        self.otc_label = TextObject(c.button_offset_x,
                                      c.button_offset_y - 25,
                                      lambda: "YOU'RE ON THE CLOCK!",
                                      c.text_color,
                                      c.font_name,
                                      18)
        self.objects.append(self.otc_label)
        self.draft_label = TextObject(c.button_offset_x,
                                      c.button_offset_y + 10,
                                      lambda: "DRAFT:",
                                      c.text_color,
                                      c.font_name,
                                      20)
        self.objects.append(self.draft_label)
        
        buttonlist = [('QB '+str(QBcount), qbButton), ('RB '+str(RBcount), rbButton), ('WR '+str(WRcount), wrButton), ('TE '+str(TEcount), teButton), ('Def '+str(DEFcount), defButton), ('PK '+str(PKcount), pkButton)]
        if PKcount > 32 or self.pkcount < 1:
            if DEFcount < 33 and self.defcount > 0:
                buttonlist = buttonlist[:-1]
            else:
                buttonlist = buttonlist[:-2]
        else:
            if DEFcount > 32 or self.defcount < 1:
                buttonlist = buttonlist[:-2] + [buttonlist[-1]]
            
        for i, (text, click_handler) in enumerate(buttonlist):
            buttoncolor = [c.qb_color,c.rb_color,c.wr_color,c.te_color,c.def_color,c.pk_color,c.button_normal_back_color][i]
            b = Button(c.button_offset_x  + (c.menu_button_w + 5) * (i) + 80,
                       c.button_offset_y,
                       c.menu_button_w,
                       c.menu_button_h,
                       text,
                       click_handler,
                       padding=10,
                       backcolor=buttoncolor,
                       text_color = c.pick_button_text_color)
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)


    def create_objects(self,actual=False):
        self.create_bricks()
        self.create_picknames(actual=actual)
        self.create_roster_table()
        self.create_menu()

        
        
    def create_labels(self):
        self.pick_label = TextObject(c.pick_offset,
                                      c.pick_offset_y,
                                      lambda: f'{"ROUND: " + str(self.thisround) + " PICK: " + str(self.roundpick)}',
                                      c.text_color,
                                      c.font_name,
                                      c.score_font_size)
        self.pick_label2 = TextObject(c.pick_offset,
                                      c.pick_offset_y + 20,
                                      lambda: f'{"(" + str(self.thispick) + " Overall)"}',
                                      c.text_color,
                                      c.font_name,
                                      c.score_font_size)
        self.timeframe_label = TextObject(c.button_offset_x,
                              5,
                              lambda: f'{"Your " + self.template + " draft takes place some time in the months of " + self.draftseasname + " and you have pick " + str(self.dpos) + "."}',
                              c.text_color,
                              c.font_name,
                              c.score_font_size)
        self.objects.append(self.timeframe_label)
        if self.thispick <= self.totalpicks:
            self.objects.append(self.pick_label)
            self.objects.append(self.pick_label2)
    
    def report_score(self):
        self.score_label = TextObject(c.button_offset_x,
                              c.pick_offset_y,
                              lambda: f'You Scored: {round(self.score,2)}',
                              c.text_color,
                              c.font_name,
                              c.score_font_size)
        self.score_label2 = TextObject(c.button_offset_x,
                                      c.pick_offset_y + 20,
                                      lambda: f'Your Rank: {self.rank}',
                                      c.text_color,
                                      c.font_name,
                                      c.score_font_size)
        self.timeframe_label = TextObject(c.button_offset_x,
                              15,
                              lambda: f'{"Your draft took place some time in the months of " + self.draftseasname + " " + str(2014 + self.TFyear) + " and you had pick " + str(self.dpos) + "."}',
                              c.text_color,
                              c.font_name,
                              c.score_font_size)
        self.objects.append(self.score_label)
        self.objects.append(self.score_label2)
        self.objects.append(self.timeframe_label)

    def score_calc(self):
        for team in range(self.teamcount):
            teamdetail = self.allrosters[team]
            if team == (self.dpos - 1):
                self.score, self.finalteam, self.teamweeks = scorecalcDL(roster=teamdetail,playerscoring=self.playerscoring,playerscoringPD=playerscoringPD,timeframe=self.timeframe,flexposlist=self.flexposlist,sflexposlist=self.sflexposlist,QBcount=self.qbcount,WRcount=self.wrcount,RBcount=self.rbcount,TEcount=self.tecount,DEFcount=self.defcount,PKcount=self.pkcount,FLEXcount=self.flexcount,SFLEXcount=self.superflex,scoring=self.scoring)
                teamscore, teamteam, teamweeks = self.score, self.finalteam, self.teamweeks
            else:
                teamscore, teamteam, teamweeks = scorecalcDL(roster=teamdetail,playerscoring=self.playerscoring,playerscoringPD=playerscoringPD,timeframe=self.timeframe,flexposlist=self.flexposlist,sflexposlist=self.sflexposlist,QBcount=self.qbcount,WRcount=self.wrcount,RBcount=self.rbcount,TEcount=self.tecount,DEFcount=self.defcount,PKcount=self.pkcount,FLEXcount=self.flexcount,SFLEXcount=self.superflex,scoring=self.scoring)
            self.allteams[team] = list(teamteam['PlayerYear'])
            self.allyears[team] = list(teamteam['Year'])
            self.allplayers[team] = list(teamteam['Player'])
            self.standings.iloc[team,2] = teamscore
            self.standings.iloc[team,3:19] = teamweeks
            self.standings["Rk"] = self.standings.Score.rank(ascending=False).astype(int)
        self.rank = self.standings.iloc[self.dpos-1,0]

        
    def color_choose(self,pos):
        blockcolor = c.brick_color
        if pos == "RB":
            blockcolor = c.rb_color
        if pos == "WR":
            blockcolor = c.wr_color
        if pos == "TE":
            blockcolor = c.te_color
        if pos == "QB":
            blockcolor = c.qb_color
        if pos == "Def":
            blockcolor = c.def_color
        if pos == "PK":
            blockcolor = c.pk_color
        return(blockcolor)
        

    def create_bricks(self):
        w = c.brick_width
        h = self.brick_height
        brick_count = self.teamcount
        offset_x = c.grid_offset_x
        bricks = []
        offset_y = c.offset_y_start
        offset_y_header = c.offset_y_start_header
        if self.is_game_running:
            offset_y = c.offset_y
            offset_y_header = c.offset_y_header
        #Team Names
        for col in range(brick_count+1):
            brick_color = c.team_color
            if col == self.dpos:
                brick_color = colors.YELLOW1
            if col == 0:
                brick = Brick(offset_x + col * (w + 1) - w/2,
                          offset_y_header,
                          w/3,
                          h/2,
                          brick_color)
            else:
                brick = Brick(offset_x + col * (w + 1) - w/2 - 2*(w/3),
                              offset_y_header,
                              w,
                              h/2,
                              brick_color)
            bricks.append(brick)
            self.objects.append(brick)
        #Picks        
        for row in range(self.roundcount):
            for col in range(brick_count+1):
                if col == 0:
                    brick = Brick(offset_x + col * (w + 1) - w/2,
                              offset_y + (row) * (h + 1) + h/2,
                              w/3,
                              h,
                              colors.BLACK)
                else:
                    brick_color = c.brick_color
                    
                    if (row % 2) == 0:
                        thispick = (row)*self.teamcount + col
                    else:
                        thispick = (row)*self.teamcount + (self.teamcount - (col-1))
                        
                    if thispick <= len(self.allpicks):
                        picktext = self.allpicks[thispick-1]
                        brick_color = self.color_choose(pos=picktext)
                    
                    
                    brick = Brick(offset_x + col * (w + 1) - w/2 - 2*(w/3),
                                  offset_y + (row) * (h + 1) + h/2,
                                  w,
                                  h,
                                  brick_color)
                bricks.append(brick)
                self.objects.append(brick)
        self.bricks = bricks
    
    def create_picknames(self,actual=False):
        w = c.brick_width
        h = self.brick_height
        brick_count = self.teamcount
        offset_x = c.grid_offset_x

        picks = []
        offset_y = c.offset_y_start
        offset_y_header = c.offset_y_start_header
        if self.is_game_running:
            offset_y = c.offset_y
            offset_y_header = c.offset_y_header
        
        for col in range(brick_count+1):
            picktext = self.teamnames[col-1]
            text_color = c.pick_text_color
            if col == 0:
                pick = PickObject(offset_x + col * (w+1) - w/3,
                                  offset_y_header,
                                  "Rd",
                                  text_color,
                                  c.font_name,
                                  10,
                                  True,
                                  False)
            else:
                if col == self.dpos:
                    text_color = colors.BLACK    
                pick = PickObject(offset_x + col * (w+1) - 2*(w/3),
                                      offset_y_header,
                                      picktext,
                                      text_color,
                                      c.font_name,
                                      10,
                                      True,
                                      False)
            picks.append(pick)
            self.objects.append(pick)
        for row in range(self.roundcount):
            for col in range(brick_count+1):
                if col == 0:
                    pick = PickObject(offset_x + col * (w+1) - w/3,
                                      offset_y + (row+1) * (h+1),
                                      str(row+1),
                                      c.pick_text_color,
                                      c.font_name,
                                      10,
                                      True,
                                      True)
                    picks.append(pick)
                    self.objects.append(pick)
                else:   
                    if actual:
                        picktext1 = str(self.allyears[col-1][row])
                        picktext2 = self.allplayers[col-1][row]
                        pick1 = PickObject(offset_x + col * (w+1) - 2*(w/3),
                                              offset_y + (row+1) * (h+1) - h/4,
                                              picktext1,
                                              c.pick_color,
                                              c.font_name,
                                              9,
                                              True,
                                              True)
                        pick2 = PickObject(offset_x + col * (w+1) - 2*(w/3),
                                              offset_y + (row+1) * (h+1) + h/4,
                                              picktext2,
                                              c.pick_color,
                                              c.font_name,
                                              7,
                                              True,
                                              True)
                        picks.append(pick1)
                        picks.append(pick2)
                        self.objects.append(pick1)
                        self.objects.append(pick2)
                    else:
                        
                        picktext = self.grid[row][col-1]
    
                        if (row % 2) == 0:
                            thispick = (row)*self.teamcount + col
                        else:
                            thispick = (row)*self.teamcount + (self.teamcount - (col-1))
                            
                        if thispick <= len(self.allpicks):
                            picktext = self.allpicksdetail[thispick-1]
                            
                        pick = PickObject(offset_x + col * (w+1) - 2*(w/3),
                                              offset_y + (row+1) * (h+1),
                                              picktext,
                                              c.pick_color,
                                              c.font_name,
                                              14,
                                              True,
                                              True)
                        picks.append(pick)
                        self.objects.append(pick)
        self.picks = picks
        
    def create_roster_table(self,actual=False):
        w = c.roster_brick_width1
        w2 = c.roster_brick_width2
        h = self.roster_brick_height
        brick_count = self.roundcount
        offset_y = c.offset_y_start
        offset_y_header = c.offset_y_start_header
        if self.is_game_running:
            offset_y = c.offset_y
            offset_y_header = c.offset_y_header
        rosterbricks = []
        rosterpicks = []
        if actual:
            results = self.finalteam
            players = results['Pos']
            posadp = results['PosADP']
            playerdetail = results['PlayerYear']
        else:
            players = self.roster
            posadp = self.posadp
            playerdetail = self.rosterdetail

        
        brick_color = c.team_color
        brick1 = Brick(c.roster_offset_x1,
                      offset_y_header,
                      w,
                      self.brick_height/2,
                      brick_color)
        brick2 = Brick(c.roster_offset_x2,
                      offset_y_header,
                      w2,
                      self.brick_height/2,
                      brick_color)
        pick1 = PickObject(c.roster_offset_x1,
                              offset_y_header,
                              "Pos",
                              c.pick_text_color,
                              c.font_name,
                              10,
                              False,
                              False)
        pick2 = PickObject(c.roster_offset_x2,
                              offset_y_header,
                              "Player",
                              c.pick_text_color,
                              c.font_name,
                              10,
                              False,
                              False)
        rosterbricks.append(brick1)
        rosterbricks.append(brick2)
        self.objects.append(brick1)
        self.objects.append(brick2)
        rosterpicks.append(pick1)
        rosterpicks.append(pick2)
        self.objects.append(pick1)
        self.objects.append(pick2)

        brick_color = colors.WHITE
        
        if len(players) > 0:
            ph = {'Pos':players,
                  'Detail':playerdetail,
                  'PosADP':posadp}
            df = pd.DataFrame(ph)
            if actual:
                df['Order'] = pd.Categorical(players, ["QB", "RB", "WR","TE","Def","PK"])
            else:
                df['Order'] = pd.Categorical(df['Pos'], ["QB", "RB", "WR","TE","Def","PK"])
            df = df.sort_values(by=['Order','PosADP'],ascending=True)
            players = np.array(df['Pos'])
            playerdetail = np.array(df['Detail'])
            for row in range(len(players)):
                picktext = players[row]
                playertext = playerdetail[row]
                brick_color = self.color_choose(pos=picktext)
                brick1 = Brick(c.roster_offset_x1,
                          offset_y + (row) * (h + 1) + self.brick_height/2,
                          w,
                          h,
                          brick_color)
                brick2 = Brick(c.roster_offset_x2,
                          offset_y + (row) * (h + 1) + self.brick_height/2,
                          w2,
                          h,
                          brick_color)
                pick1 = PickObject(c.roster_offset_x1,
                                      offset_y + (row) * (h+1) + self.brick_height/2 +2,
                                      picktext,
                                      c.pick_color,
                                      c.font_name,
                                      c.roster_font_size,
                                      False,
                                      False)
                pick2 = PickObject(c.roster_offset_x2,
                                      offset_y + (row) * (h+1) + self.brick_height/2 +2,
                                      playertext,
                                      c.pick_color,
                                      c.font_name,
                                      c.roster_font_size,
                                      False,
                                      False)
                rosterbricks.append(brick1)
                rosterbricks.append(brick2)
                self.objects.append(brick1)
                self.objects.append(brick2)
                rosterpicks.append(pick1)
                rosterpicks.append(pick2)
                self.objects.append(pick1)
                self.objects.append(pick2)
        if len(players) < brick_count:
            for row in range(len(players),self.roundcount):
                brick_color = colors.WHITE
                brick1 = Brick(c.roster_offset_x1,
                          offset_y + (row) * (h + 1) + self.brick_height/2 +2,
                          w,
                          h,
                          brick_color)
                brick2 = Brick(c.roster_offset_x2,
                          offset_y + (row) * (h + 1) + self.brick_height/2 +2,
                          w2,
                          h,
                          brick_color)
                rosterbricks.append(brick1)
                rosterbricks.append(brick2)
                self.objects.append(brick1)
                self.objects.append(brick2)

    def create_standings_table(self):
        w = c.standings_brick_width
        h = c.standings_brick_height
        brick_count = len(self.standings.columns)
        results = self.standings
        results = results.sort_values(by=['Score'],ascending=False)
        brick_color = colors.BLACK
        
        for col in range(brick_count):
            if col == 0:
                w = c.standings_brick_width/3
                offset_x = c.standings_offset_x
            else:
                w = c.standings_brick_width
                offset_x = c.standings_offset_x + col * (w + 1) - 2*(w/3)
            brick = Brick(offset_x,
                          c.standings_offset_y,
                          w,
                          h,
                          brick_color)
            val = PickObject(offset_x + 2,
                             c.standings_offset_y,
                             results.columns[col],
                             c.pick_text_color,
                             c.font_name,
                             12,
                             False,
                             False)
            self.objects.append(brick)
            self.objects.append(val)
        
        for row in range(self.teamcount):
            for col in range(brick_count):
                if col == 0:
                    w = c.standings_brick_width/3
                    offset_x = c.standings_offset_x
                else:
                    w = c.standings_brick_width
                    offset_x = c.standings_offset_x + col * (w + 1) - 2*(w/3)
                brick_color = colors.WHITE
                picktext = str(results.iloc[row,col])
                if picktext == "Team" + " " + str(self.dpos):
                    brick_color = colors.YELLOW1
                brick = Brick(offset_x,
                          c.standings_offset_y + (row+1) * (h+1),
                          w,
                          h,
                          brick_color)
                val = PickObject(offset_x + 2,
                                      c.standings_offset_y + (row+1) * (h+1),
                                      picktext,
                                      c.pick_color,
                                      c.font_name,
                                      10,
                                      False,
                                      False)
                self.objects.append(brick)
                self.objects.append(val)
        
    def repop_grid(self):
        n = 0
        for pick in self.allpicks:
            thisround = math.ceil((n+1) / self.teamcount)
            roundpick = (n+1) - (thisround-1) * self.teamcount
            if (thisround % 2) == 0:
                gridlocation = self.teamcount-roundpick
            else:
                gridlocation = roundpick - 1
            self.grid[thisround-1][gridlocation] = pick
            n += 1
    
    def create_detailgrid(self):
        n = 0
        for pick in self.allpicksdetail:
            thisround = math.ceil((n+1) / self.teamcount)
            roundpick = (n+1) - (thisround-1) * self.teamcount
            if (thisround % 2) == 0:
                gridlocation = self.teamcount-roundpick
            else:
                gridlocation = roundpick - 1
            self.detailgrid[thisround-1][gridlocation] = pick
            n += 1
        
    def record_pick(self,pick):
        poscount = self.allpicks.count(pick) + 1
        self.allpicks.insert(len(self.allpicks),pick)
        self.allpicksdetail.insert(len(self.allpicksdetail),pick+str(poscount))
        self.roster.insert(len(self.roster), pick)
        self.rosterdetail.insert(len(self.rosterdetail),pick+str(poscount))
        self.allrosters[self.dpos-1].insert(len(self.allrosters[self.dpos-1]),pick+str(poscount))
        self.posadp.insert(len(self.posadp),poscount)
        self.thispick = len(self.allpicks) + 1
        self.thisround = math.ceil(self.thispick / self.teamcount)
        self.roundpick = self.thispick - (self.thisround-1) * self.teamcount
        if (self.thisround % 2) == 0:
            self.gridlocation = (self.teamcount-self.roundpick)
        else:
            self.gridlocation = self.roundpick - 1
        
    def AI_pick(self):
        teampicks = []
        for roundnum in range(1,self.roundcount+1):
            if (roundnum % 2) == 0:
                teampicks.insert(len(teampicks),self.teamcount*(roundnum-1) + ((self.teamcount+1)-(self.gridlocation+1)) - 1)
            else:
                teampicks.insert(len(teampicks),(self.gridlocation+1) + self.teamcount*(roundnum-1) - 1)
        thisequity = [self.allEqVals[i] for i in tuple(teampicks)]
        
        thisroster = [lis[self.gridlocation] for lis in self.grid]
        thisrosterVAL = np.array([lis[self.gridlocation] for lis in self.grid])
        placeholder = np.array(np.zeros(self.roundcount))
        WRroster = np.array(placeholder)
        WRroster[thisrosterVAL == "WR"] = 1
        WRequity = sum(np.array(WRroster)*thisequity)
        RBroster = np.array(placeholder)
        RBroster[thisrosterVAL == "RB"] = 1
        RBequity = sum(np.array(RBroster)*thisequity)
        QBroster = np.array(placeholder)
        QBroster[thisrosterVAL == "QB"] = 1
        QBequity = sum(np.array(QBroster)*thisequity)
        TEroster = np.array(placeholder)
        TEroster[thisrosterVAL == "TE"] = 1
        TEequity = sum(np.array(TEroster)*thisequity)
        DEFroster = np.array(placeholder)
        DEFroster[thisrosterVAL == "Def"] = 1
        DEFequity = sum(np.array(DEFroster)*thisequity)
        PKroster = np.array(placeholder)
        PKroster[thisrosterVAL == "PK"] = 1
        PKequity = sum(np.array(PKroster)*thisequity)
        
        self.AIstate = [self.teamcount,self.roundcount,self.scoring,self.pkcount,self.defcount,self.superflex,self.allpicks.count("WR"),self.allpicks.count("RB"),self.allpicks.count("QB"),self.allpicks.count("TE"),self.allpicks.count("Def"),self.allpicks.count("PK"),thisroster.count("WR"),thisroster.count("RB"),thisroster.count("QB"),thisroster.count("TE"),thisroster.count("Def"),thisroster.count("PK"),WRequity,RBequity,QBequity,TEequity,DEFequity,PKequity]
        
        poslist = np.array(c.treeposlistPK)
        poslist_include = np.array([True,True,True,True,True,True])
        cpu_odds = cpu_model.predict_proba(np.array(self.AIstate).reshape(1,-1))[0]
        cpu_odds = [0 if math.isnan(x) else x for x in cpu_odds]
        if thisroster.count("QB") >= 3:
            poslist_include[2] = False
        if (thisroster.count("Def") >= 3 and self.roundcount<21) or (thisroster.count("Def") >= 4 and self.roundcount > 20):
            poslist_include[0] = False
        if (thisroster.count("TE") >= 3 and self.roundcount<21) or (thisroster.count("TE") >= 4 and self.roundcount > 20):
            poslist_include[4] = False
        if self.allpicks.count("Def") >= 32:
            poslist_include[0] = False
        if self.pkcount == 0:
            poslist_include[1] = False
        if self.defcount == 0:
            poslist_include[0] = False
        poslist = poslist[poslist_include]
        cpu_odds = np.array(cpu_odds)[poslist_include]
        if self.randomness == True:
            if len(poslist) > 0 and sum(cpu_odds) > 0:
                cpu_odds = cpu_odds/sum(cpu_odds)
                cpu_odds = [0 if math.isnan(x) else x for x in cpu_odds]
                pickmade = np.random.choice(poslist,1,p=cpu_odds)[0]
            else:
                if self.allpicks.count("Def") >= 32:
                    if self.allpicks.count("PK") >= 32:
                        poslist = np.array(["QB","RB","TE","WR"])
                    else:
                        poslist = np.array(["PK","QB","RB","TE","WR"])
                else:
                    if self.allpicks.count("PK") >= 32:
                        poslist = np.array(["Def","QB","RB","TE","WR"])
                    else:
                        poslist = c.treeposlistPK
                pickmade = np.random.choice(poslist,1,)[0]
        else:
            popular = np.argmax(cpu_odds)
            pickmade = poslist[popular]
        
            
        if (self.thisround == self.roundcount - 2 and thisroster.count("QB") <= 1 and thisroster.count("Def") == 0) or (self.thisround==self.roundcount - 1 and thisroster.count("QB") == 0) or (self.thisround==self.roundcount and thisroster.count("QB") == 1):
            pickmade = "QB"
        if (self.thisround == self.roundcount - 1 and thisroster.count("TE") <= 1 and thisroster.count("Def") <= 1) or (self.thisround==self.roundcount - 1 and thisroster.count("QB") == 0) or (self.thisround==self.roundcount and thisroster.count("QB") == 1):
            pickmade = "TE"
        if (self.thisround== self.roundcount - 1 and thisroster.count("TE") == 0) or (self.thisround==self.roundcount and thisroster.count("TE") == 1):
            pickmade = "TE"
        if self.allpicks.count("Def") < 32 and self.defcount > 0 and ((self.thisround==self.roundcount - 1 and thisroster.count("Def") == 0) or (self.thisround==self.roundcount and thisroster.count("Def") == 1)):
            pickmade = "Def"
        if self.allpicks.count("PK") < 32 and self.pkcount > 0 and ((self.thisround==self.roundcount - 1 and thisroster.count("PK") == 0) or (self.thisround==self.roundcount and thisroster.count("PK") == 1)):
            pickmade = "PK"
        
        if (self.allpicks.count("Def")>31 and pickmade == "Def") or (self.allpicks.count("PK")>31 and pickmade == "PK") or (self.allpicks.count("QB")>=37 and pickmade == "QB") or (self.allpicks.count("RB")>=96 and pickmade == "RB") or (self.allpicks.count("TE")>=48 and pickmade == "TE") or (self.pkcount==0 and pickmade == "PK") or (self.defcount==0 and pickmade == "Def"):
            pickmade = "WR"
        if (self.allpicks.count("WR")>=114 and pickmade == "WR"):
            pickmade = "RB"
        
        
        self.allpicks.insert(len(self.allpicks),pickmade)
        self.allpicksdetail.insert(len(self.allpicksdetail),str(pickmade + str(self.allpicks.count(pickmade))))
        self.allrosters[self.gridlocation].insert(len(self.allrosters[self.gridlocation]),str(pickmade + str(self.allpicks.count(pickmade))))
        self.thispick = len(self.allpicks) + 1
        self.thisround = math.ceil(self.thispick / self.teamcount)
        self.roundpick = self.thispick - (self.thisround-1) * self.teamcount
        if (self.thisround % 2) == 0:
            self.gridlocation = (self.teamcount-self.roundpick)
        else:
            self.gridlocation = self.roundpick - 1
        self.repop_grid()
            
    def update(self):
        if self.is_game_running == False:
            return
        if self.thispick > self.totalpicks:
            self.objects = []
            self.show_message("Allocating Players...",centralized=True)
            self.create_detailgrid()
            self.score_calc()
            self.create_objects(actual=True)
            self.report_score()
            self.create_roster_table(actual=True)
            self.create_standings_table()
            self.is_game_running = False
            return
        
        if self.start_level:
            self.start_level = False
            self.show_message(text = 'GET READY!', centralized=True)
            
        if self.rbPressed:
            self.rbPressed = False
            self.record_pick(pick="RB")
        if self.wrPressed:
            self.wrPressed = False
            self.record_pick(pick="WR")
        if self.qbPressed:
            self.qbPressed = False
            self.record_pick(pick="QB")
        if self.tePressed:
            self.tePressed = False
            self.record_pick(pick="TE")
        if self.defPressed:
            self.defPressed = False
            self.record_pick(pick="Def")
        if self.pkPressed:
            self.pkPressed = False
            self.record_pick(pick="PK")
        
        if not self.thispick in self.yourpicks and self.thispick <= self.totalpicks:
            self.objects = []
            self.AI_pick()
            self.create_labels()
            self.create_objects()
        else:
            self.objects = []
            self.create_objects()
            self.create_labels()
            self.create_Pickmenu()
                 
        super().update()



    def show_message(self, text, x= c.center_screen_x,y=c.center_screen_y, color=colors.BLACK, font_name='Arial', font_size=50, centralized=False):
        message = TextObject(x, y, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)


def main(sitetemp):
    DraftGame(sitetemp = sitetemp).run()


#if __name__ == '__main__':
main(sitetemp = "BB10 12 Team")
