import socket
import sqlite3 as sl
import random

def ispresent_for_marketd(data):
    db = sl.connect("marketplace.db")
    sql = db.cursor()
    stream = ""
    Let = ""
    for i in range(0, len(data)):
        Let += str(data[i])
    print(Let)
    for value in sql.execute(f"SELECT * FROM Market WHERE Car_ID = '{Let}'"):
        stream += str(value) + ";"
    if len(stream) < 2:
        return 0
    else:
        return 1

def ispresent_for_marketv(data):
    db = sl.connect("marketplace.db")
    sql = db.cursor()
    stream = ""
    print(data, "!")

    for value in sql.execute(f"SELECT * FROM Market WHERE Car_Name = '{data}'"):
        stream += str(value) + ";"
    if len(stream) < 2:
        return 0
    else:
        return 1


def ispresent_for_avgd(data):
    db = sl.connect("garage.db")
    sql = db.cursor()
    stream = ""
    for value in sql.execute(f"SELECT * FROM Cars WHERE Car_Name = '{data}'"):
        stream += str(value) + ";"
    if len(stream) < 2:
        return 0
    else:
        return 1


def ispresent(data):
    db = sl.connect("garage.db")
    sql = db.cursor()
    stream = ""
    for value in sql.execute(f"SELECT * FROM Cars WHERE Car_Name = '{data}'"):
        stream += str(value) + ";"
    if len(stream) < 2:
        return 0
    else:
        return 1



def view(message):
    print(message)
    db = sl.connect("marketplace.db")
    sql = db.cursor()
    data = ""
    for value in sql.execute("SELECT * FROM Market"):
        data += str(value) + ";"

    return data


def view_market(data):
    print(str(data))
    db = sl.connect("marketplace.db")
    sql = db.cursor()
    Let =""
    for i in range(1,len(data)):
        Let += data[i]
    data = ""
    if ispresent_for_marketv(Let) == 1:
        for value in sql.execute(f"SELECT * FROM Market WHERE Car_Name = '{Let}' ORDER BY Damage"):
            data += str(value) + ";"

        return data
    else:
        data = "Car didn't find?"
        return data

def view_avg(message):
    print(message)
    db = sl.connect("garage.db")
    sql = db.cursor()
    data = ""
    for value in sql.execute("SELECT * FROM Cars"):
        data += str(value) + ";"
    return data


