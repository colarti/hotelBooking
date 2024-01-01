import pandas as pd
import time
import json

class Hotel:
    def __init__(self, hotel_pd):
        self.hotel_pd = hotel_pd
        self.id = hotel_pd['id'].squeeze()
        self.name = hotel_pd['name'].squeeze()
        self.city = hotel_pd['city'].squeeze()
        self.capacity = hotel_pd['capacity'].squeeze()
        self.avail = hotel_pd['available'].squeeze()

    def book_hotel(self):
        self.avail = 'no'  

    def get_dict(self):
        return {'id':self.id, 'name':self.name, 'city':self.city, 'capacity':self.capacity, 'available':self.avail}      

    def available(self):
        temp = self.hotel_pd['available'].squeeze()
        return self.avail

    def get(self):
        return self.hotel_pd


class Hotels:
    def __init__(self):
        self.hotel_list = list()
        self.hotel_pd = None
        self.__parse_hotels()
    
    def view_hotels(self):
        for idx, hotel in enumerate(self.hotel_list):
            print(f'{idx+1}. {hotel.title()}')
    
    def get_hotel_info(self, idx):
        if idx <= len(self.hotel_list): 
            info = self.hotel_pd.loc[self.hotel_pd['name'] == self.hotel_list[idx-1]]
            print(info)
        else:
            print(f'ERR: Invalid Index {idx}')
            info = None

        return info
    
    def __parse_hotels(self, file='hotels.csv'):
        df = pd.read_csv(file)
        self.hotel_pd = df

        for idx, hotel in df.iterrows():
            self.hotel_list.append(hotel['name'])
    
    def update_hotel_status(self, hotel:Hotel):
        self.hotel_pd.loc[self.hotel_pd['name'] == hotel['name'].squeeze(), 'available'] = 'no'
        status = self.hotel_pd.loc[self.hotel_pd['name'] == hotel['name'].squeeze()]
        # print(f'CSV File Updated to : {status}')
        #update csv file with new information
        self.hotel_pd.to_csv('hotels.csv', index=False)


class Reservation:
    count = 1
    res_list = list()

    def __init__(self, name, hotel, cc):
        self.name = name
        self.hotel = hotel
        self.cc = cc.get_dict()

    def generate_reservation(self):
        str_count = f'{Reservation.count:08d}'
        Reservation.res_list.append({'id':str_count, 'name':self.name, 
                                     'hotel':self.hotel.get_dict()['name'],
                                     'cc':self.cc})
        Reservation.count += 1

        msg = f"""\n
            Thank you for your reservation!
            Here are your booking information:
            Name: {self.name}
            Hotel Name: {Reservation.res_list[-1]['hotel']}
            Credit Card on File: {self.cc['number']} <> {self.cc['exp']} <> {self.cc['cvc']}
        """

        return Reservation.res_list[-1], msg

    @classmethod
    def cls_print_res_list(cls):
        print('HOTEL RESERVATION LISTS')
        for res in cls.res_list:
            print(res)
    
    @classmethod
    def cls_save_res_list(cls, file='reslist.json'):
        json_data = json.dumps(Reservation.res_list)

        with open(file, 'w') as f:
            f.write(json_data)
    
    @classmethod
    def cls_read_res_list(cls, file='reslist.json'):
        try:
            with open(file, 'r') as f:
                json_data = json.load(f)
            
            for x in json_data:
                Reservation.res_list.append(x)
            
            Reservation.count = len(json_data)+1
        except:
            pass
        

