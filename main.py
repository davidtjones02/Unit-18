from guizero import *
import sqlite3
import re
from datetime import datetime


with sqlite3.connect("Silver Dawn Data.db") as db:
   cursor = db.cursor()

if (db):
    # Carry out database work
    print ("Connection successful")
else:
    # No connection to the database
    print ("Connection unsuccessful")

def successScreen():
    success_window = Window(app, title="Success", bg = (253, 71, 74), height = 300)
    text = Text(success_window, text="Success")
    text.text_color = "white"
    text.text_size = 20

    success_button = PushButton(success_window, text="Ok", command=success_window.destroy)

def errorScreen():
    error_screen = Window(app, title="Error, unsuccessful", bg = (253, 71, 74), height = 300)
    text = Text(error_screen, text="Error, unsuccessful \nplease check all fields")
    text.text_color = "white"
    text.text_size = 20

    error_button = PushButton(error_screen, text="Ok", command=error_screen.destroy)


def tickboxes():
    if requirements_checkbox.value == 1:
        requirements_text.enable()
    elif requirements_checkbox.value == 0:
        requirements_text.disable()

def new_customer():
    customer_window = Window(app, title = "Add Customer", bg = (253, 71, 74), height = 750)
    picture = Picture(customer_window, image="Logo.gif")



    text = Text(customer_window, text="New Customer")
    text.text_color = "white"
    text.text_size = 20


    text = Text(customer_window, text= "First Name")
    text.text_color = "white"
    first_name = TextBox(customer_window)
    first_name.width = 15

    text = Text(customer_window, text= "Last Name")
    text.text_color = "white"
    last_name = TextBox(customer_window)
    last_name.width = 15


    text = Text(customer_window, text= "Address 1")
    text.text_color = "white"
    address1 = TextBox(customer_window)
    address1.width = 40

    text = Text(customer_window, text= "Address 2")
    text.text_color = "white"
    address2 = TextBox(customer_window)
    address2.width = 40

    text = Text(customer_window, text= "City")
    text.text_color = "white"
    city = TextBox(customer_window)
    city.width = 15

    text = Text(customer_window, text= "Post Code")
    text.text_color = "white"
    post_code = TextBox(customer_window)
    post_code.width = 15

    text = Text(customer_window, text= "Phone Number")
    text.text_color = "white"
    phone_number = TextBox(customer_window)
    phone_number.width = 25

    text = Text(customer_window, text= "Email")
    text.text_color = "white"
    email = TextBox(customer_window)
    email.width = 30

    global requirements_checkbox
    global requirements_text

    requirements_checkbox = CheckBox(customer_window, text="Special Requirements?", command=tickboxes)
    requirements_checkbox.text_color = "white"

    requirements_text = TextBox(customer_window, text="No Requirements")
    requirements_text.width = 25
    requirements_text.disable()

    customer_button = PushButton(customer_window, text="Enter", command=add_new_customer, args=[customer_window, first_name, last_name, address1, address2, post_code, city, phone_number, email, requirements_text])
    customer_button.width = 15
    customer_button.text_color = "white"

    home_button = PushButton(customer_window, text="Home", align="bottom", command=customer_window.destroy)
    home_button.width = 6
    home_button.text_color = "white"


def validEmail(email):

    regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    if(re.search(regex,email)):
        return True


    else:
        return False

def add_new_customer(customer_window, first_name, last_name, address1, address2, post_code, city, phone_number, email, requirements_text):


    print(first_name.value)
    FirstName = first_name.value
    Surname = last_name.value
    Email = email.value
    PhoneNumber = phone_number.value
    SpecialNotes = requirements_text.value


    Address1 = address1.value
    Address2 = address2.value
    City = city.value
    Postcode = post_code.value
    #<-- Validation -->

    checkEmail = validEmail(Email)

    if checkEmail:
        print("Valid Email")
    elif checkEmail == False:
        text = Text(customer_window, text= "")
        text.text_color = "white"
    try:
        cursor.execute(("""INSERT INTO Address(Address1, Address2, Postcode, City) VALUES(?, ?, ?, ?)"""),(Address1, Address2, City, Postcode))
        addressID = cursor.lastrowid
        print(addressID)
        cursor.execute(("""INSERT INTO Customer(AddressID, FirstName, Surname, Email, PhoneNumber, SpecialNotes) VALUES(?, ?, ?, ?, ?, ?)"""),(addressID, FirstName, Surname, Email, PhoneNumber, SpecialNotes))

        db.commit()
        successScreen()
    except:
        errorScreen()


