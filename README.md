# hotelBooking
Using OOP to create a Hotel Booking Console Text.  At start, the program will read the hotel.csv as a pandas dataframe, then display all hotels.

The user will then select a hotel based on index (not by id).  If the hotel has availability, it will then ask the user for a name on the reservation, then ask for credit card information.  The credit card will be validated to make sure the input is correct, then it will ask the user to authenticate with a password.  If authenticated, then it will process the reservation, where a message will display in the console as a similar receipt.

The program will then ask if the user wants to include a SPA package; if yes, then it will also charge the same credit card and display another receipt.

Then there are class functions to save the reservations for the hotel and spa into 2 separate json files.  This will keep track of the count on the number of reservations.

## Python Features
1. Object Oriented Programming
2. __init__(self)
3. Classes - **(Inheritance)**
    1. A Parent class can hold the init fx
    2. A Child class will inherit the parents functions
    3. A Child class can override a parent's function
4. Pandas
    1. read csv files - using flags like `dtype=str`
    2. data manipulation using `*.loc`
    3. converting to dict using `pd.read_csv(<file>, dtype=str).to_dict(orient='records')`
    4. converting back to csv with `.to_csv(<file>, index=False)`
5. JSON
    1. using json to load/dumps from/to a file
