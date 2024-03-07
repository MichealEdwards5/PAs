import random

SEC_PER_ITEM=4
OVERHEAD_SECONDS=45
TOTAL_TEST_TIME=7200
DATA_INTERVAL=50
REGISTER=5

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    def front(self):
        return self.items[-1]
            
class Register():
    def __init__(self,express=False):
        self.express=express
        self.current_job=None
        self.checkout_time_remaining=0
        self.queue=Queue()
        self.customers_served=0
        self.items_total=0
        self.idle_time=0
        self.queue=Queue()
        self.wait_time=0
      
    def add_wait_time(self):
        if self.current_job!=None or not self.queue.isEmpty():
            self.wait_time+=1
            
    def get_wait_time(self):
        return self.wait_time
        
    def serve_customer(self):
        self.customers_served += 1
        return self.customers_served
    
    def add_item_total(self,items):
        self.items_total += items
        return self.items_total
    
    def add_idle_time(self):
        self.idle_time +=1
        
    def get_customers_served(self):
        return self.customers_served
    
    def get_item_total(self):
        return self.items_total
    
    def get_idle_time(self):
        return self.idle_time
    
    def is_express(self):
        return self.express
    
    def tick(self):
        if not(self.idle()):
            self.checkout_time_remaining-=1
            if self.checkout_time_remaining<=0:
                self.current_job=None
                
    def idle(self):
        return (self.current_job==None)
    
    def add_customer(self,customer):
        self.queue.enqueue(customer)
        if self.current_job==None:
            new_job=self.queue.dequeue()
            self.current_job=new_job.get_items()
            self.checkout_time_remaining=new_job.checkout_time()

class Customer():
    def __init__(self):
        self.items=random.randint(6, 20)
    
    def get_items(self):
        return self.items
    
    def checkout_time(self):
        return self.items*SEC_PER_ITEM+OVERHEAD_SECONDS
       
def create_registers(REGISTERS):
    registers={}
    for i in range(REGISTERS):
        if i == 0:
            registers['register_'+str(i)]=Register(express=True)
        else:
            registers['register_'+str(i)]=Register()
    return registers
   
def choose_register(customer_queue,registers):
    best_registers=[]

    for i in range(len(registers)):
        best_registers.append((registers['register_'+str(i)].checkout_time_remaining,'register_'+str(i)))
    
    best_registers=sorted(best_registers)

    for register in best_registers:

        if not customer_queue.isEmpty() and (customer_queue.front().get_items())<=10:
            customer_items=customer_queue.front().get_items()
            registers[best_registers[0][1]].add_customer(customer_queue.dequeue())
            registers[best_registers[0][1]].serve_customer()
            registers[best_registers[0][1]].add_item_total(customer_items)
            
        elif not customer_queue.isEmpty() and customer_queue.front().get_items()>10 and not registers[best_registers[0][1]].is_express():
            customer_items=customer_queue.front().get_items()
            registers[best_registers[0][1]].add_customer(customer_queue.dequeue())
            registers[best_registers[0][1]].serve_customer()
            registers[best_registers[0][1]].add_item_total(customer_items)
            
        elif not customer_queue.isEmpty() and customer_queue.front().get_items()>10 and registers[best_registers[0][1]].is_express() and registers[best_registers[1][1]].current_job==None:
            customer_items=customer_queue.front().get_items()
            registers[best_registers[1][1]].add_customer(customer_queue.dequeue())
            registers[best_registers[1][1]].serve_customer()
            registers[best_registers[1][1]].add_item_total(customer_items)
                    
    return customer_queue,registers
        
def display_50(registers,current_sec):
    print(f'Time={current_sec}')
    print('Register #     Customer')

    for i in range(len(registers)):
        current_job=registers["register_"+str(i)].current_job
        queue='-'
        if not registers["register_"+str(i)].queue.isEmpty():
            queue=registers["register_"+str(i)].queue.items[0].get_items()
        if current_job==None:
            current_job='-'
        print(f'{i:9d}{current_job:>6} | {queue:>4} ')
   
