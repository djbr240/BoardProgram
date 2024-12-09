#code for clue game panels
#future plans: change "pixels" to "panel?" for each panel
#              change all variables, copy, undo, then paste to save time
#
#              only run for each panel if it is that players turn
#last edit:
#           Instead of using a counter there is a variable that is
#           now set to 1 when the correct item in a category has been found



from machine import Pin  # Import Pin class from machine module
import neopixel
from utime import sleep
import urandom  # For generating random values

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 26
pin = Pin(21, Pin.OUT)

pixels = neopixel.NeoPixel(pin, num_pixels)

brightness = 50

playerturn = True

person = 0
toy = 0
time = 0

mustard = 0

scarlett = 0

green = 0

peacock = 0

orchid = 0

plum = 0

rex = 0

car = 0

bear = 0

potato = 0

xylophone = 0

ball = 0

pool = 0

desk = 0

chair = 0

piano = 0

plant = 0

dining = 0

time11 = 0

time12 = 0

time1 = 0

time2 = 0

time3 = 0

time4 = 0

time5 = 0

while True:
    # if it is players turn, light up top LED blue
    if (playerturn == True):
        pixels[25] = (0,0,brightness)

    # input the selected items number
    itemasstring = input("what is the item number")
    item = int(itemasstring)

    # The following will initialize the game
    # Set all item variables to 0
    # Turn off all LED's
    # Reset person toy and time to 0
    if (item == 0):

        person = 0
        toy = 0
        time = 0

        mustard = 0

        scarlett = 0

        green = 0

        peacock = 0

        orchid = 0

        plum = 0

        rex = 0

        car = 0

        bear = 0

        potato = 0

        xylophone = 0

        ball = 0

        pool = 0

        desk = 0

        chair = 0

        piano = 0

        plant = 0

        dining = 0

        time11 = 0

        time12 = 0

        time1 = 0

        time2 = 0

        time3 = 0

        time4 = 0

        time5 = 0

        pixels.fill ((0,0,0))


    # Check the input and set corresponding 
    # piece to 1 if correct person has not been found
    if (item == 1 and person == 0):
        mustard = 1

    if (item == 2 and person == 0):
        scarlett = 1

    if (item == 3 and person == 0):
        green = 1

    if (item == 4 and person == 0):
        peacock = 1

    if (item == 5 and person == 0):
        orchid = 1

    if (item == 6 and person == 0):
        plum = 1

    # Check the input and set corresponding 
    # piece to 1 if correct toy has not been found
    if (item == 7 and toy == 0):
        rex = 1

    if (item == 8 and toy == 0):
        car = 1

    if (item == 9 and toy == 0):
        bear = 1

    if (item == 10 and toy == 0):
        potato = 1

    if (item == 11 and toy == 0):
        xylophone = 1

    if (item == 12 and toy == 0):
        ball = 1

    if (item == 13):
        pool = 1

    if (item == 14):
        desk = 1

    if (item == 15):
        chair = 1

    if (item == 16):
        piano = 1

    if (item == 17):
        plant = 1

    if (item == 18):
        dining = 1

    # Check the input and set corresponding 
    # piece to 1 if correct time has not been found
    if (item == 19 and time == 0):
        time11 = 1

    if (item == 20 and time == 0):
        time12 = 1

    if (item == 21 and time == 0):
        time1 = 1

    if (item == 22 and time == 0):
        time2 = 1

    if (item == 23 and time == 0):
        time3 = 1

    if (item == 24 and time == 0):
        time4 = 1

    if (item == 25 and time == 0):
        time5 = 1


    # The following lights up each corresponding LED red
    # depending on if the item is set to 1

    if (mustard == 1):
        pixels[19] = (brightness,0,0)

    if (scarlett == 1):
        pixels[20] = (brightness,0,0)

    if (green == 1):
        pixels[21] = (brightness,0,0)

    if (peacock == 1):
        pixels[22] = (brightness,0,0)

    if (orchid == 1):
        pixels[23] = (brightness,0,0)

    if (plum == 1):
        pixels[24] = (brightness,0,0)

    if (rex == 1):
        pixels[18] = (brightness,0,0)

    if (car == 1):
        pixels[17] = (brightness,0,0)

    if (bear == 1):
        pixels[16] = (brightness,0,0)

    if (potato == 1):
        pixels[15] = (brightness,0,0)

    if (xylophone == 1):
        pixels[14] = (brightness,0,0)

    if (ball == 1):
        pixels[13] = (brightness,0,0)

    if (pool == 1):
        pixels[7] = (brightness,0,0)

    if (desk == 1):
        pixels[8] = (brightness,0,0)

    if (chair == 1):
        pixels[9] = (brightness,0,0)

    if (piano == 1):
        pixels[10] = (brightness,0,0)

    if (plant == 1):
        pixels[11] = (brightness,0,0)

    if (dining == 1):
        pixels[12] = (brightness,0,0)

    if (time11 == 1):
        pixels[6] = (brightness,0,0)

    if (time12 == 1):
        pixels[5] = (brightness,0,0)

    if (time1 == 1):
        pixels[4] = (brightness,0,0)

    if (time2 == 1):
        pixels[3] = (brightness,0,0)

    if (time3 == 1):
        pixels[2] = (brightness,0,0)

    if (time4 == 1):
        pixels[1] = (brightness,0,0)

    if (time5 == 1):
        pixels[0] = (brightness,0,0)


    # The following lights the LED green
    # when it is the last person left
    # and sets person to 1 to block previous code from making it red

    if (mustard==0 and scarlett==1 and green==1 and peacock==1 and orchid==1 and plum==1):
        pixels[19] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==0 and green==1 and peacock==1 and orchid==1 and plum==1):
        pixels[20] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==0 and peacock==1 and orchid==1 and plum==1):
        pixels[21] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==1 and peacock==0 and orchid==1 and plum==1):
        pixels[22] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==1 and peacock==1 and orchid==0 and plum==1):
        pixels[23] = (0,brightness,0)
        person = 1

    if (mustard==1 and scarlett==1 and green==1 and peacock==1 and orchid==1 and plum==0):
        pixels[24] = (0,brightness,0)
        person = 1


    # The following lights the LED green
    # when it is the last toy left
    # and sets toy to 1 to block previous code from making it red
    if (rex==0 and car==1 and bear==1 and potato==1 and xylophone==1 and ball==1):
        pixels[18] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==0 and bear==1 and potato==1 and xylophone==1 and ball==1):
        pixels[17] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==0 and potato==1 and xylophone==1 and ball==1):
        pixels[16] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==1 and potato==0 and xylophone==1 and ball==1):
        pixels[15] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==1 and potato==1 and xylophone==0 and ball==1):
        pixels[14] = (0,brightness,0)
        toy = 1

    if (rex==1 and car==1 and bear==1 and potato==1 and xylophone==1 and ball==0):
        pixels[13] = (0,brightness,0)
        toy = 1


    # The following lights the LED green
    # when it is the last time left
    # and sets time to 1 to block previous code from making it red
    if (time11==0 and time12==1 and time1==1 and time2==1 and time3==1 and time4==1 and time5==1):
        pixels[6] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==0 and time1==1 and time2==1 and time3==1 and time4==1 and time5==1):
        pixels[5] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==0 and time2==1 and time3==1 and time4==1 and time5==1):
        pixels[4] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==0 and time3==1 and time4==1 and time5==1):
        pixels[3] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==1 and time3==0 and time4==1 and time5==1):
        pixels[2] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==1 and time3==1 and time4==0 and time5==1):
        pixels[1] = (0,brightness,0)
        time = 1

    if (time11==1 and time12==1 and time1==1 and time2==1 and time3==1 and time4==1 and time5==0):
        pixels[0] = (0,brightness,0)
        time = 1

    #playerturn = False

    item = 100
    pixels.write()  # Send the data to the NeoPixels
    sleep(0.1)  # Delay before updating colors again