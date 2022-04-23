import time
import hashlib
import random,string
import pygame
import statistics
#THink in pygame style instead of looping in a function use main loop where  gam eis done
#Need to create something such that call the validaor first then {read 1st statement}
#UI should be taken care of like it should state the validation time as well as mining time

#**Try Making 2 Apps with different CAs PoW does not have voting nodes number and
#**and Raft has no difficulty

#Need to Implement voting although a random is done but may be create a new class called nodes
#Which can cast there votes give numbers to the miners and let them choose or other way round
#Need to create a election and forget about the nonce thing 
#The flow is a new block is mined adn then validated 3 miners have/should generate new
#BLock and election would be conducted{Rember pygame logic} and the highest will be selected
# Added to teh chain 
class User:
    def __init__(self):
        self.private = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
        self.bal = random.randint(10,50)
        self.cot =0
class Transaction:
    def __init__(self,to,fro,amt,ti,fi):
        self.to,self.fro,self.amt = to,fro,amt
        self.ti,self.fi=ti,fi#TO Index,
        
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
        self.nd = 380#Netwrok difficulty on the scale of 1000
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
        pygame.init()
        for x in range(0,5):
            self.users.append(User())
        for x in range(0,20):
            self.maketrans()
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
        

    def minera(self,block):
        
        for x in range(0,15):
            temp =self.miners[x%3].mining(self.chain[-1])
            if(temp>self.nd):
                self.name = self.miners[x%3].name
                self.chain.append(block)
                self.mining = False
                return

            
   
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
    
    def lable(self,screen):
        font_title = pygame.font.Font(None,30)
        ann = font_title.render("No. Of Users", True, (255,255,255))
        annr = ann.get_rect(center = (120,25))
        screen.blit(ann,annr)
        ann = font_title.render("Transaction Rate", True, (255,255,255))
        annr = ann.get_rect(center = (380,25))
        screen.blit(ann,annr)
        ann = font_title.render("Difficulty:", True, (255,255,255))
        annr = ann.get_rect(center = (640,25))
        screen.blit(ann,annr)
        ann = font_title.render("Miner Status:   Alpha                          Beta                          Gamma", True, (255,255,255))
        annr = ann.get_rect(center = (350,120))
        screen.blit(ann,annr)
        ann = font_title.render(str(self.un), True, (255,255,255))
        annr = ann.get_rect(center = (120,80))
        screen.blit(ann,annr)
        
        ann = font_title.render(str(self.tr), True, (255,255,255))
        annr = ann.get_rect(center = (380,80))
        screen.blit(ann,annr)
        
        ann = font_title.render(str(self.nd-307), True, (255,255,255))
        annr = ann.get_rect(center = (640,80))
        screen.blit(ann,annr)
        
        
        
        ann = font_title.render("Total Transactions:"+str(self.count), True, (255,255,255))
        annr = ann.get_rect(center = (870,10))
        screen.blit(ann,annr)

        ann = font_title.render("# of Blocks:"+str(len(self.chain)), True, (255,255,255))
        annr = ann.get_rect(center = (1150,10))
        screen.blit(ann,annr)
        
       
        
        ann = font_title.render("MemPool Transactions : "+str(len(self.mp)), True, (255,255,255))
        annr = ann.get_rect(center = (1000,40))
        screen.blit(ann,annr)

        vt = statistics.mean(self.vtime)
        mt = statistics.mean(self.mtime)
        ti = vt+mt
        ti=str(format(ti,".5f"))
        ann = font_title.render("Time Taken : "+ti, True, (255,255,255))
        annr = ann.get_rect(center = (1000,80))
        screen.blit(ann,annr)
        ti = str(format(vt,".5f"))
        ann = font_title.render("Validating : "+ti, True, (255,255,255))
        annr = ann.get_rect(center = (870,120))
        screen.blit(ann,annr)
        ti = str(format(mt,".5f"))
        
        ann = font_title.render("Mining : "+ti, True, (255,255,255))
        annr = ann.get_rect(center = (1100,120))
        screen.blit(ann,annr)

        ann = font_title.render("Last Blocked Mined By: "+self.name, True, (255,255,255))
        annr = ann.get_rect(center = (1000,150))
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
            print(self.tr)
        if(count==2):
            temp = (self.circle[2][0]/180)*100
            temp =int(temp)
            self.nd=temp#While Printing add this  -306
            

    def blockprinter(self,screen):
        x,y=0,160
        cout=0
        
        for x1 in self.chain:
            cout+=1;
            if(cout%53==0):
                x=0;y+=20
            pygame.draw.rect(screen,[15,100,255],[x,y,10,10])
            x+=15
    
    def tableprinter(self,screen,num):
        
        if(num=='' ):
            return
        
        pygame.draw.rect(screen,[25,255,25],[820,220,410,400],2,3)
        pygame.draw.rect(screen,[25,255,255],[820,265,410,30],2,3)
        pygame.draw.rect(screen,[25,255,255],[820,295,410,30],2,3)
        pygame.draw.rect(screen,[25,255,255],[820,325,410,30],2,3)
        pygame.draw.rect(screen,[201,205,64],[825,360,400,250],0,3)
        
        num=int(num)
        
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

    input_rect = pygame.Rect(950, 170, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False
    a= time.time()
    block = c.validator()
    c.mining = True
    troy = time.time()#Validating time
    troy1 = time.time()
            
    while True:
        screen.fill((0,0,0));clock.tick(35);
        pygame.draw.rect(screen,[255,255,255],[0,150,800,500])
    
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
        if(not(c.mining)and len(c.mp)>c.bs):
            troy = time.time()#Validating time
            troy1 = time.time()
            block = c.validator()
            c.vtime.append(float(time.time()-troy))
            c.mining=True
        c.minera(block)
        c.tableprinter(screen,user_text)
        if(c.mining==False):
            c.mtime.append(float(time.time()-troy1))
            pygame.draw.rect(screen,[255,255,255],[180,105,60,25],3)
            pygame.draw.rect(screen,[255,255,255],[590,105,80,25],3)
            pygame.draw.rect(screen,[255,255,255],[385,105,60,25],3)
        
            
        pygame.display.update()
    


    