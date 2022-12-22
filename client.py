dict_market = ["Car model: ","Cost: ", "Mileage: ", "Damage to your left: ","Damage to your right: ", "Damage to your front: ", "Damage to your rear: ", "Damage to your engine: ","Damage to your suspension: ","Damage to your lights: ", "Damage to your mirrors: ", "Damage to your electronics: "]
dict = ["Car model: ", "Average cost: "]

def view_market(mes):
    message = "1"
    message += mes
    return message


def view_avg():
    message = "2"
    return message


def add_market(mes):
    message = "3"
    message += mes
    return message


def add_avg(mes):
    message = "4" + mes
    return message


def delete_market(mes):
    message = "5" + mes
    return message


def delete_avg(mes):
    message = "6" + mes
    return message

def view_all():
    message = "7"
    return message


"!!COMMENTED FOR TESTS!!"

"""import random
import socket
dict = ['Volga','Aurus','Vesta','X-Ray','Kamaz','Patrol','Moskvich','Kia K5','Toyota Camry','Kia Sorento','Kia Rio','Kia Soul','Kia Ceed','Kia Optima','Toyota Land Cruiser','Toyota Tundra','Toyota RAV4','Toyota Celica','Toyota Highlander','Toyota Corolla','Nissan Qashqai','Nissan GT-R','Nissan X-Trail','Nissan Teana','Nissan Pathfinder','Nissan Juke','Hyundai Palisade','Hyundai Solaris','Hyundai Santa Fe','Hyundai Sonata','Hyundai Creta','Hyundai Elantra','Citroen Berlingo','EXEED VX','Citroen C1','Citroen C3','Citroen C4','Citroen C5','Audi A3','Audi A4','Audi A5','Audi A6','Audi A7','Audi A8','Audi Q3','Audi Q5','Audi Q7','Audi Q8','BMW 1','BMW 3','BMW 4','BMW 5','BMW 6','BMW 7','BMW X1','BMW X3','BMW X4','BMW X5','BMW X6','Mercedes-Benz A','Mercedes-Benz C','Mercedes-Benz E','Mercedes-Benz S','Mercedes-Benz V','Mercedes-Benz CLA','Mercedes-Benz GL','Chery Amulet','Chery Fora','Chery IndiS','Chery QQ6','Chery Tiggo','Chevrolet Aveo','Chevrolet Camaro','Chevrolet Captiva','Chevrolet Cobat','Chevrolet Cruze','Chevrolet Epica','Chevrolet Lacetti','Chevrolet Lanos','Chevrolet Tahoe','Chevrolet TrailBlazer','Daewoo Gentra','Daewoo Lanos','Daewoo Leganza','Daewoo Magnus','Daewoo Matiz','Daewoo Nexia','EXEED TXL','Volvo S40','Volvo S60','Geely Atlas','Geely Coolray','Geely GC6','Geely GS','Geely MK']




def add_market():
    inp = ""
    inp += "3" + random.choice(dict) + ";" + str(random.randint(0, 50000000)) + ";" + str(random.randint(0,500000)) +";"+ str(
        random.randint(0, 5)) + ";" + str(random.randint(0, 5)) + ";" + str(random.randint(0, 5)) + ";" + str(
        random.randint(0, 5)) + ";" + str(random.randint(0, 5)) + ";" + str(random.randint(0, 5)) + ";" + str(
        random.randint(0, 5)) + ";" + str(random.randint(0, 5)) + ";" + str(random.randint(0, 5)) + ";"
    return inp


# DO

def Main():
    port = 4005
    host = "192.168.1.52"
    server = ('192.168.1.52', 3001)
    # host = '192.168.31.84'
    myHostName = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # host = socket.gethostbyname(myHostName)

    print(host, port)

    s.bind((host, port))
    i = 0
    while (i != 100000):
        ino = add_market()
        print(ino)
        s.sendto(ino.encode('utf-8'), server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print (data)
        i+=1
    s.close()

Main()"""