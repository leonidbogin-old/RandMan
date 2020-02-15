import sys
import random
import string
import sqlite3 as lite
import time
from threading import Thread

def generation_house_number():
    odds_for_house = random.randint(0,10)
    house_new = 0
    if (odds_for_house < 2): #0.2
        house_new = str(random.randint(150,250))
    elif (odds_for_house < 4): #0.2
        house_new = str(random.randint(50,149))
    else: #0.6
        house_new = str(random.randint(1,49))
    return house_new

def generation_flat_number():
    odds_for_flat = random.randint(0,10)
    flat_new = 0
    if (odds_for_flat > 6): #0.3
        flat_new = random.randint(100,600)
    elif (odds_for_flat > 1): #0.5
        flat_new = random.randint(50,99)
    else: #0.2
        flat_new = random.randint(1,49)
    return flat_new

def generation_phone_number(number_template):
    number = ""
    for i in range(len(number_template)):
        if number_template[i] != "*":
            number += number_template[i]
        else:
            number += str(random.randint(0,9))
    return number

def make_mistake(word):
    word_length_min = 5  #mistake parameters
    word_length_max = 40
    type_of_error = random.randint(0,10)
    j = random.randint(0, len(word))
    word_new = ""
    if type_of_error < 3 and len(word) > word_length_min: 
        for i in range(0, len(word)):
            if i != j: word_new += word[i]
    elif type_of_error < 6 and len(word) < word_length_max:
        word_new = word[:j] + ''.join(random.choice(letters+string.digits)) + word[j:]
    else: 
        for i in range(0, len(word)):
            if i != j: word_new += word[i]
            else: word_new += ''.join(random.choice(letters+string.digits))
    return word_new

def loop():
    sex = random.randint(1,2)                                                             #sex
    if sex == 1: 
        surname = random.choice(surnames_man)[0]                                          #man surname, name, patronymic
        name = random.choice(names_man)[0]
        if len(patronymics_man) > 0: patronymic = random.choice(patronymics_man)[0]
        else: patronymic = ""
    else:
        surname = random.choice(surnames_woman)[0]                                        #woman surname, name, patronymic
        name = random.choice(names_woman)[0]
        if len(patronymics_man) > 0: patronymic = random.choice(patronymics_man)[0]
        else: patronymic = ""
    country = country_original
    state_obj = random.choice(states)
    state = state_obj[2]
    #with connection:                                                                      #city                                                                  
    #    cursor.execute("SELECT name FROM cities WHERE state_id = " + str(state_obj[0]))  
    #    cities = cursor.fetchall()
    #if len(cities) > 0: city = random.choice(cities)[0]                                   
    #else: city = ""
    city = ""
    street = random.choice(streets)[0]                                                    #street
    house = str(generation_house_number())                                                #house
    flat = str(generation_flat_number())                                                  #flat
    phone_number = generation_phone_number(random.choice(phone_templates)[0])                                              #phone_number
    number_of_errors = int(error_rate)                                                    #number of errors
    real_part = error_rate - number_of_errors
    number_of_errors += random.choices([0,1], weights=[1.0 - real_part, real_part])[0]

    for i in range(1, number_of_errors):                                                  #make mistakes
        where_error = random.randint(0,9)
        if where_error == 0: surname = make_mistake(surname)
        elif where_error == 1: name = make_mistake(name)
        elif where_error == 2: patronymic = make_mistake(patronymic)
        elif where_error == 3: country = make_mistake(country)
        elif where_error == 4: state = make_mistake(state)
        elif where_error == 5: city = make_mistake(city)
        elif where_error == 6: street = make_mistake(street)
        elif where_error == 7: house = make_mistake(house)
        elif where_error == 8: flat = make_mistake(flat)
        elif where_error == 9: phone_number = make_mistake(phone_number)
    
    outstring = surname + " " + name                                                     #output
    if len(patronymic) > 0: outstring += " " + patronymic
    outstring += "; "
    outstring += country + ", " + state + ", " + city + ", "
    outstring += street + ", " + str(house) + ", " + str(flat) + "; "
    outstring += phone_number
    #print(outstring)

time_start = time.time() #start

#start parameters
n = 10
region = 1
error_rate = 0.5
if __name__ == "__main__":
    if len (sys.argv) > 3:
        n = int(sys.argv[1])
        region = int(sys.argv[2])
        error_rate = float(sys.argv[3])
    elif len (sys.argv) > 2:
        n = int(sys.argv[1])
        region = int(sys.argv[2])
    elif len (sys.argv) > 1:
        n = int(sys.argv[1])

#choice alphabet
ascii_letters_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
if region == 1 or region == 2:
    letters = ascii_letters_rus
else:
    letters = string.ascii_letters

#get data from database
connection = lite.connect("randman.db")
cursor = connection.cursor() 
with connection:
    cursor.execute("SELECT name FROM surnames WHERE (sex = 0 OR sex = 2) AND country_id = " + str(region))
    surnames_man = cursor.fetchall()          #surnames man
    cursor.execute("SELECT name FROM surnames WHERE (sex = 0 OR sex = 1) AND country_id = " + str(region))
    surnames_woman = cursor.fetchall()        #surnames woman
    cursor.execute("SELECT name FROM names WHERE (sex = 0 OR sex = 2) AND country_id = " + str(region))
    names_man = cursor.fetchall()             #names man
    cursor.execute("SELECT name FROM names WHERE (sex = 0 OR sex = 1) AND country_id = " + str(region))
    names_woman = cursor.fetchall()           #names woman
    cursor.execute("SELECT name FROM patronymics WHERE (sex = 0 OR sex = 2) AND country_id = " + str(region))
    patronymics_man = cursor.fetchall()       #patronymic man
    cursor.execute("SELECT name FROM patronymics WHERE (sex = 0 OR sex = 1) AND country_id = " + str(region))
    patronymics_woman = cursor.fetchall()     #patronymic woman
    cursor.execute("SELECT name FROM countries WHERE country_id = " + str(region))
    country_original = cursor.fetchall()[0][0]#country
    cursor.execute("SELECT * FROM states WHERE country_id = " + str(region))
    states = cursor.fetchall()                #states
    cursor.execute("SELECT name FROM streets WHERE country_id = " + str(region))
    streets = cursor.fetchmany()               #streets
    cursor.execute("SELECT phone FROM phone_templates WHERE country_id = " + str(region))
    phone_templates = cursor.fetchall()       #phone number templates

for i in range(0,n):
    loop()
time_end = time.time()  
print(str(n) + " record ready in " + str((time_end - time_start)))