#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functools import reduce
import math
import sys
import copy
import time
import random


# In[45]:


not_use_pointer = 0
factorys_number = 0
factorys = []
customers_number = 0
customers = []
T = 1
data = None
to_print_customers = []
to_print_factorys = []


# In[3]:


def start(num):
    global not_use_pointer
    global factorys_number
    global factorys
    global customers_number
    global customers
    global T
    global data
    with open("Instances/p"+str(num),'r') as f:
        data = f.read().split()
        #print(data)
        for x in range(len(data)):
            if len(data[x])>10:
                data = data[:x]
                break
        def map_f(x):
            if x[-1]=='.':
                return int(x[:-1])
            else:
                return int(x)
        data = list(map(map_f,data))
    not_use_pointer = 0
    factorys_number = data[not_use_pointer]
    factorys = []
    not_use_pointer += 1
    customers_number = data[not_use_pointer]
    customers = []
    not_use_pointer += 1
    T = 10000
    init()


# In[ ]:





# In[4]:


class Factoray:
    def __init__(self,capacity,open_cost,number):
        self.capacity = capacity
        self.open_cost = open_cost
        self.current_load = 0
        self.number = number
        self.assigned_customers = []
    def assign(self,customer):
        self.assigned_customers.append(customer.number)
        self.current_load += customer.load
    def unassign(self,customer):
        self.assigned_customers.pop(self.assigned_customers.index(customer.number))
        self.current_load -= customer.load
    def clean(self):
        self.curren_load = 0
        self.assigned_customers = []


# In[5]:


class Customer:
    def __init__(self,load,distance_list,number):
        self.load = load
        self.distance_list = distance_list
        self.assigned_factory = None
        self.number = number
    def assign(self,_factory):
        if _factory.capacity - _factory.current_load < self.load:
            return False
        else:
            _factory.assign(self)
            self.assigned_factory = _factory.number
            return True
    def unassign(self):
        if self.assigned_factory != None:
            factorys[self.assigned_factory].unassign(self)
            self.assigned_factory = None
            return True
        return False


# In[6]:


def init():
    global not_use_pointer
    global factorys_number
    global customers_number
    global factorys
    global customers
    global data
    for x in range(factorys_number):
        #print(not_use_pointer)
        factorys.append(Factoray(data[not_use_pointer],data[not_use_pointer+1],x))
        not_use_pointer += 2
    for x in range(customers_number):
        customers.append(Customer(data[not_use_pointer],[],x))
        not_use_pointer += 1
    for x in range(customers_number):
        for y in range(factorys_number):
            customers[x].distance_list.append(data[not_use_pointer])
            not_use_pointer+=1
    #print(not_use_pointer)
            #print(not_use_pointer)


# In[53]:


def judge():
    global factorys
    global customers
    score = 0
    for factory in factorys:
        if factory.current_load != 0:
            score+=factory.open_cost
    for customer in customers:
        score+=customer.distance_list[customer.assigned_factory]
    return score
def output_data():
    _str = ""
    _str +=str(judge())
    _str +="\n"
    for factory in factorys:
        if len(factory.assigned_customers) == 0:
            _str += "0 "
        else:
            _str += "1 "
    _str += "\n"
    for customer in customers:
        _str += str(customer.assigned_factory)+" "
    return _str
def to_print_output_data():
    _str = ""
    _str +=str(judge())
    _str +="\n"
    for factory in to_print_factorys:
        if len(factory.assigned_customers) == 0:
            _str += "0 "
        else:
            _str += "1 "
    _str += "\n"
    for customer in to_print_customers:
        _str += str(customer.assigned_factory)+" "
    return _str   
def judge_from(factorys,customers):
    #global factorys
    #global customers
    score = 0
    for factory in factorys:
        if factory.current_load != 0:
            score+=factory.open_cost
    for customer in customers:
        score+=customer.distance_list[customer.assigned_factory]
    return score


# In[8]:


