import time
import hashlib
import random,string
import pygame
import statistics
class User:
    def __init__(self):
        self.private = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
        self.bal = random.randint(10,50)
        self.cot =0
class Transaction:
    def __init__(self,to,fro,amt,ti,fi):
        self.to,self.fro,self.amt = to,fro,amt
        self.ti,self.fi=ti,fi#TO Index,

class Nodes:
    def castvote(self):
        return(random.randint(0,2))     
        
class Block:
    def __init__(self,index,ph,history):
        
        self.index = index
        self.p_hash = ph
        self.ts = time.time()
        self.nonce = 0
        self.transactions = history
class Miner:
    def __init__(self,name):
        self.name = name
        self.vote = 0
        self.step = 0
    def mining (self,block):
        block.nonce+= self.step
        temp = f'{block.index}{block.p_hash}{block.ts}{block.nonce}{block.transactions}'
        temp = hashlib.sha256(temp.encode()).hexdigest()
        temp = int(temp,16)
        sm=0;
        while temp>0:
            sm+=temp%10
            temp/=10
        return(int(sm))
class Controller:
    def __init__(self):
        self.mining='';
        self.un = 30#User Num
        self.tr = 1#Transaction Rate
        self.nd = 20#Netwrok difficulty on the scale of 1000
        self.bs = 15#Block Size
        self.mp=[]#MemePool
        self.tt=[]#TimeTaken
        self.users=[]#User Details
        self.chain = []#Block Chain
        self.count=0
        self.ui=[]#User Interface
        self.ui.append(pygame.Rect(50,50,180,5))#User
        self.ui.append(pygame.Rect(300,50,180,5))#TransactionRate
        self.ui.append(pygame.Rect(550,50,180,5))#Difficulty
        self.circle=[]
        self. name = ""
        self.circle.append([70,52]);self.circle.append([305,52]);self.circle.append([560,52]);
        self.vtime=[0];self.mtime=[0];
        self.nodes=[]
        pygame.init()
        for x in range(0,5):
            self.users.append(User())
        for x in range(0,20):
            self.maketrans()
            self.nodes.append(Nodes())
        r = Transaction(self.users[random.randint(0,1)],self.users[random.randint(2,4)],0.005,0,0)
        
        temp = Block(0,0,[r])
        self.chain.append(temp)#Adding the Genesis Block
        self.miners = []
        self.miners.append(Miner("Alpha"));self.miners.append(Miner("Beta"));self.miners.append(Miner("Gamma"));
    def maketrans(self):
        tempr = len(self.mp)
        for x in range(0,self.un*self.tr):
            self.count +=1
            length = len(self.users)
            source = random.randint(0,length-1)
            
            dest = source+random.randint(0,length-1)
            if(dest >= length):
                dest = dest%length
            
            amount = random.random()
            self.users[source].bal-=amount;self.users[dest].bal+=amount;
            self.users[source].cot+=1;self.users[dest].cot+=1;
            temp = Transaction(self.users[source].private,self.users[dest].private,amount,dest,source)
            self.mp.append(temp)
        #rint(len(self.mp)-tempr)
    def validator(self):
        for x in range(0,3):
            self.miners[x].step = random.randint(1,9)
            
        temp=[];count =0;
        for x in range(0,self.bs):
            temp.append(self.mp[0])
            self.mp.pop(0)
        for x in temp:
            for y in self.chain:
                for z in y.transactions:
                    if(x.to==self.users[z.ti].private or x.to==self.users[z.fi].private or x.fro == self.users[z.ti].private or x.fro == self.users[z.fi].private):
                        count+=1;
        #print("It is doen")
        block = self.chain[-1]
        temp1 = f'{block.index}{block.p_hash}{block.ts}{block.nonce}{block.transactions}'
        temp1 = hashlib.sha256(temp1.encode()).hexdigest()
        
        temp2 = Block(len(self.chain),temp1,temp)
        return(temp2)
        

    def minera(self,block,given):
        
        if(given+5>len(self.nodes)):
            self.voting = False
            return(block)
        for x in range(given,given+5):
            self.miners[self.nodes[given].castvote()].vote+=1;
        
        return(block)
            
   
    def changeusernum(self,current):
        if(self.un>current):
            for x in range(0,self.un-current):
                self.users.pop(random.randint(0,len(self.users)-1))
            self.un =current
            return
        else:
            for x in range(0,current-self.un):
                temp = User()
                self.users.append(temp)
            self.un =current
    def changenodesnum(self,current):
        if(self.un>current):
            for x in range(0,self.un-current):
                self.nodes.pop()
            self.nd =current
            return
        else:
            for x in range(0,current-self.nd):
                
                self.nodes.append(Nodes())
            self.nd =current
    def lable(self,screen):
        font_title = pygame.font.Font(None,30)
        ann = font_title.render("No. Of Users", True, (255,255,255))
        annr = ann.get_rect(center = (120,25))
        screen.blit(ann,annr)
        ann = font_title.render("Transaction Rate", True, (255,255,255))
        annr = ann.get_rect(center = (380,25))
        screen.blit(ann,annr)
        ann = font_title.render("# of Nodes:", True, (255,255,255))
        annr = ann.get_rect(center = (640,25))
        screen.blit(ann,annr)
        ann = font_title.render(str(self.un), True, (255,255,255))
        annr = ann.get_rect(center = (120,80))
        screen.blit(ann,annr)
        
        ann = font_title.render(str(self.tr), True, (255,255,255))
        annr = ann.get_rect(center = (380,80))
        screen.blit(ann,annr)
        
        ann = font_title.render(str(self.nd), True, (255,255,255))
        annr = ann.get_rect(center = (640,80))
        screen.blit(ann,annr)
        
        
        
        ann = font_title.render("Total Transactions:"+str(self.count), True, (255,255,255))
        annr = ann.get_rect(center = (110,120))
        screen.blit(ann,annr)

        ann = font_title.render("# of Blocks:"+str(len(self.chain)), True, (255,255,255))
        annr = ann.get_rect(center = (320,120))
        screen.blit(ann,annr)
        
       
        
        ann = font_title.render("MemPool Transactions : "+str(len(self.mp)), True, (255,255,255))
        annr = ann.get_rect(center = (550,120))
        screen.blit(ann,annr)

        vt = statistics.mean(self.vtime)
        mt = statistics.mean(self.mtime)
        ti = vt+mt
        ti=str(format(ti,".5f"))
        ann = font_title.render("Time Taken : "+ti, True, (255,255,255))
        annr = ann.get_rect(center = (120,170))
        screen.blit(ann,annr)
        ti = str(format(vt,".5f"))
        ann = font_title.render("Validating : "+ti, True, (255,255,255))
        annr = ann.get_rect(center = (350,170))
        screen.blit(ann,annr)
        ti = str(format(mt,".5f"))
        
        ann = font_title.render("Voting : "+ti, True, (255,255,255))
        annr = ann.get_rect(center = (550,170))
        screen.blit(ann,annr)

        ann = font_title.render("Last Blocked Mined By: "+self.name, True, (255,255,255))
        annr = ann.get_rect(center = (250,220))
        screen.blit(ann,annr)
        
    def mod(self,count,screen):
        if(count==0):
            temp = (self.circle[0][0]/180)*120
            temp =int(temp)-28
            self.changeusernum(temp)
        if(count==1):
            temp = (self.circle[1][0]/180)*20
            temp =int(temp)
            self.tr=temp-30
        if(count==2):
            temp = (self.circle[2][0]/180)*20
            temp =int(temp)

            temp-= 40+temp%5
            self.changenodesnum(temp)

            

    def blockprinter(self,screen):
        x,y=0,260
        cout=0
        
        for x1 in self.chain:
            cout+=1;
            if(cout%53==0):
                x=0;y+=20
            pygame.draw.rect(screen,[15,100,255],[x,y,10,10])
            x+=15
    
    def tableprinter(self,screen,num):
        
        if(num=='' or num=="1"):
            return
        num = int(num)
        pygame.draw.rect(screen,[25,255,25],[820,220,410,400],2,3)
        pygame.draw.rect(screen,[25,255,255],[820,265,410,30],2,3)
        pygame.draw.rect(screen,[25,255,255],[820,295,410,30],2,3)
        pygame.draw.rect(screen,[25,255,255],[820,325,410,30],2,3)
        pygame.draw.rect(screen,[201,205,64],[825,360,400,250],0,3)
        
        num=int(num)
        num-=1
        font_title = pygame.font.Font(None,30)
        ann = font_title.render("Block Details:"+str(num), True, (255,255,255))
        annr = ann.get_rect(center = (1010,240))
        screen.blit(ann,annr)
        
        ann = font_title.render("Version:0.pow.2v", True, (255,255,255))
        annr = ann.get_rect(center = (930,280))
        screen.blit(ann,annr)
        bts = self.chain[num]
        ann = font_title.render("Nonce:"+str(bts.nonce), True, (255,255,255))
        annr = ann.get_rect(center = (1130,280))
        screen.blit(ann,annr)
        string =str(bts.ts)
        ann = font_title.render("TimeStamp:"+string, True, (255,255,255))
        annr = ann.get_rect(center = (1020,310))
        screen.blit(ann,annr)
        

        string =str(self.chain[num].p_hash)
        ann = font_title.render("Previous Hash:"+string[0:20], True, (255,255,255))
        annr = ann.get_rect(center = (1030,340))
        screen.blit(ann,annr)
        
        bts = self.chain[num]
        li = bts.transactions
        y=370
        font_title = pygame.font.Font(None,20)
        for x in range(0,12):
            to,fro,amt = li[x].to,li[x].fro,li[x].amt
            ann = font_title.render("To:"+str(to)+"   "+"From:"+str(fro)+"   "+"Amount:"+str(amt)[0:8], True, (255,255,255))
            annr = ann.get_rect(center = (1030,y))
            y+=20
            screen.blit(ann,annr)

    def mineprint(self,screen):
        current =0
        mi = self.miners[0].vote
        for x in range(0,3):
            if(mi<c.miners[x].vote):
                current = x;
                mi = self.miners[x].vote
        pygame.draw.circle(screen,[255,255,255],[1225,((current+1)*50)-10],10)
        pygame.draw.rect(screen,[20,255,25],[850,10,350,150],3,2)
        pygame.draw.line(screen,[255,255,5],[850,50],[1200,50],2)
        pygame.draw.line(screen,[255,255,5],[850,100],[1200,100],2)
        font_title = pygame.font.Font(None,35)
        
        ann = font_title.render("Alpha:", True, (255,255,255))
        annr = ann.get_rect(center = (910,25))
        screen.blit(ann,annr)
        ann = font_title.render("Beta:", True, (255,255,255))
        annr = ann.get_rect(center = (900,75))
        screen.blit(ann,annr)
        ann = font_title.render("Gamma:", True, (255,255,255))
        annr = ann.get_rect(center = (920,125))
        screen.blit(ann,annr)

        
        ann = font_title.render(str(self.miners[0].vote), True, (255,255,255))
        annr = ann.get_rect(center = (1000,25))
        screen.blit(ann,annr)
        ann = font_title.render(str(self.miners[1].vote), True, (255,255,255))
        annr = ann.get_rect(center = (1000,75))
        screen.blit(ann,annr)
        ann = font_title.render(str(self.miners[2].vote), True, (255,255,255))
        annr = ann.get_rect(center = (1000,125))
        screen.blit(ann,annr)
   
