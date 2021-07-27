# this class simulates a wumpus world

class WumpusWorld: # WumpusWorld 클래스. 메서드로 neighbours, arrow_hits, print, sim이 있다.
  def __init__(self, blocks, pits, gold, wumpus, initial_location): #생성자 함수. wumpusWorld class 사용 시 매개변수로 block, pit, gold, wumpus, initial_location 순서대로 입력
    self.initial_location = initial_location    # copy the input (매개변수에 입력된 값 객체의 변수로 입력됨)
    self.wumpus = wumpus
    self.pits = pits
    self.gold = gold
    self.blocks = blocks
    self.player = self.initial_location # 플레이어는 초기 위치에 있다
    self.has_arrow = True # 초기 설정에는 화살이 있다.

    self.breeze = {}    # 바람이 부는 곳을 저장할 위치 / stores locations of breezy squares
    self.stench = {}    # 냄새 나는 곳을 저장할 위치 / stores location of smelly squares
    
    for p in self.pits: # pits의 상하좌우에 breeze=True 입력, initalise breezy squares
      for l in self.neighbours(p):
        self.breeze[l] = True
    for w in self.wumpus: # wumpus의 상하좌우에 stench=True 입력, intialise smelly squares
      for l in self.neighbours(w):
        self.stench[l] = True
      
      
  def neighbours(self, loc):    # 상하좌우 위치 함수. loc의 상하좌우를 리턴한다, returns neighbours of tuple loc = (x,y)
    return [(loc[0]+1,loc[1]), (loc[0]-1,loc[1]), (loc[0],loc[1]+1), (loc[0],loc[1]-1)]

  def arrow_hits(self, location, dx, dy): # location + dx, dy에 괴물이 있어서 화살이 적중하는지 확인하는 함수 / scans to see if the arrow hits
    while location not in self.blocks:   # 조준 위치가 벽이 아닌 이상 계속 수행
      location = (location[0]+dx, location[1]+dy)  # 조준 위치는 x축으로 +dx, y축으로 +dy 조준
      if location in self.wumpus: # 조준 위치에 괴물이 있으면 True를 반환(화살 적중)
        return True
    return False # 조준 위치에 괴물이 없다면 false 반환 (화살 빗나감)
  
  def print(self):    # 6*6보드 판에 block, pit, wumpus, gold, player를 나타태는 함수. print the board state (useful for debugging)
    print(self.player)
    xmin = min([x for x,y in self.blocks])
    xmax = max([x for x,y in self.blocks])
    ymin = min([y for x,y in self.blocks])
    ymax = max([y for x,y in self.blocks])
    for y in range(ymin, ymax+1):       # y 0~6 // 좌표 (1,1)~(4,4) 까지 B,W,P,G,Y 입력하고 arrow, breezy, stenchy 유무 출력
      for x in range(xmin, xmax+1):     # x 0~6
        
        if (x,ymax-y) in self.blocks:
          print('B',end='')
        elif (x,ymax-y) in self.wumpus:
          print('W',end='')
        elif (x,ymax-y) in self.pits:
          print('P',end='')
        elif (x,ymax-y) in self.gold:
          print('G',end='')
        elif self.player == (x, ymax - y):
          print('Y',end='')
        else:
          print(' ',end='')
      print("")
    b = self.player in self.breeze       # 플레이어 위치에 breezy유무에 따라 T/F 반환. is their square breezy?
    s = self.player in self.stench       # 플레이어 위치에 stench유무에 따라 T/F 반환. is it smelly?
    print("arrow: " + str(self.has_arrow)) # 화살 있나 없나 출력
    print("breezy: " + str(b))             # 플레이어 위치에 breezy 유무를 출력
    print("stenchy: " + str(s))            # 플레이어 위치에 stench 유무를 출력

    

  def sim(self, agent): #agent 클래스를 상속
    t = 0
    self.has_arrow = True   # 화살 장전 된 상태로 sim 함수 시작
    self.player = self.initial_location  # 플레이어는 초기 위치(1,1)에서 시작한다
    while t < 1000: # 1000번 수행
      t+=1 

      self.print()  # 한 번 수행 할 때 마다 board 판에 'B','W','P','G','Y' 출력

      b = self.player in self.breeze      # 플레이어 위치에 breezy유무에 따라 T/F 반환. is their square breezy?
      s = self.player in self.stench      # 플레이어 위치에 stench유무에 따라 T/F 반환. is it smelly?
      agent.give_senses(self.player, b, s)  # agent에게 b, s의 정보 전달. give the agent its senses
      action = agent.get_action()       # 상 하 좌 우 움직임의 action 입력
      print(action, end='\n\n')    # action 출력

      new_location = self.player    # new_location에 사용자의 위치 입력
      if action == 'MOVE_UP':             # 위에 언급된 action에 입력된 값에 따라 사용자의 위치 이동
        new_location = (self.player[0], self.player[1]+1)
      elif action == 'MOVE_DOWN':
        new_location = (self.player[0], self.player[1]-1)
      elif action == 'MOVE_LEFT':
        new_location = (self.player[0]-1,self.player[1])
      elif action == 'MOVE_RIGHT':
        new_location = (self.player[0]+1,self.player[1])
      elif not self.has_arrow and action[0:5] == 'SHOOT':  # 화살이 없거나 쐇다면 NO ARROW 리턴
        return 'NO ARROW'
      elif action == 'SHOOT_UP':    # 화살을 상,하,좌,우 중 한 곳에 쏴서 wumpus를 없앰
        if self.arrow_hits(self.player, 0, 1):
          self.wumpus = {}    
          agent.killed_wumpus()
      elif action == 'SHOOT_DOWN':
        if self.arrow_hits(self.player, 0, -1):
          self.wumpus = {}
          agent.killed_wumpus()
      elif action == 'SHOOT_LEFT':
        if self.arrow_hits(self.player, -1, 0):
          self.wumpus = {}
          agent.killed_wumpus()
      elif action == 'SHOOT_RIGHT':
        if self.arrow_hits(self.player, 1, 0):
          self.wumpus = {}
          agent.killed_wumpus()
      elif action == 'QUIT':  # agent.get_action의 counter가 1000이 되면 action=='Quit'가 된다,
        return 'QUIT'


      if action[0:5] == 'SHOOT':      # 화살을 쏘면
        self.has_arrow = False        # 보유한 화살이 False가 된다

      if new_location in self.pits:   # 새 위치(플레이어 위치)에 pit이 있으면 (물에 빠지면) FELL 리턴
        return 'FELL'
      if new_location in self.wumpus: # 새 위치에 wumpus가 있으면 EATEN 리턴
        return 'EATEN'
      if new_location in self.gold:   # 새 위치에 gold가 있으면 GOLD 리턴
        return 'GOLD'

      if new_location not in self.blocks: # 플레이어가 벽에 부딪히지 않는 이상
        self.player = new_location        # new_location 위치를 플레이어 위치에 대입한다.
                                          # 그럼 while 문을 반복하면서 player의 위치가 계속 갱신된다.