def find_n_least_big_index(arr,n,drop_factory_number):
    current_big = -1
    current_index_list = []
    for x in range(n):
        inner_big = 1000000
        inner_index = -1
        for y in range(len(arr)):
            if drop_factory_number != None:
                if y == drop_factory_number:
                    continue
            if y not in current_index_list:
                if arr[y] < inner_big:
                    inner_big = arr[y]
                    inner_index = y
        current_index_list.append(inner_index)
        if x == n-1:
            return inner_index


# In[46]:


def gridy():
    global customers
    #print(customers)
    for customer in customers:
        for x in range(len(customer.distance_list)):
            target_index = find_n_least_big_index(customer.distance_list,x+1,None)
            if factorys[target_index].capacity - factorys[target_index].current_load < customer.load:
                continue
            else:
                customer.assign(factorys[target_index])
                break
def random_init():
    backoff()
    global customers
    #print(customers)
    for customer in customers:
        for x in range(len(customer.distance_list)):
            target_index = random.randint(0,len(customer.distance_list)-1)
            #target_index = find_n_least_big_index(customer.distance_list,x+1,None)
            if factorys[target_index].capacity - factorys[target_index].current_load < customer.load:
                continue
            else:
                customer.assign(factorys[target_index])
                break
    
def backoff():
    global customers
    global factorys
    for customer in customers:
        customer.unassign()
    for factory in factorys:
        factory.clean()
def compress_2_3():
    backoff()
    gridy()
    temp_min = judge()
    for x in range(len(factorys)-1):
        backoff()
        gridy()
        empty_facory_reassign(x)
        ## empty how many factory you want
        #empty_facory_reassign(x+1)
        if judge() < temp_min:
            temp_min = judge()
    print(temp_min)
def compress_2for2_3():
    backoff()
    gridy()
    temp_min = judge()
    for x in range(len(factorys)-2):
        ## empty how many factory you want
        #empty_facory_reassign(x+1)
        for y in range(x,len(factorys)-1):
            backoff()
            gridy()
            empty_facory_reassign(x)
            empty_facory_reassign(y)
            if judge() < temp_min:
                temp_min = judge()
    print(temp_min)
def empty_deep(empty_factory_list,start,end):
    global to_print_customers
    global to_print_factorys
    temp_min = 1000000000
    if len(empty_factory_list) > 3:
        return temp_min
    for x in range(start,end):
        backoff()
        gridy()
        for index in empty_factory_list:
            empty_facory_reassign(index)
        if empty_facory_reassign(x) == False:
            return 10000000
        temp_arr = empty_factory_list.copy()
        if judge() < temp_min:
            temp_min = judge()
            to_print_customers = copy.deepcopy(customers)
            to_print_factorys = copy.deepcopy(factorys)
        temp_arr.append(x)
        temp_value = empty_deep(temp_arr,x+1,end)
        if temp_value < temp_min:
            temp_min = temp_value
    return temp_min


# In[36]:


def empty_facory_reassign(number):
    target_factory = factorys[number]
    target_factory.current_load = 0
    free_customers = target_factory.assigned_customers
    target_factory.assigned_customers = []
    for free_customer_number in free_customers:
        for x in range(len(customers[free_customer_number].distance_list)):
            target_index = find_n_least_big_index(customers[free_customer_number].distance_list,x+1,number)
            if factorys[target_index].capacity - factorys[target_index].current_load < customers[free_customer_number].load:
                continue
            else:
                customers[free_customer_number].assign(factorys[target_index])
                break
        if customers[free_customer_number].assigned_factory==None:
            return False


# In[ ]:





# In[ ]:





# In[ ]:





# In[37]:


def possibility(energy):
    if energy <= 0:
        return 0
    global T
    #print(1 - 1/(1+math.e**(-energy/(T))))
    return 1 - 1/(1+math.e**(-energy/(T)))


# In[38]:


