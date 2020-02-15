import sys
import random
import string
import sqlite3 as lite
import time
from multiprocessing import Process

class Config(object):
    def __init__(self):
        self.n = 10
        self.region = 1
        self.error_rate = 0.5
        self.hide_output = False
        self.core = 4

class Data(object):
    def __init__(self, config):
        connection = lite.connect("randman.db")
        cursor = connection.cursor() 
        with connection:
            cursor.execute("SELECT name FROM surnames WHERE (sex = 0 OR sex = 2) AND country_id = " + str(config.region))
            self.surnames_man = cursor.fetchall()          
            cursor.execute("SELECT name FROM surnames WHERE (sex = 0 OR sex = 1) AND country_id = " + str(config.region))
            self.surnames_woman = cursor.fetchall()        
            cursor.execute("SELECT name FROM names WHERE (sex = 0 OR sex = 2) AND country_id = " + str(config.region))
            self.names_man = cursor.fetchall()             
            cursor.execute("SELECT name FROM names WHERE (sex = 0 OR sex = 1) AND country_id = " + str(config.region))
            self.names_woman = cursor.fetchall()           
            cursor.execute("SELECT name FROM patronymics WHERE (sex = 0 OR sex = 2) AND country_id = " + str(config.region))
            self.patronymics_man = cursor.fetchall()       
            cursor.execute("SELECT name FROM patronymics WHERE (sex = 0 OR sex = 1) AND country_id = " + str(config.region))
            self.patronymics_woman = cursor.fetchall()     
            cursor.execute("SELECT name FROM countries WHERE country_id = " + str(config.region))
            self.chosen_country = cursor.fetchall()[0][0]
            cursor.execute("SELECT name FROM states WHERE country_id = " + str(config.region))
            self.states = cursor.fetchall()              
            cursor.execute("SELECT name FROM cities WHERE country_id = " + str(config.region))
            self.cities = cursor.fetchall()
            cursor.execute("SELECT name FROM streets WHERE country_id = " + str(config.region))
            self.streets = cursor.fetchall()             
            cursor.execute("SELECT phone FROM phone_templates WHERE country_id = " + str(config.region))
            self.phone_templates = cursor.fetchall()  
    def get_surname_man(self): 
        return random.choice(self.surnames_man)[0]
    def get_name_man(self): 
        return random.choice(self.names_man)[0]
    def get_patronymic_man(self): 
        if len(self.patronymics_man) > 0: return random.choice(self.patronymics_man)[0]
        else: return ""
    def get_surname_woman(self): 
        return random.choice(self.surnames_woman)[0]
    def get_name_woman(self): 
        return random.choice(self.names_woman)[0]
    def get_patronymic_woman(self): 
        if len(self.patronymics_woman) > 0: return random.choice(self.patronymics_woman)[0]
        else: return ""
    def get_state(self): 
        return random.choice(self.states)[0]
    def get_city(self): 
        return random.choice(self.cities)[0]
    def get_street(self): 
        return random.choice(self.streets)[0]
    def get_phone_template(self): 
        return random.choice(self.phone_templates)[0]

class Man(object):
    def __init__(self, sex, surname, name, patronymic, phone_number):
        self.sex = sex
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.phone_number = phone_number
    def getstr(self):
        outstring = self.surname + " " + self.name                                                    
        if len(self.patronymic) > 0: outstring += " " + self.patronymic
        outstring += ";" 
        return outstring
    def getstr_phone_number(self):
        return self.phone_number

class Address(object):
    def __init__(self, country, state, city, street, house, flat):
        self.country = country
        self.state = state
        self.city = city
        self.street = street
        self.house = house
        self.flat = flat
    def getstr(self):
        outstring = self.country + ", " + self.state + ", " + self.city + ", " + self.street + ", " 
        outstring += self.house + ", " + self.flat + ";"
        return outstring