def new_booking():
    showAllCustomers = []
    showAllDestinations = []

    showAllDates = []

    cursor.execute("SELECT * FROM Customer")
    result = cursor.fetchall()
    for row in result:
       showAllCustomers.append(str(row[0]) + ' ' +  str(row[2]) + ' ' + str(row[3]))
    cursor.execute("SELECT * FROM Destination")
    result2 = cursor.fetchall()
    for row in result2:
       showAllDestinations.append(str(row[0]) + ' ' +  str(row[1]))

    print(showAllCustomers)



    booking_window = Window (app, title = "Add Booking", bg = (253, 71, 74), height = 750)
    picture = Picture(booking_window, image="Logo.gif")

    text = Text(booking_window, text="Add Booking")
    text.text_color = "white"
    text.text_size = 20



    text = Text(booking_window, text="Search Customers")
    text.text_color = "white"
    bookingCustomers_combo = Combo(booking_window, options=showAllCustomers)
    bookingCustomers_combo.text_color = "white"

    global bookingDestination_combo
    global bookingDate_combo

    text = Text(booking_window, text="Search Destinations")
    text.text_color = "white"
    bookingDestination_combo = Combo(booking_window, options=showAllDestinations, command=findBookingDates)
    bookingDestination_combo.text_color = "white"


    text = Text(booking_window, text="Choose Date")
    text.text_color = "white"
    bookingDate_combo = Combo(booking_window, options=showAllDates)
    bookingDate_combo.text_color = "white"
    findBookingDates()



    text = Text(booking_window, text="Number of seats required")
    text.text_color = "white"
    booking_seatNumber = TextBox(booking_window)
    booking_seatNumber.width = 2
    booking_seatNumber.text_color = "white"

    text = Text(booking_window, text="Notes")
    text.text_color = "white"
    text_notes = TextBox(booking_window, text="No Notes", multiline=True)
    text_notes.width = 25
    text_notes.height = 3
    text_notes.text_color = "white"





    booking_button = PushButton(booking_window, text="Enter", command=add_new_booking, args=[bookingCustomers_combo, bookingDestination_combo, booking_seatNumber, text_notes, bookingDate_combo])
    booking_button.width = 15
    booking_button.text_color = "white"

    home_button = PushButton(booking_window, text="Home", align="bottom", command=booking_window.destroy)
    home_button.width = 6
    home_button.text_color = "white"


def findBookingDates():
    DestinationID = bookingDestination_combo.value.split(' ', 1)[1] #Takes the global variable of the

    cursor.execute("SELECT DateOfTrip FROM Trip INNER JOIN Destination on Destination.DestinationID = Trip.DestinationID WHERE Town =?", (DestinationID,))
    showAllDates = cursor.fetchall()
    bookingDate_combo.clear()


    showAllDates = [item[0] for item in showAllDates]
    print(showAllDates)

    datesArrayLength = len(showAllDates)
    for i in range(datesArrayLength):
        bookingDate_combo.append(showAllDates[i])


def add_new_booking(bookingCustomers_combo, bookingDestination_combo, booking_seatNumber, text_notes, bookingDate_combo):

    CustomerID = bookingCustomers_combo.value.split(' ', 1)[0] #Only takes the values before the first space which in this case is the ID
    CustomerID = int(CustomerID) #Converts CustomerID to an integer

    DestinationID = bookingDestination_combo.value.split(' ', 1)[1] #Only takes the values after the first space which in this case is the Destination Town


    SeatAmount = booking_seatNumber.value #Gets the value of the amount of seats the user has put in and then saves it as SeatAmount

    findDate = bookingDate_combo.value

    BookingDate = datetime.today().strftime('%d/%m/%y') #Gets the current date of the computer and adds it as a variable.

    Notes = text_notes.value #Gets notes from user input and saves it as the variable Notes

    cursor.execute("SELECT TripID FROM Trip INNER JOIN Destination on Destination.DestinationID = Trip.DestinationID WHERE Town =? AND DateOfTrip =?", (DestinationID,findDate)) #Find the foreign key value for the destinationID inputed by the user that's being stored in the Trip Table and gets the primary key for the trip that they have requested
    TripID = cursor.fetchall() # Grabs the value entered
    TripID = [item[0] for item in TripID] #Only gets the first element in the array removing it from the tuple
    TripID = int(TripID.pop(0)) #Takes it out of the array and concatenates the value to an integer to be saved as the TripID for this booking


    cursor.execute(("""INSERT INTO Booking(CustomerID, TripID, SeatAmount, BookingDate, Notes) VALUES(?, ?, ?, ?, ?)"""),(CustomerID, TripID, SeatAmount, BookingDate, Notes)) #Inserts all the information above into the booking table.
    db.commit() #Saves the table




