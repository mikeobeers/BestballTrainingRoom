import pygame
import config as c
from pygame.rect import Rect
import sys
from collections import defaultdict
import numpy as np
import colors
import string

class GameObject:
    def __init__(self, x, y, w, h):
        self.bounds = Rect(x, y, w, h)

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    def draw(self, surface):
        pass


class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass

class PickObject:
    def __init__(self, x, y, text, color, font_name, font_size,center_x=True,center_y=True):
        self.pos = (x, y)
        self.text = text
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text)
        

    def draw(self, surface):
        text_surface, self.bounds = self.get_surface(self.text)
        pos = self.pos
        if self.center_x:
            pos = (pos[0] - self.bounds.width // 2, pos[1])
        if self.center_y:
            pos = (pos[0], pos[1] - self.bounds.height // 2)
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass



class Brick(GameObject):
    def __init__(self, x, y, w, h, color):
        GameObject.__init__(self, x, y, w, h)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)
    
    def update(self):
        pass


class Button(GameObject):
    def __init__(self, x, y, w, h, text, on_click=lambda x: None, padding=0,backcolor=c.button_normal_back_color,text_color=c.button_text_color,font_size = c.font_size):
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click
        self.backcolor = backcolor
        self.text = TextObject(x + padding, y + padding, lambda: text, text_color, c.font_name, font_size)

    def update(self):
        pass
    @property
    def back_color(self):
        return dict(normal=self.backcolor,
                    hover=colors.GREENYELLOW,
                    pressed=colors.GREEN)[self.state]

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.bounds)
        self.text.draw(surface)

    def handle_mouse_event(self, type1, pos):
        if type1 == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type1 == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type1 == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'
            
class Game:
    def __init__(self, caption, width, height, back_image_filename, frame_rate, sitetemp = "BB10 12 Team"):
        self.background_image = pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        self.template = sitetemp
        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            #self.clock.tick(self.frame_rate)
            
            
