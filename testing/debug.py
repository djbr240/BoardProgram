# The LED position for the clue panels
cluePanelLED = {
    #characters
    "yellow": 19,
    "red": 20,
    "green": 21,
    "blue": 22,
    "pink": 23,
    "purple": 24,

    #toys
    "trex": 18,
    "racecar": 17,
    "teddybear": 16,
    "mr_potatohead": 15,
    "xylophone": 14,
    "ball": 13,

    #furniture
    "pooltable": 7,
    "desk": 8,
    "chair": 9,
    "piano": 10,
    "plant": 11,
    "diningtable": 12,

    #time
    "11": 6,
    "12": 5,
    "1": 4,
    "2": 3,
    "3": 2,
    "4": 1,
    "5": 0
}



while True:
    # Get user input
    userinput = input("Enter the piece: ")

    # Fetch the corresponding position from the dictionary
    if userinput in cluePanelLED:
        print(f"The {userinput} piece is at position {cluePanelLED[userinput]}")
    else:
        print("Invalid input. Please enter a valid name from the dictionary.")