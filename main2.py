import pandas
from abc import ABC, abstractmethod

df = pandas.read_csv("hotels.csv", dtype={"id": str})


class Hotel:
    watermark = 'The Real Estate Company'

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False
        
    @classmethod
    def update_watermark(cls, msg):
        cls.watermark = msg
    
    @classmethod
    def get_hotel_count(cls, data):
        return len(data)


    def __eq__(self, other):
        if self.hotel_id == other.hotel_id:
            return True
        else:
            return False


class Ticket(ABC):          #ABC makes the entire class an abstract, therefore, it won't compile

    @abstractmethod         #every child will need to code this method
    def generate(self):
        pass





class ReservationTicket(Ticket):
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.the_customer_name}
        Hotel name: {self.hotel.name}
        """
        return content

    @property           #use property to modify variables
    def the_customer_name(self):
        name = self.customer_name.strip()
        name = name.title()
        return name
    
    @staticmethod      #use methods like utility function, a necessary function that might not be associated, but related to get it working
    def convert(amount):
        return amount * 1.2


class DigitalTicket(Ticket):
    def generate(self):
        return 'Hello this is a generate function'
    
    def download(self):
        return 'hi, this is a download function'






print(Hotel.watermark)
# print(Hotel.name)     #<-- this fails since there is no class variable 'name'

hotel1 = Hotel('188')
print(f'name: {hotel1.name}')
print(f'watermark: {hotel1.watermark}')

hotel1.update_watermark('Testing if instance can change the Class watermark')
print(f'watermark2: {hotel1.watermark}')
print(f'Class watermark: {Hotel.watermark}')

print(f'hotel count: {Hotel.get_hotel_count(df)}')
print(f'hotel1 class hotel count: {hotel1.get_hotel_count(df)}')

r = ReservationTicket('john doe', hotel1)
print(r.the_customer_name)
print(r.generate())

print(f'instance static method: {r.convert(250)}')
print(f'class static method: {ReservationTicket.convert(300)}')

print(f'magic method 1 .__add__(3): {1 .__add__(3)}')

print(f'instances comparison hotel1 == hotel2 --> {hotel1 == Hotel("134")}')
print(f'instances comparison hotel1 == hotel1 --> {hotel1 == hotel1}')
print(f'instances comparison hotel1 == Hotel(188) --> {hotel1 == Hotel("188")}')