def new_trip():
    showAllCoaches = []
    showAllDrivers = []
    showAllDestinations = []

    cursor.execute("SELECT * FROM Coach")
    result = cursor.fetchall()
    for row in result:
       showAllCoaches.append(str(row[0]) + ' ' +  str(row[1]) + ' Seat Count: ' + str(row[2]))

    cursor.execute("SELECT * FROM Driver")
    result2 = cursor.fetchall()
    for row in result2:
        showAllDrivers.append(str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2]))
    cursor.execute("SELECT * FROM Destination")
    result3 = cursor.fetchall()
    for row in result3:
       showAllDestinations.append(str(row[0]) + ' ' +  str(row[1]))


    trip_window = Window (app, title = "New Trip", bg = (253, 71, 74), height= 700)
    picture = Picture(trip_window, image="Logo.gif")

    text = Text(trip_window, text="Book Trip")
    text.text_color = "white"
    text.text_size = 20

    text = Text(trip_window, text="Cost per Person")
    text.text_color = "white"
    trip_cost = TextBox(trip_window)
    trip_cost.width = 7

    text = Text(trip_window, text="Date of Trip")
    text.text_color = "white"
    trip_dateOfTrip = TextBox(trip_window)
    trip_dateOfTrip.width = 10

    text = Text(trip_window, text="Days")
    text.text_color = "white"
    trip_days = TextBox(trip_window)
    trip_days.width = 3

    text = Text(trip_window, text="Search Destinations")
    text.text_color = "white"
    tripDestination_combo = Combo(trip_window, options=showAllDestinations)
    tripDestination_combo.text_color = "white"

    text = Text(trip_window, text="Coach")
    text.text_color = "white"
    coach_combo = Combo(trip_window, options=showAllCoaches)
    coach_combo.text_color = "white"

    text = Text(trip_window, text="Driver")
    text.text_color = "white"
    driver_combo = Combo(trip_window, options=showAllDrivers)
    driver_combo.text_color = "white"


    coach_button = PushButton(trip_window, text="Enter", command=add_new_trip, args=[trip_cost, trip_dateOfTrip, trip_days, tripDestination_combo, coach_combo, driver_combo])
    coach_button.width = 15
    coach_button.text_color = "white"

    home_button = PushButton(trip_window, text="Home", align="bottom", command=trip_window.destroy)
    home_button.width = 6
    home_button.text_color = "white"

def add_new_trip(trip_cost, trip_dateOfTrip, trip_days, tripDestination_combo, coach_combo, driver_combo):
    CostPerPerson = trip_cost.value
    DateOfTrip = trip_dateOfTrip.value
    Days = trip_days.value


    DestinationID = tripDestination_combo.value.split(' ', 1)[0] # Only takes in the values before the first space in the string to get the DestinationID
    DestinationID = int(DestinationID) # Converts DestinationID to integer
    CoachID = coach_combo.value.split(' ', 1)[0] # Only takes in the values before the first space in the string to get the CoachID
    CoachID = int(CoachID) # Converts CoachID to integer
    DriverID = driver_combo.value.split(' ', 1)[0] # Only takes in the values before the first space in the string to get the DriverID
    DriverID = int(DriverID) # Converts DriverID to integer

    cursor.execute(("""INSERT INTO Trip(CostPerPerson, DateOfTrip, Days, DestinationID, CoachID, DriverID) VALUES(?, ?, ?, ?, ?, ?)"""),(CostPerPerson, DateOfTrip, Days, DestinationID, CoachID, DriverID)) #Inserts all the information above into the booking table.
    db.commit() #Saves the table





def new_destination():
    destination_window = Window(app, title = "Add Destination", bg = (253, 71, 74))
    picture = Picture(destination_window, image="Logo.gif")

    text = Text(destination_window, text="New Destination")
    text.text_color = "white"
    text.text_size = 20

    text = Text(destination_window, text="Name of Town")
    text.text_color = "white"
    destination_town = TextBox(destination_window)
    destination_town.width = 25

    text = Text(destination_window, text="Name of Hotel")
    text.text_color = "white"
    destination_hotel = TextBox(destination_window, text="No Hotel")
    destination_hotel.width = 25
    destination_hotel.text_color = "white"

    destination_button = PushButton(destination_window, text="Enter", command=add_new_destination, args=[destination_town, destination_hotel])
    destination_button.width = 15
    destination_button.text_color = "white"

    home_button = PushButton(destination_window, text="Home", align="bottom", command=destination_window.destroy)
    home_button.width = 6
    home_button.text_color = "white"

