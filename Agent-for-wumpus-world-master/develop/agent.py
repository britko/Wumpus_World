import random   # 랜덤 관련한 함수들을 모아놓은 모듈
import numpy as np  # 고성능의 수치계산을 위한 모듈(벡터 및 행렬 연산)
class Agent:
    def __init__(self):
        self.wump=[['A' for i in range(50)] for j in range(50)] # 괴물에 관한 
        self.kb=[['A' for i in range(50)] for j in range(50)]   # 구덩이에 관한 것
        self.moves=[]   # explore_world에 대한 행동을 추가하는 리스트
        self.move=1 # explore_world 함수를 시작하기 전에 있어 move를 1로 초기화하여 시작
        self.tb=False   # explore_world 함수를 시작하기 전에 있어 tb를 False로 초기화하여 시작
        self.move_stack=[]  # == move_p ??
        self.unsafe=[]  # 위험유무를 판단하기 위한 리스트로 취할 행동을 추가한다.
        self.border=False   # 방해물의 유무
        self.prev=[]    # 이전 행동을 기록하는 리스트
        self.f=False    # def get_action내 동작을 제어하기 위한 변수
        self.exp_t=False    # def get_action, explore_world내 동작을 제어하기 위한 변수
        self.shoot=""   # 상하좌우로 shoot을 지정하는 변수
        self.arrow_fired=3  # 화살을 쏘았느냐? 처음엔 False로 초기화
        self.visited=[] #  
        self.a=False    #
        self.right_border=False #
        self.left_border=False  #
        self.last_move='null'   #
        self.counter=0  #
        

    #
    def get_action(self):
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']   # 동작열
        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']    # 화살 동작열
        self.counter+=1 # 동작횟수 추가
        if self.counter>999:    # 동작횟수가 1000이상이면 종료
            return "QUIT"
        if self.shoot in extras and self.arrow_fired!=0:    # shoot이 화살 동작열 안에 있고 화살을 쏘지 않았으면
            if self.move_p==actions[0]: # move_p가 MOVE_UP이면 last_move는 MOVE_DOWN
                self.last_move=actions[1]
            if self.move_p==actions[1]: # move_p가 OVE_DOWN이면 last_move는 MOVE_UP
                self.last_move=actions[0]
            if self.move_p==actions[2]: # move_p가 MOVE_LEFT면 last_move는 MOVE_RIGHT
                self.last_move=actions[3]
            if self.move_p==actions[3]: # move_p가 MOVE_RIGHT이면 last_move는 MOVE_LEFT
                self.last_move=actions[2]
            
            self.arrow_fired-=1   # 화살 사용
            return self.shoot   # shoot을 리턴
            
        if self.f==False:   # f가 false일때
            if self.exp_t==True:    # exp_t가 true이면 
                #self.unsafe=[
                self.exp_t=False    # exp_t를 false로
                self.f=True # f를 true로
            else:   # exp_t가 false이면 
                return(self.explore_world())    #explore_world 실행결과를 리턴
        
        if self.f==True: # f가 true일면
            t=self.make_move()  # make_move 실행결과를 t에 넣고
            self.f=False    # f를 false로
            return t # t를 리턴

    def explore_world(self):  #move와 tb에 따라 moves에 action을 추가하고 action을 반환
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        if self.move==1 and self.tb==False: # move=1이고 tb=false이면
            self.tb=True
            self.moves.append(actions[0])   # moves 리스트에 MOVE_UP 추가
            self.move_p=actions[0]  #move_p를 MOVE_UP로 하고
            return actions[0]   # MOVE_UP을 리턴
        if self.move==1 and self.tb==True:  # move=1이고 tb=true일때
            self.tb=False   #tb를 false로
            self.move=2 #move를 2로 바꾸고
            if self.border==False:  #border가 false이면
                return actions[1] #DOWN
            else:   #border가 true이면 
                return actions[0]   #UP
        
        if self.move==2 and self.tb==False: #move=2이고 tb=false
            self.tb=True    #tb를 true로
            self.moves.append(actions[1])   #moves에 DOWN을 추가
            self.move_p=actions[1]  #move_p를 DOWN으로
            return actions[1] #DOWM 리턴
        if self.move==2 and self.tb==True: #move=2이고 tb=true
            self.tb=False
            self.move=3
            if self.border==False:
                return actions[0]
            else:
                return actions[1]
        
        if self.move==3 and self.tb==False:
            self.tb=True
            self.moves.append(actions[2])
            self.move_p=actions[2]
            return actions[2]
        if self.move==3 and self.tb==True:
            self.tb=False
            self.move=4
            if self.border==False:
                return actions[3]
            else:
                return actions[2]
        
        if self.move==4 and self.tb==False:
            self.tb=True
            self.moves.append(actions[3])
            self.move_p=actions[3]
            return actions[3]
        if self.move==4 and self.tb==True:
            self.tb=False
            self.move=1
            self.moves=[]
            self.exp_t=True
            if self.border==False:
                return actions[2]
            else:
                return actions[3]

    
    #
    def make_move(self): 
        self.f=False
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        temp=[]
        t=self.check_pit(self.prev) #1,2,3,4중 하나를 받음
        if isinstance(t,int):   #t가  int형인지 검사 -> T/F
            if actions[t] in self.unsafe:   #actions[t]가 unsafe에 있을때, 행동이 위험하면
                if len(self.unsafe)!=1: #unsafe의 길이가 1이 아니면, unsafe에 move_p가 있으면
                    for item in self.unsafe:    #unsafe 동작열동안 
                        if item==actions[t]:    #item은 actions[t]이면
                            self.unsafe.remove(item)    #unsafe에서 item을 삭제
        for item in actions:  # actions열이(item이)
            if item not in self.unsafe: # unsafe 동작열 안에 없으면
                temp.append(item)  # temp에 item(action)추가
        self.unsafe=[]
        self.a=True
        if temp:
            return (random.choice(temp)) # up, down, left, right 중 1개를 무작위로 반환
        
    #
    def give_senses(self, location, breeze, stench):
        actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        x=location[0]
        y=location[1]
        if stench==True:    #악취나면
            self.wump[x][y]='s' #현재 위치 wump에 s표시
        if breeze==True:    #미풍있으면
            self.kb[x][y]='b'   #현재 위치 kb에 b표시
            self.locate_pit(location) #b에따라 구덩이를 표시
        if breeze==False and stench==False: #미풍, 악취 없으면
            self.kb[x][y]='o'   #현재 위치 kb, wump에 안전 표시
            self.wump[x][y]='o'
        if self.prev==location: #이전위치와 현재위치가 같으면
            self.border=True    #방해물이 있다
        else:   #같지 않으면
            self.prev=location  #이전위치에 현재 위치 대입
            self.border=False   #방해물이 없다
        if (breeze==True):  #미풍있으면
            self.unsafe.append(self.move_p) #unsafe에 move_p를 추가
        if stench==True:    #악취있고
            if self.arrow_fired!=0: #화살 안쐈으면
                self.unsafe.append(self.move_p) #unsafe에 move_p추가
        c=self.killed_wumpus()  #killde_wumpus 리턴값을 c에 저장
        if c in extras: #c가 extras에 있으면
            self.shoot=c    #shoot에 c를 저장 (상,하,좌,우로 shoot)
        #input()
        #print (np.matrix(self.kb[-1::-1]))

        
    #s(악취)에따라 추론후 웜푸스를 죽이는 함수
    def killed_wumpus(self):
        c=(0,0)
        v=(0,0)
        x=0
        y=0
        l=[]
        l=self.prev #prev가 뭔지 모르겠다... || prev = 이전 위치??
        for i,lst in enumerate(self.wump):  #i:인덱스, lst:wump 해당 인덱스의 값
            for j,k in enumerate(lst):  #j:인덱스, k:lst 해당 인덱스의 값
                if k == "s":    #k값이 s(악취)이면
                     c=(i, j)   #c에 i,j값 저장(x,y)좌표
        
        if c:
            x,y=c   # x,y에 i,j의 값 저장
        
            if self.wump[x+2][y]=='s':  #오른쪽 두번째칸 s면 오른쪽 칸에 w표시
                self.wump[x+1][y]='w'
            if self.wump[x-2][y]=='s':  #왼쪽 두번째칸 s면 왼쪽 칸에 w표시
                self.wump[x-1][y]='w'
            if self.wump[x+1][y+1]=='s':    #우상향 대각이 s면 오른쪽 칸에 w표시
                self.wump[x+1][y]='w'
            if self.wump[x+1][y-1]=='s':    #우하향 대각이 s면 오른쪽 칸에 w표시
                self.wump[x+1][y]='w'
            if self.wump[x-1][y+1]=='s':    #좌상향 대각이 s면 위쪽 칸에 w표시
                self.wump[x][y+1]='w'
            if self.wump[x-1][y-1]=='s':    #좌하향 대각이 s면 아래쪽 칸에 w표시
                self.wump[x][y-1]='w'

        extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
        for i,lst in enumerate(self.wump):  #wump의 x좌표
            for j,k in enumerate(lst):  #wump의 y좌표
                if k == "w":    #x,y좌표가 wumpus이면
                     v=(i, j)   #v에 좌표 저장 (wumpus)
                     
        if l[0]==v[0]:  # 악취나는 곳과 괴물이 있는 곳의 x좌표가 같고
            if l[1]>v[1]:   # 악취나는 곳의 y축 위치가 괴물의 위치보다 높다면
                return (extras[1]) # 아래 방햐으로 shoot을 한다
            else:
                return (extras[0]) # 악취나는 곳의 위치가 괴물보다 아래라면 위쪽 방향으로 shoot을 한다
        if l[1]==v[1]:  # 악취나는 곳과 괴물이 있는 곳의 x좌표가 같고
            if l[0]>v[0]:   # 악취나는 곳의 x축 위치가 괴물보다 우측이라면
                return (extras[2]) # 우측으로 shoot을 한다
            else:
                return (extras[3]) # 악취나는 곳의 x축 위치가 괴물보다 좌측이라면 좌측으로 shoot을 한다

    
    #b에따라 추론해서 구덩이를 표시하는 함수
    def locate_pit(self,location):
        
        
        x=location[0]   #현재위치의 x좌표
        y=location[1]   #현재위치의 y좌표
        if self.kb[x+2][y]=='b' and self.kb[x+1][y+1]=='b': #오른쪽으로 2번째와 우상향 대각으로 'b'가 있을때
            self.kb[x+1][y]='p' #오른쪽 칸에 구덩이 표시
        if self.kb[x+2][y]=='b' and self.kb[x+1][y-1]=='b': #오른쪽으로 2번째와 우하향 대각으로 'b'가 있을때
            self.kb[x+1][y]='p'
        if self.kb[x-2][y]=='b' and self.kb[x-1][y+1]=='b': #왼쪽 2번째와 좌상향 대각으로 'b'가 있을때
            self.kb[x-1][y]='p' #왼쪽 칸에 구덩이 표시
        if self.kb[x-2][y]=='b' and self.kb[x-1][y-1]=='b': #왼쪽 2번째와 좌하향 대각으로 'b'가 있을때
            self.kb[x+1][y]='p' #오른쪽 칸에 구덩이 표시
        if self.kb[x][y+2]=='b' and self.kb[x+1][y+1]=='b': #위쪽 2번째와 우상향 대각으로 'b'가 있을때
            self.kb[x][y+1]='p' #위쪽 칸에 구덩이 표시
        if self.kb[x][y+2]=='b' and self.kb[x-1][y+1]=='b': #위쪽 2번째와 좌상향 대각으로 'b'가 있을때
            self.kb[x][y+1]='p'
        if self.kb[x][y-2]=='b' and self.kb[x+1][y-1]=='b': #아래쪽 2번째와 우하향 대각으로 'b'가 있을때
            self.kb[x][y-1]='p' #아래칸에 구덩이 표시
        if self.kb[x][y-2]=='b' and self.kb[x-1][y-1]=='b': #아래쪽 2번째와 좌하향 대각으로 'b'가 있을때
            self.kb[x][y-1]='p'
        
    
    def check_pit(self,l):  #구덩이 조사 prev를 받음
        x=l[0]  #prev[0]
        y=l[1]  #prev[1]
        if self.kb[x+1][y]=='p':    #오른쪽 p이면 3 리턴
            return 3
        if self.kb[x-1][y]=='p':    #왼쪽 p이면 2 리턴
            return 2
        if self.kb[x][y+1]=='p':    #위쪽 p이면 0 리턴
            return 0
        if self.kb[x][y-1]=='p':    #아래쪽 p이면 1 리턴
            return 1