def add_market(data):
    print(data)
    otter = ""
    i = 1
    while data[i] != ";":
        otter += data[i]
        i+=1
    if ispresent(otter) == 1:
        db = sl.connect("marketplace.db")
        sql = db.cursor()

        garage = sl.connect("garage.db")
        cursors = garage.cursor()

        sql.execute("""CREATE TABLE IF NOT EXISTS Market(
                   Car_ID INT,
                   Car_Name TEXT,
                   Cost BIGINT,
                   Mileage BIGINT,
                   Color_damage_right INT,
                   Color_damage_left INT,
                   Color_damage_front INT,
                   Color_damage_rear INT,
                   Engine_damage INT,
                   Suspension_damage INT,
                   Lights_damage INT,
                   Mirrors_damage INT,
                   Electronics_damage INT,
                   Damage INT)""")

        db.commit()


        car = ""
        Avg = ""
        Miles = ""
        CD_r = ""
        CD_l = ""
        CD_f = ""
        CD_b = ""
        ED = ""
        SD = ""
        LD = ""
        MD = ""
        ElD = ""
        # DP = CD_r + CD_l + CD_f + CD_b + ED + SD + LD + MD + ElD

        k = 0

        for i in range(1,len(data)):
            if data[i]!=";" and k == 0:
                car+=str(data[i])
            elif data[i]!=";" and k == 1:
                Avg+=str(data[i])
            elif data[i]!=";" and k == 2:
                Miles+=str(data[i])
            elif data[i]!=";" and k == 3:
                CD_r+=str(data[i])
            elif data[i]!=";" and k == 4:
                CD_l+=str(data[i])
            elif data[i]!=";" and k == 5:
                CD_f+=str(data[i])
            elif data[i]!=";" and k == 6:
                CD_b+=str(data[i])
            elif data[i]!=";" and k == 7:
                ED+=str(data[i])
            elif data[i]!=";" and k == 8:
                SD+=str(data[i])
            elif data[i]!=";" and k == 9:
                LD+=str(data[i])
            elif data[i]!=";" and k == 10:
                MD+=str(data[i])
            elif data[i]!=";" and k == 11:
                ElD+=str(data[i])
            else:
                k+=1

        if Avg.isdigit() == True and Miles.isdigit() == True:

            DP = int(CD_r) + int(CD_l) + int(CD_f) + int(CD_f) + int(ED) + int(SD) + int(LD) + int(MD) + int(ElD)

            """ Поясняю за Класс автомобиля - это не привичный А - мини-автомобиль, E - Автомобиль бизнес-класса. Нет
            Каждая буква закрепленна за ценовым сегментом.
            A - До миллиона
            B - 1 - 3 миллиона
            C - 3 - 7 миллиона
            D - 7 - 15 миллионов
            E - Более 15 """

            for value in cursors.execute(f"SELECT * FROM Cars WHERE Car_Name = '{car}'"):
                if value[2] == "A":
                    absolute = 100000 + 10000 * DP
                if value[2] == "B":
                    absolute = 200000 + 40000 * DP
                if value[2] == "C":
                    absolute = 300000 + 60000 * DP
                if value[2] == "D":
                    absolute = 500000 + 100000 * DP
                if value[2] == "E":
                    absolute = 1000000 + 200000 * DP
                if int(Avg) < int(value[1]) + absolute and int(Avg) > int(value[1]) - absolute:
                    sql.execute("SELECT Car_Name FROM Market")
                    ID = random.randint(0, 100000)

                    sql.execute(f"INSERT INTO Market VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                (ID, car, int(Avg), int(Miles), int(CD_r), int(CD_l), int(CD_f), int(CD_b), int(ED), int(SD), int(LD), int(MD), int(ElD), int(DP)))
                    db.commit()

                    data = "Car passed!"
                    return data

                else:
                    data = "Car not passed :("
                    return data
        else:
            if Avg.isdigit() == False and Miles.isdigit() == False:
                data = "Wrong cost and mileage"
                return data
            elif Avg.isdigit() == False:
                data = "Wrong cost"
                return data
            elif Miles.isdigit() == False:
                data = "Wrong mileage"
                return data
    else:
        data = "No such car in database"
        return data


def add_avg(data):
    i = 1
    otter = ""
    while data[i]!=";":
        otter+=data[i]
        i+=1
    if ispresent(otter) == 0:
        db = sl.connect("garage.db")
        sql = db.cursor()

        sql.execute("""CREATE TABLE IF NOT EXISTS Cars(
                Car_Name TEXT,
                Avg_cost BIGINT,
                Car_class TEXT)""")

        db.commit()


        car = ""
        Avg = ""

        k = 0
        for i in range(1, len(data)):
            if data[i]!=";" and k == 0:
                car+=str(data[i])
            elif data[i]!=";" and k == 1:
                Avg+=str(data[i])
            else:
                k+=1
        if Avg.isdigit() == True:

            if int(Avg) <= 1000000:
                Classcar = "A"
            elif int(Avg) > 1000000 and int(Avg) <= 3000000:
                Classcar = "B"
            elif int(Avg) > 3000000 and int(Avg) <= 7000000:
                Classcar = "C"
            elif int(Avg) > 7000000 and int(Avg) <= 15000000:
                Classcar = "D"
            else:
                Classcar = "E"

            sql.execute("SELECT Car_Name FROM Cars")

            sql.execute(f"INSERT INTO Cars VALUES (?,?,?)", (car, Avg, Classcar))
            db.commit()

            data = "New car add!"
            return data
        else:
            data = "Incorrect cost"
            return data

    else:
        data = "Car already exist!"
        return data


def delete_market(data):
    otter =""
    for i in range(1, len(data)):
        otter += data[i]
    if ispresent_for_marketd(otter) == 1:

        db = sl.connect("marketplace.db")
        sql = db.cursor()

        delete = ""
        for i in range(1, len(data)):
            delete += str(data[i])

        sql.execute(f"DELETE FROM Market WHERE Car_ID = '{int(delete)}'")
        db.commit()

        data = "Car delete!"
        return data
    else:
        data = "No such car in database"
        return data


def delete_avg(data):
    otter = ""
    for i in range(1,len(data)):
        otter+=data[i]
    if ispresent_for_avgd(otter) == 1:

        db = sl.connect("garage.db")
        sql = db.cursor()
        delete = ""
        for i in range(1, len(data)):
            delete += str(data[i])

        sql.execute(f"DELETE FROM Cars WHERE Car_name = '{delete}'")
        db.commit()

        data = "Car delete!"
        return data
    else:
        data = "No such car in DataBase"
        return data


def alt(data):
    print(data)
    message = "You don't have rights to do that"
    return message


def Main():
    host = '192.168.1.52'  # Server ip ВСТАВИТЬ СВОЙ IP!
    port = 3001
    myHostName = socket.gethostname()
    #host = socket.gethostbyname(myHostName)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))


#4294967296
    print("Server Started")
    while True:
        data, addr = s.recvfrom(4294967296)
        data = data.decode('utf-8')
        print("Message from: " + str(addr))
        print("From connected user: " + data)
        inp = data[0]
        out = {'1': view_market, '2': view_avg, '3': add_market, '4': add_avg, "5": delete_market, "6": delete_avg,
               "7": view, "A": alt}[inp](data)


        s.sendto(out.encode('utf-8'), addr)
    s.close()


if __name__ == '__main__':
    Main()