def sa():
    global T
    while T>10**(-8):
        T = T*0.995
        for x in range(10):
            print(judge())
            change_customer_index = random.randint(0,len(customers)-1)
            #temp = judge()
            while True:
                ## move lots of customers at the same time
                #move_n_customers()
                change_to_factory_index = random.randint(0,len(factorys)-1)
                if factorys[change_to_factory_index].capacity - factorys[change_to_factory_index].current_load >= customers[change_customer_index].load:
                    #compare which one better
                    energy = 0
                    if factorys[customers[change_customer_index].assigned_factory].current_load == customers[change_customer_index].load:
                        energy -= customers[change_customer_index].load
                    energy += customers[change_customer_index].distance_list[change_to_factory_index]
                    energy -= customers[change_customer_index].distance_list[customers[change_customer_index].assigned_factory]
                    if energy<0 or possibility(energy) > random.random():
                        customers[change_customer_index].unassign()
                        customers[change_customer_index].assign(factorys[change_to_factory_index])
                    break


# In[43]:


def sa2():
    global T
    T = 100
    global customers
    global factorys
    while T > 10**(-8):
        T *= 0.995
        for x in range(10):
            random_drop_number = random.randint(1,len(customers)//2)
            #print(len(customers))
            temp_arr = [x for x in range(len(customers))]
            random.shuffle(temp_arr)
            #temp_arr = random.shuffle(temp_arr)
            #print(temp_arr)
            temp_customers = copy.deepcopy(customers)
            temp_factorys = copy.deepcopy(factorys)
            temp_arr = temp_arr[:random_drop_number]
            #print(random_drop_number)
            for number in temp_arr:
                #temp_customers[number].unassign()
                #can not use them for temp object
                temp_factory = temp_customers[number].assigned_factory
                temp_customers[number].assigned_factory = None
                temp_factorys[temp_factory].current_load -= temp_customers[number].load
                temp_factorys[temp_factory].assigned_customers.pop(temp_factorys[temp_factory]                                                                   .assigned_customers.index(number))
            #print(temp_arr)
            random_start = random.randint(0,len(temp_arr)-1)
            for x in range(random_start,len(temp_arr)):
                x = temp_arr[x]
                customer = temp_customers[x]
                #for x in range(len(customer.distance_list)):
                while True:
                    #randomly
                    target_index = random.randint(0,len(customer.distance_list)-1)
                    #target_index = find_n_least_big_index(customer.distance_list,x+1,None)
                    if factorys[target_index].capacity - factorys[target_index].current_load < customer.load:
                        continue
                    else:
                        customer.assigned_factory = target_index
                        temp_factorys[target_index].current_load += customer.load
                        temp_factorys[target_index].assigned_customers.append(customer.number)
                        #customer.assign(factorys[target_index])
                    break
            for x in range(0,random_start):
                x = temp_arr[x]
                customer = temp_customers[x]
                #for x in range(len(customer.distance_list)):
                while True:
                    #randomly
                    target_index = random.randint(0,len(customer.distance_list)-1)
                    #target_index = find_n_least_big_index(customer.distance_list,x+1,None)
                    if factorys[target_index].capacity - factorys[target_index].current_load < customer.load:
                        continue
                    else:
                        customer.assigned_factory = target_index
                        temp_factorys[target_index].current_load += customer.load
                        temp_factorys[target_index].assigned_customers.append(customer.number)
                        #customer.assign(factorys[target_index])
                    break
            #print(possibility((judge()-judge_from(temp_factorys,temp_customers))))
            if judge_from(temp_factorys,temp_customers) < judge() or possibility(-(judge()-judge_from(temp_factorys,temp_customers))) > random.random():
                customers = temp_customers
                factorys = temp_factorys
                #print(judge())
    return judge()


# In[54]:


with open("3dcompression.txt",'w') as f:
    f2 = open("3dcompression_data.txt",'w')
    for x in range(1,72):
        start_time = time.time()
        start(x)
        gridy()
        f.write("p{} | {} | {}\n".format(str(x),empty_deep([],0,len(factorys)),time.time()-start_time))
        f2.write(output_data())
    f2.close()


# In[ ]:


with open("sa.txt",'w') as f:
    f2 = open("sa_data.txt",'w')
    for x in range(1,72):
        start_time = time.time()
        start(x)
        gridy()
        random_init()
        f.write("p{} | {} | {}\n".format(str(x),sa2(),time.time()-start_time))
        f2.write(to_print_output_data())
    f2.close()


# In[ ]:





# In[18]:





# In[19]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




