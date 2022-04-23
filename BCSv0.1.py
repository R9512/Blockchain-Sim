    #Need to Add UI and come up with a plan to implement the transaction rates
import time,datetime
import hashlib
import random,string
import pygame
import multiprocessing
import statistics
class User:
    def __init__(self):
        self.private = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
        self.bal = random.randint(10,50)
class Rodda:
   
        
    
    def __init__(self,index,history):
        self.index = index
        self.p_hash = 0
        self.ts = time.time()
        self.nonce = 0
        self.transactions = history
        
class Transaction:
    def __init__(self,to,fro,amt):
        self.to,self.fro,self.amt = to,fro,amt
        
class Miner:
    def __init__(self):
        pass
    def mining(self,block,dl):
        a= time.time()
        while(True):
            block.nonce+=1;
            temp = "{}{}{}{}".format(block.index,block.p_hash,block.nonce,block.transactions)
            
            string =str(hashlib.sha256(temp.encode()).hexdigest())
            
            val = sum(bytearray(string.encode()))
            
            if(val>1000):
                val%=1000
            if(val > dl):
                
                b = time.time()
                return(block,float(b-a))
                
            
        
class Controller:
    def __init__(self):
        self.user_num = 15
        self.tr = 1;#Transaction Rate
        self.trans = []
        self.dl=22
        self.bt =0
        self.users = [];self.blocks=[]
        self.size=105
        self.count =0;self.time=[0.0]
        self.rs=False;self.s=False
        self.miner = Miner()
        for x in range(0,5):
            temp = User();
            self.users.append(temp)
        self.ui=[]
        self.ui.append(pygame.Rect(50,50,180,5))#User
        self.ui.append(pygame.Rect(300,50,180,5))#TransactionRate
        self.ui.append(pygame.Rect(550,50,180,5))#Size
        self.ui.append(pygame.Rect(180,120,180,5))#Difficulty
        self.ui.append(pygame.Rect(1200,50,20,20))#Shardings
        self.circle=[]
        self.circle.append([70,52]);self.circle.append([305,52]);self.circle.append([560,52]);self.circle.append([185,122]);self.circle.append([456,1560])
            
    def resize(self):
        
        i=0;
        self.blocks=[]
        for x in range(0,self.count//self.size):
            i=x*self.size;
            j = i+self.size 
            self.createblock(i,j)
            
        self.rs=False
    def changeusernum(self,current):
        if(self.user_num>current):
            for x in range(0,self.user_num-current):
                self.users.pop(random.randint(0,len(self.users)-1))
            self.user_num =current
            return
        else:
            for x in range(0,current-self.user_num):
                temp = User()
                self.users.append(temp)
            self.user_num =current
            
    def maketrans(self):
        for x in range(0,self.tr*self.user_num):
            self.count +=1
            length = len(self.users)
            source = random.randint(0,length-1)
            dest = source+random.randint(0,length-1)
            if(dest >= length):
                dest = dest%length
            
            amount = random.random()
            self.users[source].bal-=amount;self.users[dest].bal+=amount;
            temp = Transaction(self.users[source].private,self.users[dest].private,amount)
            self.trans.append(temp)
            
    def createblock(self,i1=0,j1=0):
        
        i =self.count//self.size;i-=1
        self.bt+=self.size;
        test =Rodda(i,self.trans[i*self.size:(i+1)*self.size])
        if(i1!=0 and j1!=0):
            sega = self.trans[i1:j1]
            test=Rodda(i,self.trans[i*self.size:(i+1)*self.size])
        
        temp,time = self.miner.mining(test,self.dl)
        if(self.s):
            time/=3
        self.time.append(time)
        
        self.blocks.append(temp)
        
    def lable(self,screen):
        font_title = pygame.font.Font(None,30)
        ann = font_title.render("No. Of Users", True, (255,255,255))
        annr = ann.get_rect(center = (120,25))
        screen.blit(ann,annr)
        ann = font_title.render("Transaction Rate", True, (255,255,255))
        annr = ann.get_rect(center = (380,25))
        screen.blit(ann,annr)
        ann = font_title.render("Block Size", True, (255,255,255))
        annr = ann.get_rect(center = (640,25))
        screen.blit(ann,annr)
        ann = font_title.render("Difficulty:", True, (255,255,255))
        annr = ann.get_rect(center = (100,120))
        screen.blit(ann,annr)
        ann = font_title.render(str(self.user_num), True, (255,255,255))
        annr = ann.get_rect(center = (120,80))
        screen.blit(ann,annr)
        
        ann = font_title.render(str(self.tr), True, (255,255,255))
        annr = ann.get_rect(center = (380,80))
        screen.blit(ann,annr)
        
        ann = font_title.render(str(self.size), True, (255,255,255))
        annr = ann.get_rect(center = (640,80))
        screen.blit(ann,annr)
        
        ann = font_title.render(str(self.dl), True, (255,255,255))
        annr = ann.get_rect(center = (400,120))
        screen.blit(ann,annr)
        
        ann = font_title.render("Total Transactions:"+str(self.count), True, (255,255,255))
        annr = ann.get_rect(center = (870,30))
        screen.blit(ann,annr)

        ann = font_title.render("# of Blocks:"+str(len(self.blocks)), True, (255,255,255))
        annr = ann.get_rect(center = (1150,30))
        screen.blit(ann,annr)
        s = float(statistics.mean(self.time))
        ann = font_title.render("Time :"+str(format(s,".5f")), True, (255,255,255))
        annr = ann.get_rect(center = (836,60))
        screen.blit(ann,annr)
       
        ann = font_title.render("Miner Status :   Mine   Idle", True, (255,255,255))
        annr = ann.get_rect(center = (600,120))
        screen.blit(ann,annr)

        ann = font_title.render("Sharding : ", True, (255,255,255))
        annr = ann.get_rect(center = (1150,60))
        screen.blit(ann,annr)
        
        
    def mod(self,count,screen):
        if(count==0):
            temp = (self.circle[0][0]/180)*120
            temp =int(temp)-28
            self.changeusernum(temp)
        if(count==1):
            temp = (self.circle[1][0]/180)*20
            temp =int(temp)
            self.tr=temp-33
        if(count==2):
            temp = (self.circle[2][0]/180)*50
            temp =int(temp)
            self.size=(temp-153)*15
            c.rs=True
            self.resize()
        if(count==3):
            temp = (self.circle[3][0]/180)*1000
            temp =int(temp)
            self.dl=temp-1005
        if(count==4):
            
            self.s=not(self.s)
            
            self.blockprinter(screen);pygame.display.update()
            
    def blockprinter(self,screen):
        x,y=0,160
        cout=0
        if(not(self.s)):
            pygame.draw.rect(screen,[25,255,158],[x,y,10,10]);x+=15
        if(self.s):
            col = [[255,0,0],[0,0,255],[0,255,0],[0,255,255]]
            #print("It is in the following")
            for x1 in self.blocks:
                cout+=1;
                if(cout%53==0):
                    x=0;y+=20
                pygame.draw.rect(screen,col[cout%4],[x,y,10,10]);
                x+=15
            return
        
        for x1 in self.blocks:
            cout+=1;
            if(cout%53==0):
                x=0;y+=20
            pygame.draw.rect(screen,[15,100,255],[x,y,10,10])
            x+=15
    def tableprinter(self,num=1):
        
        if(num==''):
            return
        num=int(num)
        font_title = pygame.font.Font(None,30)
        ann = font_title.render("Block Details:"+str(num), True, (255,255,255))
        annr = ann.get_rect(center = (1010,210))
        screen.blit(ann,annr)
        
        ann = font_title.render("Version:0.1v", True, (255,255,255))
        annr = ann.get_rect(center = (930,270))
        screen.blit(ann,annr)
        bts = self.blocks[num]
        ann = font_title.render("Nonce:"+str(bts.nonce), True, (255,255,255))
        annr = ann.get_rect(center = (1130,270))
        screen.blit(ann,annr)

        bts = self.blocks[num-1]
        temp = "{}".format(bts)
        string =str(hashlib.sha256(temp.encode()).hexdigest())
        ann = font_title.render("Previous Hash:"+string[0:30], True, (255,255,255))
        annr = ann.get_rect(center = (1050,340))
        screen.blit(ann,annr)
        bts = self.blocks[num]
        li = bts.transactions
        y=400
        font_title = pygame.font.Font(None,20)
        for x in range(0,10):
            to,fro,amt = li[x].to,li[x].fro,li[x].amt
            ann = font_title.render("To:"+str(to)+"   "+"From:"+str(fro)+"   "+"Amount:"+str(amt)[0:8], True, (255,255,255))
            annr = ann.get_rect(center = (1050,y))
            y+=20
            screen.blit(ann,annr)
            
            
def extract(rod):
    leng = len(c.blocks)
    
    for x in range(0,leng):
        block =Rodda()
        while(True):
                block.nonce+=1;
                temp = "{}{}{}{}".format(block.index,block.p_hash,block.nonce,block.transactions)
                
                string =str(hashlib.sha256(temp.encode()).hexdigest())
                
                val = sum(bytearray(string.encode()))
                
                if(val>1000):
                    val%=1000
                if(val > dl):
                    c.blocks.append(block)
c= Controller()

screen = pygame.display.set_mode((1300,650))
pygame.display.set_caption("BlockChainSim-2021")
clock = pygame.time.Clock()
pygame.font.init()
a = time.time()
base_font = pygame.font.Font(None, 32)
user_text = ''

input_rect = pygame.Rect(1000, 130, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False
while True:
    screen.fill((0,0,0));clock.tick(35);
    for x in range(0,len(c.ui)):
        pygame.draw.rect(screen,[205,125,250],c.ui[x])
        pygame.draw.circle(screen,[25,180,60],c.circle[x],10)
    #Block size No of transactions a block can hold
    pygame.draw.rect(screen,[255,255,255],[0,150,800,500])
    
                    
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
      
    # display.flip() will update only a portion of the
    # screen to updated, not full area
    #pygame.display.flip()_text
    c.lable(screen)
    b = time.time()
    s = float(b-a)
    c.blockprinter(screen)
    c.tableprinter(user_text)
    if(s>1 and not(c.rs)):
        c.maketrans()
        a= time.time()
    if(c.count-c.size>(len(c.blocks)-1)*c.size):
        if(not(c.s)):
            pygame.draw.rect(screen,[255,255,255],[626,110,50,20],3);pygame.display.update()
        
        c.createblock()
    
    pygame.draw.rect(screen,[255,255,255],[685,108,50,22],3);pygame.display.update()
    
        
    #print("Sairam:",c.count,len(c.blocks))
    
    
    
        
    