def scorecalcDL(roster,playerscoring,playerscoringPD,timeframe,flexposlist=['RB','WR','TE'],sflexposlist=['QB','RB','WR','TE'],QBcount=1,WRcount=3,RBcount=2,TEcount=1,DEFcount=1,PKcount=0,FLEXcount=1,SFLEXcount=0,scoring=1):
    thisroster = [lis + " " + str(timeframe) for lis in roster]
    poscol = 3
    weekcol = 6
    ptscol = 7
    if scoring == 1:
        ptscol = 10
    if scoring == 0:
        ptscol = 11
    playercol = 0
    thesecodes = []
    theseplayers = []
    theseyears = []
    thesepos = []
    theseplayeryears = []
    theseposadps = []
    scores_pd1 = playerscoringPD
    scores_pd = scores_pd1[scores_pd1.PlayerFrame.isin(thisroster)]
    for code in thisroster:
        thisplayer = np.unique(scores_pd['Player'][scores_pd.PlayerFrame.isin([code])])
        thisyear = np.unique(scores_pd['Year'][scores_pd.PlayerFrame.isin([code])])
        thiscode = np.unique(scores_pd['PosADPcode'][scores_pd.PlayerFrame.isin([code])])
        thispos = np.unique(scores_pd['Pos'][scores_pd.PlayerFrame.isin([code])])
        thisposadp = np.unique(scores_pd['PosADP'][scores_pd.PlayerFrame.isin([code])])
        thisplayeryear = str(thisyear)[1:-1] + " " + thisplayer
        thesepos.insert(len(thesepos),thispos)
        thesecodes.insert(len(thesecodes),thiscode)
        theseplayers.insert(len(theseplayers),thisplayer)
        theseyears.insert(len(theseyears),thisyear)
        theseplayeryears.insert(len(theseplayeryears),thisplayeryear)
        theseposadps.insert(len(theseposadps),thisposadp)
    scores = np.array([b for b in playerscoring.tolist() if any(a in b for a in thisroster)])
    thisweek = 0
    weektotals = []
    while thisweek < 16:
        QBplayers = np.array(["TBD"])
        RBplayers = np.array(["TBD"])
        WRplayers = np.array(["TBD"])
        TEplayers = np.array(["TBD"])
        DEFplayers = np.array(["TBD"])
        PKplayers = np.array(["TBD"])
        QBscores = 0
        RBscores = 0
        WRscores = 0
        TEscores = 0
        DEFscores = 0
        PKscores = 0
        FLEXscores = 0
        S_FLEXscores = 0
        
        thisweek += 1

        weekfinder = np.array([int(lis[weekcol]) for lis in scores])
        weektester = [weekfinder == thisweek]
        weekscores1 = scores[tuple(weektester)]
        if len(weekscores1) >0:
            pts = np.array(weekscores1[:,ptscol].astype(float))
            sortvals = np.argsort(-pts)
            weekscores = weekscores1[sortvals]

            QBrostered = len([b for b in weekscores.tolist() if any(a in b for a in ['QB'])])
            RBrostered = len([b for b in weekscores.tolist() if any(a in b for a in ['RB'])])
            WRrostered = len([b for b in weekscores.tolist() if any(a in b for a in ['WR'])])
            TErostered = len([b for b in weekscores.tolist() if any(a in b for a in ['TE'])])
            DEFrostered = len([b for b in weekscores.tolist() if any(a in b for a in ['Def'])])
            PKrostered = len([b for b in weekscores.tolist() if any(a in b for a in ['PK'])])
  
        if QBrostered > 0 and QBcount > 0:
            used = int(min([QBrostered,QBcount]))
            QBs = weekscores[weekscores[:,poscol]=='QB']
            QBplayers = QBs[:used,playercol]
            QBscores = sum(QBs[:used,ptscol].astype(float))
  
        if RBrostered > 0 and RBcount > 0:
            used = int(min([RBrostered,RBcount]))
            RBs = weekscores[weekscores[:,poscol]=='RB']
            RBplayers = RBs[:used,playercol]
            RBscores = sum(RBs[:used,ptscol].astype(float))
        if WRrostered > 0 and WRcount > 0:
            used = int(min([WRrostered,WRcount]))
            WRs = weekscores[weekscores[:,poscol]=='WR']
            WRplayers = WRs[:used,playercol]
            WRscores = sum(WRs[:used,ptscol].astype(float))
        if TErostered > 0 and TEcount > 0:
            used = int(min([TErostered,TEcount]))
            TEs = weekscores[weekscores[:,poscol]=='TE']
            TEplayers = TEs[:used,playercol]
            TEscores = sum(TEs[:used,ptscol].astype(float))
        if DEFrostered > 0 and DEFcount > 0:
            used = int(min([DEFrostered,DEFcount]))
            DEFs = weekscores[weekscores[:,poscol]=='Def']
            DEFplayers = DEFs[:used,playercol]
            DEFscores = sum(DEFs[:used,ptscol].astype(float))
        if PKrostered > 0 and PKcount > 0:
            used = int(min([PKrostered,PKcount]))
            PKs = weekscores[weekscores[:,poscol]=='PK']
            PKplayers = PKs[:used,playercol]
            PKscores = sum(PKs[:used,ptscol].astype(float))        
          
        starters = QBplayers.tolist() + RBplayers.tolist() + WRplayers.tolist() + TEplayers.tolist() + DEFplayers.tolist() + PKplayers.tolist()
  
        if SFLEXcount > 0:
            S_FLEXs = np.array([b for b in weekscores.tolist() if all(a not in b for a in starters)])
            S_FLEXs = np.array([b for b in S_FLEXs.tolist() if any(a in b for a in sflexposlist)])
            S_FLEXrostered = len(S_FLEXs)
            if S_FLEXrostered > 0:
                used = int(min([SFLEXcount,S_FLEXrostered]))
                S_FLEXplayers = S_FLEXs[:used,playercol]
                S_FLEXscores = sum(S_FLEXs[:used,ptscol].astype(float)) 
                starters = starters + S_FLEXplayers.tolist()
                  
        if FLEXcount > 0:
            FLEXs = np.array([b for b in weekscores.tolist() if all(a not in b for a in starters)])
            FLEXs = np.array([b for b in FLEXs.tolist() if any(a in b for a in flexposlist)])
            FLEXrostered = len(FLEXs)
            if FLEXrostered > 0:
                used = int(min([FLEXcount,FLEXrostered]))
                FLEXplayers = FLEXs[:used,playercol]
                FLEXscores = sum(FLEXs[:used,ptscol].astype(float))
                starters = starters + FLEXplayers.tolist()
                          
        thisweekscore = QBscores + RBscores + WRscores + TEscores + DEFscores + PKscores + S_FLEXscores + FLEXscores
        weektotals.insert(len(weektotals),round(thisweekscore,2))


    ph = {'Pos':np.array(thesepos).reshape(1,-1)[0],
          'PosADP':np.array(theseposadps).reshape(1,-1)[0],
          'PosADPcode':np.array(thesecodes).reshape(1,-1)[0],
          'Player':np.array(theseplayers).reshape(1,-1)[0],
          'Year':np.array(theseyears).reshape(1,-1)[0],
          'PlayerYear':np.array(theseplayeryears).reshape(1,-1)[0]}
    return round(sum(weektotals),2), ph, weektotals