def generation_phone_number(number_template):
    number = ""
    for i in range(len(number_template)):
        if number_template[i] != "*":
            number += number_template[i]
        else:
            number += str(random.randint(0,9))
    return number

def rand_man(data):
    sex = random.randint(1,2)                                      
    if sex == 1: 
        surname = data.get_surname_man()
        name = data.get_name_man()
        patronymic = data.get_patronymic_man()
    else:
        surname = data.get_surname_woman()
        name = data.get_name_woman()
        patronymic = data.get_patronymic_woman()
    phone_number = generation_phone_number(data.get_phone_template())    
    return Man(sex, surname, name, patronymic, phone_number)

def rand_address(data):
    state = data.get_state()
    city = data.get_city() 
    street = data.get_street()                                                    
    house = str(random.randint(1,250))                                               
    flat = str(random.randint(1,600))                                                   
    return Address(data.chosen_country, state, city, street, house, flat)

def make_mistakes(number_of_errors, man, address):
    for i in range(number_of_errors):                                                  
        where_error = random.randint(0,9)
        if where_error == 0: man.surname = make_mistake(man.surname, False)
        elif where_error == 1: man.name = make_mistake(man.name, False)
        elif where_error == 2: man.patronymic = make_mistake(man.patronymic, False)
        elif where_error == 3: man.phone_number = make_mistake(man.phone_number, True)
        elif where_error == 4: address.country = make_mistake(address.country, False)
        elif where_error == 5: address.state = make_mistake(address.state, False)
        elif where_error == 6: address.city = make_mistake(address.city, False)
        elif where_error == 7: address.street = make_mistake(address.street, False)
        elif where_error == 8: address.house = make_mistake(address.house, True)
        elif where_error == 9: address.flat = make_mistake(address.flat, True)
    return man, address

def make_mistake(word, only_number):
    word_length_min = 5  #mistake parameters
    word_length_max = 40
    type_of_error = random.randint(0,3)
    j = random.randint(0, len(word))
    word_new = ""
    if type_of_error < 1 and len(word) > word_length_min: 
        for i in range(0, len(word)):
            if i != j: word_new += word[i]
    elif type_of_error < 2 and len(word) < word_length_max:
        if only_number: new_symbol = random.choice(string.digits)
        else: new_symbol = random.choice(string.ascii_letters)
        word_new = word[:j] + ''.join(new_symbol) + word[j:]
    else: 
        rand_i = random.randint(0,len(word))
        for i in range(0, len(word)):
            if i != rand_i: word_new += word[i]
            else: 
                if only_number: new_symbol = random.choice(string.digits)
                else: new_symbol = random.choice(string.ascii_letters)
                word_new += ''.join(new_symbol)
    return word_new

def loop(n, data, config):  
    for i in range(n):  
        man = rand_man(data)
        address = rand_address(data)
        number_of_errors = int(config.error_rate)                                                    
        real_part = config.error_rate - number_of_errors
        number_of_errors += random.choices([0,1], weights=[1.0 - real_part, real_part])[0]
        if number_of_errors > 0: man, address = make_mistakes(number_of_errors, man, address)
        if not config.hide_output: print(man.getstr() + " " + address.getstr() + " " + man.getstr_phone_number())

if __name__ == "__main__":
    config = Config()
    if len (sys.argv) > 4: 
        if sys.argv[4] == "1": config.hide_output = True
    if len (sys.argv) > 3: config.error_rate = float(sys.argv[3])
    if len (sys.argv) > 2: config.region = int(sys.argv[2])
    if len (sys.argv) > 1: config.n = int(sys.argv[1])
    
    time_start = time.time() 
    data = Data(config)
    part_n = (config.n//config.core)
    procs = []
    for index in range(config.core):
        if index == 0: 
            number = config.n - (part_n * config.core) + part_n
        else: number = part_n
        proc = Process(target=loop, args=(number,data,config,))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

    time_end = time.time()  
    print(str(config.n) + " record ready in " + str((time_end - time_start)))