def add_new_destination(destination_town, destination_hotel):
    Town = destination_town.value
    Hotel = destination_hotel.value

    cursor.execute(("""INSERT INTO Destination(Town, Hotel) VALUES(?, ?)"""), (Town, Hotel))
    db.commit()

def passenger_details():
    details_window = Window (app, title = "Passenger Details", bg = (253, 71, 74))
    picture = Picture(details_window, image="Logo.gif")

    text = Text(details_window, text="Passenger Details")
    text.text_color = "white"
    text.text_size = 20

    destination_button = PushButton(details_window, text="Ok", command=details_window.destroy)
    destination_button.width = 15
    destination_button.text_color = "white"

    cursor.execute("SELECT FirstName, Surname, SeatAmount FROM Customer INNER JOIN Booking on Booking.CustomerID =  Customer.CustomerID WHERE TripID = '8'")
    query_passengers = cursor.fetchall()

    print(query_passengers)

    try:
        with open('Passenger_Details.txt', 'w') as file:
            row = ("First Name | Surname | Amount of Seats \n\n")
            file.write(row)
            for result in query_passengers:
                row = ("%s | %s | %d \n " % (result[0], result[1], result[2]))
                file.write(row)
        text = Text(details_window, text="File Created as \n query_passengers.txt")
        text.text_color = "white"

    except:
        text = Text(details_window, text="Error, File Creation Unsuccessful")
        text.text_color = "white"



def all_trips():
    trips_window = Window(app, title="All Trips", bg = (253, 71, 74), width = 500, height = 400)
    picture = Picture(trips_window, image="Logo.gif")

    text = Text(trips_window, text="All Trips")
    text.text_color = "white"
    text.text_size = 20

    cursor.execute("SELECT Town, DateOfTrip, CostPerPerson, Days FROM Trip INNER JOIN Destination on Destination.DestinationID = Trip.DestinationID ORDER BY DateOfTrip")
    query_all_trips = cursor.fetchall()


    try:
        with open('all_trips.txt', 'w') as file:
            row = ("Town | Date Of Trip | Cost Per Person | Amount Of Days \n \n")
            file.write(row)
            for result in query_all_trips:
                row = ("%s | %s | %s | %s \n \n" % (result[0], result[1], result[2], result[3]))
                file.write(row)
        text = Text(trips_window, text="File Created as \n all_trips.txt")
        text.text_color = "white"

    except:
        text = Text(trips_window, text="Error, File Creation Unsuccessful")
        text.text_color = "white"

    ok_button = PushButton(trips_window, text="Ok", command=trips_window.destroy)
    ok_button.text_color = "white"

def customer_addresses():
    addresses_window = Window(app, title="Customer Addresses", bg = (253, 71, 74), width = 500, height = 400)
    picture = Picture(addresses_window, image="Logo.gif")

    text = Text(addresses_window, text="Customer Addresses")
    text.text_color = "white"
    text.text_size = 20

    cursor.execute("SELECT Customer.FirstName, Customer.Surname, Address1, Address2, Postcode FROM Address INNER JOIN Customer ON Customer.AddressID = Address.AddressID WHERE Postcode LIKE 'E5%'")
    query_addresses = cursor.fetchall()



    try:
        with open('customer_addresses.txt', 'w') as file:
            row = ('First Name | Surname | Address Line 1 | Address Line 2 \n \n')
            file.write(row)
            for result in query_addresses:
                row =  ("%s | %s | %s | %s \n \n" % (result[0], result[1], result[2], result[3]))
                file.write(row)
        text = Text(addresses_window, text="File Created as \n customer_addresses.txt")
        text.text_color = "white"

    except:
        text = Text(addresses_window, text="Error, File Creation Unsuccessful")
        text.text_color = "white"

    ok_button = PushButton(addresses_window, text="Ok", command=addresses_window.destroy)
    ok_button.text_color = "white"