if(__name__=='__main__'): 
    
    c = Controller()
    a= time.time()
    block = 1;

    
    screen = pygame.display.set_mode((1300,650))
    pygame.display.set_caption("BlockChainSim-2021 0.pow.2v")
    clock = pygame.time.Clock()
    pygame.font.init()
    a = time.time()
    base_font = pygame.font.Font(None, 32)
    user_text = ''

    input_rect = pygame.Rect(450, 200, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False
    a= time.time()
    block = c.validator()
    c.mining = True
    troy = time.time()#Validating time
    troy1 = time.time()
    current =0
    lec=lec1=len(c.chain)
    c.voting=True;winner=""
    while True:
        screen.fill((0,0,0));clock.tick(35);
        pygame.draw.rect(screen,[255,255,255],[0,250,800,500])
    
        for x in range(0,len(c.ui)):
            pygame.draw.rect(screen,[205,125,250],c.ui[x])
            pygame.draw.circle(screen,[25,180,60],c.circle[x],10)
        c.lable(screen)
        for x in pygame.event.get():
            if x.type == pygame.QUIT:
                pygame.quit()
            if(x.type == pygame.MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos();count =0
                    for y in c.ui:
                        if(y.collidepoint(pos)):
                            c.circle[count][0]=pos[0]
                            c.mod(count,screen)
                        count+=1;
            if x.type == pygame.KEYDOWN:
    
                if x.key == pygame.K_r:
                    
                    c.chain=[]
                    c.count=0
                    break;
                if x.key == pygame.K_q:
                    pygame.quit()
                    break;
                if x.key == pygame.K_BACKSPACE:
  
                    user_text = user_text[:-1]
                else:
                    user_text += x.unicode
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)
  
        text_surface = base_font.render(user_text, True, (255, 255, 255))
      
    # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
      
    # set width of textfield so that text cannot get
    # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)
        b = time.time()
        s = float(b-a)
        c.blockprinter(screen)
        #c.tableprinter(user_text)
        if(s>1):
            c.maketrans()
            a=time.time()
        #If mining is done then calle dvalidator\
        if(lec-lec1!= 0 and len(c.mp)>15):
            lec1 = lec
            c.voting= True
            troy = time.time()
        block = c.minera(block,current)
        current+=5
        c.tableprinter(screen,user_text)
        if(c.voting==False):
            c.mtime.append(float(time.time()-troy))
            if(len(c.mp)>15):
                troy1= time.time()
                block = c.validator()
                c.vtime.append(float(time.time()-troy1))
            mi =0;current=0;
            mi = c.miners[0].vote
            current =0
            c.miners[0].vote = 0
            winner = c.miners[0].name
            for x in range(1,3):
                if(mi<c.miners[x].vote):
                    mi = c.miners[x].vote
                    winner =c.miners[x].name
                c.miners[x].vote = 0
            block.nonce =random.randint(10,255) 
            if(len(c.mp)>15):
                c.chain.append(block)
            lec = len(c.chain)
        c.name=winner 
        c.mineprint(screen)
        pygame.display.update()
    


    