def sim(simLength,REGISTERS,register_stats=None):
    registers=create_registers(REGISTERS)
    customer_queue=Queue()
    
    if register_stats==None:
        register_stats={}
        for i in range(len(registers)):
            register_stats['register_'+str(i)+'_customers_served']=0
            register_stats['register_'+str(i)+'_items_total']=0
            register_stats['register_'+str(i)+'_idle_time']=0
            register_stats['register_'+str(i)+'_wait_time']=0
            register_stats['register_total_customers']=0
    for current_sec in range(simLength):
        if current_sec % DATA_INTERVAL==0:
            display_50(registers, current_sec)
        if current_sec%30==0:
            customer=Customer()
            customer_queue.enqueue(customer)
            
        if customer_queue.size()!=0:
            for i in range(customer_queue.size()):
                customer_queue,registers=choose_register(customer_queue, registers)
                    
        for i in range(len(registers)):
            register=registers['register_'+str(i)]
            register.tick()
            if register.idle():
                register.add_idle_time()
            elif not register.queue.isEmpty():
                register.add_wait_time()
                
        if current_sec+1==TOTAL_TEST_TIME:
            for i in range(len(registers)):
                register_stats['register_'+str(i)+'_customers_served']=register_stats['register_'+str(i)+'_customers_served']+registers['register_'+str(i)].get_customers_served()
                register_stats['register_'+str(i)+'_items_total']=register_stats['register_'+str(i)+'_items_total']+registers['register_'+str(i)].get_item_total()
                register_stats['register_'+str(i)+'_idle_time']=register_stats['register_'+str(i)+'_idle_time']+registers['register_'+str(i)].get_idle_time()
                register_stats['register_'+str(i)+'_wait_time']=register_stats['register_'+str(i)+'_wait_time']+registers['register_'+str(i)].get_wait_time()
                register_stats['register_'+str(i)+'_avg_wait_time']=register_stats['register_'+str(i)+'_wait_time']/register_stats['register_'+str(i)+'_customers_served']

    return register_stats

def print_totals(register_stats):
    print(f"{'total':>45s}{'average':>15s}" )
    print(f"{'total':>17s}{'total':>15s}{'idle time':>15s}{'wait time':>14s}")
    print(f"Register{'customer':>11s}{'items':>13s}{'(min)':>13s}{'(sec)':>14s}")
    for i in range(REGISTER):
        if i==0:
                print(f"{'express':^8}{register_stats['register_'+str(i)+'_customers_served']:^12}{register_stats['register_'+str(i)+'_items_total']:^18}{'':2}{register_stats['register_'+str(i)+'_idle_time']/60:.2f}{'':8}{register_stats['register_'+str(i)+'_avg_wait_time']:>.2f}")
        else:
            print(f"{i:^8}{register_stats['register_'+str(i)+'_customers_served']:^12}{register_stats['register_'+str(i)+'_items_total']:^18}{'':2}{register_stats['register_'+str(i)+'_idle_time']/60:.2f}{'':8}{register_stats['register_'+str(i)+'_avg_wait_time']:>.2f}")
    print('_'*65)
    print(f"{'TOTAL':^8}{register_stats['register_total_customers']:^12}{register_stats['register_total_items']:^19}{register_stats['register_total_idle']:.2f}")

def main():
    cust_sum=0
    item_sum=0
    idle_sum=0
    for i in range(12):
        if i==0:
            register_stats=None
            
        else:
            register_stats=register_stats
        register_stats=sim(TOTAL_TEST_TIME,REGISTER,register_stats) 
    for i in range(REGISTER):
        cust_sum+=register_stats['register_'+str(i)+'_customers_served']
        item_sum+=register_stats['register_'+str(i)+'_items_total']
        idle_sum+=register_stats['register_'+str(i)+'_idle_time']
        register_stats['register_total_customers']=cust_sum
        register_stats['register_total_items']=item_sum
        register_stats['register_total_idle']=idle_sum/60

    print_totals(register_stats)
main()    
   
    






