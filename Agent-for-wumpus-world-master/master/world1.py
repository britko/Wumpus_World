## 웜푸스 월드 환경 만드는 모듈
import wumpus
import random
width = 5

#비어있는 집합(set)인 block을 만든다
blocks = set()

#6x6맵 생성
for x in range(width+1):
    blocks.add((0, x))
    blocks.add((x, 0))
    blocks.add((width,x))
    blocks.add((x, width))


t=True
while(t):     #(1,1), (1,2), (2,1)을 제외한 위치에 금 생성
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

pits=[]
wumpus_location = []

for i in range(width+1):   # 구덩이 생성
    for j in range(width+1):
        z=random.randint(1,100)
        a=random.randint(1,4)
        b=random.randint(1,4)
        if z<=15:
            if a==1 and b==1:
                continue
            elif a==1 and b==2:
               continue
            elif a==2 and b==1:
                continue
            elif a==x and b==y:
                continue
            pits.append((a,b))

for i in range(width+1):  # 괴물 생성
    for j in range(width+1):
        z=random.randint(1,100)
        a=random.randint(1,4)
        b=random.randint(1,4)
        if z<=15:
            if a==1 and b==1:
                continue
            elif a==1 and b==2:
               continue
            elif a==2 and b==1:
                continue
            elif a==x and b==y:
                continue
            wumpus_location.append((a,b))

initial_location = (1,1)    #에이전트 초기 위치 1,1

#6x6맵에 벽, 금, 웜푸스, 구덩이, 에이전트를 위치시킴
world1 = wumpus.WumpusWorld(blocks = blocks, gold = gold, wumpus = wumpus_location, pits = pits, initial_location = initial_location)