class SpaReservation(Reservation):
    spa_count = 1
    spa_list = list()\
    
    def generate_reservation(self):
        str_count = f'{SpaReservation.count:08d}'
        SpaReservation.spa_list.append({'id':str_count, 'name':self.name, 
                                     'hotel':self.hotel.get_dict()['name'],
                                     'cc':self.cc})
        SpaReservation.spa_count += 1

        msg = f"""\n
            Thank you for your SPA reservation!
            Here are your SPA information:
            Name: {self.name}
            Hotel Name: {Reservation.res_list[-1]['hotel']}
            Credit Card on File: {self.cc['number']} <> {self.cc['exp']} <> {self.cc['cvc']}
        """

        return SpaReservation.res_list[-1], msg

    @classmethod
    def cls_print_spa_list(cls):
        print('SPA RESERVATION LISTS')
        for res in cls.spa_list:
            print(res)
    
    @classmethod
    def cls_save_spa_list(cls, file='spalist.json'):
        json_data = json.dumps(SpaReservation.spa_list)

        with open(file, 'w') as f:
            f.write(json_data)
    
    @classmethod
    def cls_read_spa_list(cls, file='spalist.json'):
        try:
            with open(file, 'r') as f:
                json_data = json.load(f)
            
            for x in json_data:
                SpaReservation.spa_list.append(x)
            
            SpaReservation.spa_count = len(json_data)+1
        except:
            pass


class CreditCard:
    def __init__(self, name, cc=None, exp=None, cvc=None):
        self.name = name
        self.cc_num = cc
        self.exp = exp
        self.cvc = cvc
    
    def input_data(self):
        self.cc_num = input('Enter the credit card number: ')
        self.exp = input('Enter expiration (MM/YYYY): ')
        self.cvc = input('Enter security numbers: ')
    
    def validate(self):
        pd_cards = pd.read_csv('cards.csv', dtype=str).to_dict(orient='records')

        # print(f'PD_CARDS: {pd_cards}')

        status = True
        # if len(self.cc_num) < 16:
        #     self.cc_num = None
        #     status = False
        
        # m,y = self.exp.split('/')
        # m = int(m)
        # y = int(y)
        # y_diff = int(time.strftime('%Y')) - y
        # if (m < 1 or m > 12) and y_diff < 1:
        #     self.exp = None
        #     status = False

        # if len(self.cvc) < 3 or len(self.cvc) > 4:
        #     self.cvc = None
        #     status = False
        
        info_to_check = {'number':self.cc_num,'expiration':self.exp,'cvc':self.cvc,'holder':self.name}
        if info_to_check not in pd_cards:
            status = False

        return status
    
    def get_dict(self):
        msg = dict()

        msg['number'] = self.cc_num
        msg['exp'] = self.exp
        msg['cvc'] = self.cvc

        return msg

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        pd_password = pd.read_csv('card_security.csv', dtype=str)
        password = pd_password.loc[pd_password['number'] == self.cc_num, 'password'].squeeze()

        # print(f'PASSWORD: {password} --- GIVEN PASSWORD: {given_password}')

        if password != given_password:
            return False
        else:
            return True


if __name__ == '__main__':
    hotels = Hotels()

    hotels.view_hotels()

    hotel_idx = int(input('Enter the hotel number: '))
    hotel = Hotel(hotels.get_hotel_info(hotel_idx))

    if hotel.available() == 'yes':
        customer_name = 'JOHN SMITH'
        customer_cc = SecureCreditCard(cc="1234567890123456",
                                       exp="12/26",
                                       cvc="123",
                                       name=customer_name
                                       )
        # customer_cc.input_data()

        if customer_cc.validate():
            if customer_cc.authenticate(given_password='mypass'):
                Reservation.cls_read_res_list()
                r = Reservation(customer_name.title(), hotel, customer_cc)
                data, msg = r.generate_reservation()

                print(msg)

                hotel.book_hotel()
                hotels.update_hotel_status(hotel.get())

                result = input('Do you want to book a spa package? ')

                if result.strip() in ['yes','y']:
                    SpaReservation.cls_read_spa_list()
                    spa = SpaReservation(customer_name.title(), hotel, customer_cc)
                    data, msg = spa.generate_reservation()

                    print(msg)

                    SpaReservation.cls_print_spa_list()
                    SpaReservation.cls_save_spa_list()
                else:
                    pass
            else:
                print(f'ERR: Credit Card Authenication Failed')
        else:
            print(f'ERR: Invalid Credit Card')

        Reservation.cls_print_res_list()
        Reservation.cls_save_res_list()
    else:
        print(f'ERR: The Hotel has no availability')
    

    