def trip_income():
    showAllDestinations = []
    showIncomeDates = []

    cursor.execute("SELECT * FROM Destination")
    result = cursor.fetchall()
    for row in result:
       showAllDestinations.append(str(row[0]) + ' ' + str(row[1]))


    global income_window
    income_window = Window (app, title = "Passenger Details", bg = (253, 71, 74))
    picture = Picture(income_window, image="Logo.gif")

    text = Text(income_window, text="Trip Income")
    text.text_color = "white"
    text.text_size = 20

    text = Text(income_window, text="Trips")
    text.text_color = "white"

    text = Text(income_window, text="Choose a Destination")
    text.text_color = "white"
    global trips_combo
    trips_combo = Combo(income_window, options=showAllDestinations, command=get_trip_dates)
    trips_combo.text_color = "white"

    global income_dates

    income_dates = Combo(income_window, options=showIncomeDates)
    income_dates.text_color = "white"



    trip_income_box = TextBox(income_window, text="Choose a Destination")
    trip_income_box.width = 22
    trip_income_box.text_color = "white"

    get_trip_dates()


    income_button = PushButton(income_window, text="Enter", command=get_trip_income, args=[trips_combo,trip_income_box,income_dates])
    income_button.width = 15
    income_button.text_color = "white"

    back_button = PushButton(income_window, text="Back", align="bottom", command=income_window.destroy)
    back_button.width = 6
    back_button.text_color = "white"

def get_trip_dates():
    print(trips_combo.value)

    DestinationTown = trips_combo.value.split(' ', 1)[1:]
    DestinationTown = ''.join(DestinationTown)

    cursor.execute("SELECT DateOfTrip FROM Trip INNER JOIN Destination on Destination.DestinationID = Trip.DestinationID WHERE Town =?", (DestinationTown,))
    showAllDates = cursor.fetchall()
    income_dates.clear()


    showAllDates = [item[0] for item in showAllDates]
    print(showAllDates)

    datesArrayLength = len(showAllDates)
    for i in range(datesArrayLength):
        income_dates.append(showAllDates[i])

def get_trip_income(trips_combo,trip_income_box,income_dates):


    DestinationID = trips_combo.value.split(' ', 1)[:1]
    DestinationID = ''.join(DestinationID)

    DestinationTown = trips_combo.value.split(' ', 1)[1:]
    DestinationTown = ''.join(DestinationTown)
    selectDate = income_dates.value


    cursor.execute("SELECT TripID FROM Trip INNER JOIN Destination on Destination.DestinationID = Trip.DestinationID WHERE Town =? AND DateOfTrip =?", (DestinationTown,selectDate))
    TripID = cursor.fetchall()
    TripID = [item[0] for item in TripID]
    TripID = int(TripID.pop(0))
    print(TripID)

    try:
        cursor.execute("SELECT SUM(SeatAmount) FROM BOOKING WHERE TripID = ?", (TripID,))
        seatsSold = cursor.fetchall()
        seatsSold = [item[0] for item in seatsSold]
        seatsSold = int(seatsSold.pop(0))
    except:
        trip_income_box.clear()
        trip_income_box.value = 'No correlating bookings!'
        return

    cursor.execute("SELECT SUM(CostPerPerson)*? FROM Trip INNER JOIN Destination on Destination.DestinationID = Trip.DestinationID WHERE Town =?", (seatsSold, DestinationTown))
    seatsSold = cursor.fetchall()

    seatsSold = ''.join(str(e) for e in [item[0] for item in seatsSold])
    seatsSold = '£' + seatsSold

    trip_income_box.clear()
    trip_income_box.value = seatsSold




def query_data():
    query_window = Window (app, title = "Query Data", bg = (253, 71, 74), height = 550)
    picture = Picture(query_window, image="Logo.gif")

    text = Text(query_window, text="Query Data")
    text.text_color = "white"
    text.text_size = 20

    submit = PushButton(query_window, text="Passenger Details", command=passenger_details)
    submit.text_color = "white"
    submit = PushButton(query_window, text="All Trips", command=all_trips)
    submit.text_color = "white"
    submit = PushButton(query_window, text="Customer Addresses", command=customer_addresses)
    submit.text_color = "white"
    submit = PushButton(query_window, text="Trip Income", command=trip_income)
    submit.text_color = "white"

    home_button = PushButton(query_window, text="Home", align="bottom", command=query_window.destroy)
    home_button.width = 6
    home_button.text_color = "white"


app = App(title='Silver Dawn Coaches', height=550, bg = (253, 71, 74))

text = Text(app, text="Silver Dawn Coaches Customer Software")
text.text_color = "white"



picture = Picture(app, image="Logo.gif")


submit = PushButton(app, text="Add Customer", command=new_customer)
submit.text_color = "white"
submit = PushButton(app, text="Book Coach", command=new_booking)
submit.text_color = "white"
submit = PushButton(app, text="Add Trip", command=new_trip)
submit.text_color = "white"
submit = PushButton(app, text="Add Destination", command=new_destination)
submit.text_color = "white"
submit = PushButton(app, text="Query Database", command=query_data)
submit.text_color = "white"

exit_button = PushButton(app, text="Exit", align="bottom", command=app.destroy)
exit_button.width = 6
exit_button.text_color = "white"
