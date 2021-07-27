## 웜푸스 월드 환경 만드는 모듈
import wumpus, random
width = 5
width2 = 7
#비어있는 집합(set)인 block을 만든다
blocks = set()
pits_location=[]
wumpus_location=[]

#6x6맵 생성
for x in range(width+1):
    blocks.add((0, x))
    blocks.add((x, 0))
    blocks.add((width,x))
    blocks.add((x, width))
    blocks.add((width2, x))
    blocks.add((width2 + x, 0))
    blocks.add((width2 + width,x))
    blocks.add((width2 + x, width))

while(True):     #(1,1), (1,2), (2,1)을 제외한 위치에 금 생성
    x=random.randint(1,4)
    y=random.randint(1,4)
    if x==1 and y==1:
        continue
    elif x==1 and y==2:
        continue
    elif x==2 and y==1:
        continue
    gold={(x,y)}
    break


for i in range(1,width):   # 구덩이 생성
    for j in range(1,width):
        if random.randint(1,100) <= 15:
            if i==1 and j==1:
                continue
            elif i==1 and j==2:
               continue
            elif i==2 and j==1:
                continue
            elif i==x and j==y:
                continue
            pits_location.append((i,j))


for i in range(1,width):   # 웜푸스 생성
    for j in range(1,width):
        if random.randint(1,100) <= 15:
            if i==1 and j==1:
                continue
            elif i==1 and j==2:
               continue
            elif i==2 and j==1:
                continue
            elif i==x and j==y:
                continue
            wumpus_location.append((i,j))
            
            
initial_location = (1,1)    #에이전트 초기 위치 1,1

#6x6맵에 벽, 금, 웜푸스, 구덩이, 에이전트를 위치시킴
world1 = wumpus.WumpusWorld(blocks = blocks, gold = gold, wumpus = wumpus_location, pits = pits_location, initial_location = initial_location)

