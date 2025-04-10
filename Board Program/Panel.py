# from config import *
# from main import *

class Panel:
    def __init__(self, panelID):
        self.panelID = panelID

    def lightLED(clue, panelID):
        ledPos = cluePanelLED.get(clue, None)
        print(ledPos)

        # Get potentiometer position from the mux
        for i, pin in enumerate(MUX_select_pins):
            pin.value((panelID >> i) & 1)  # Set the pin value based on the channel bits
        
        #Check the reading of the potentiometer from the mux
        adc_value = ADC0_MUX.read_u16()  # Read ADC 
        percentage = (adc_value / 65535) * 100 # convert to percent 
        brightness = readPotentiometer(panelID)
        color = LED_COLORS("White")
        apply_brightness = tuple(int(c * brightness) for c in LED_COLORS("White"))
        panel[panelID][ledPos] = apply_brightness
        panel[panelID].write()

    def turn_off(panelID):
        panel[panelID] = (0, 0, 0)
        panel[panelID].write()

    def test_panel(panelID):
        # Turn on all the LEDs on the panel for 2 seconds and then turn them off
        panel[panelID] = (255, 255, 255)
        panel[panelID].write()
        sleep(2)
        panel[panelID] = (0, 0, 0)
        panel[panelID].write()

    # TODO: This hasn't been tested. Not sure if this would work.
    # This function will read the states of the first 6 pins from the fourth PCF board. Return the panel number corresponding to that panel.
    def detectPanels():
        detectedPanels = []
        for pin in range(6):
            # Read the state of the current pin
            state = read_pcf()[pin + 58]
            # If the pin is high, it means a panel is present
            if state:
                detectedPanels.append(pin + 1)
                print(f"Panel {pin + 1} detected")
        return detectedPanels
    
    