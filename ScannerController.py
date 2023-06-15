import time
import random
from Model import *
from Button import *
from Counters import *
from Displays import *
from Lights import *

class Product:
   """Represents a product with a name, SKU, and expiration date."""
   def __init__(self, name, sku, expiration_date):
        self.name = name
        self.sku = sku
        self.expiration_date = expiration_date

products = [
    Product('Apple', '123456789', '2023-06-20               '),
    Product('Banana', '987654321', '2023-06-15               '),
    Product('Orange', '456789123', '2023-06-18               '),
    Product('Tomato', '789123456', '2023-06-22               '),
    Product('Broccoli', '321987654', '2023-06-17             ')
]

class Scanner:
# Simulates a scanner for reading product info or barcodes
    def scanBarcode(self, prompt='Scan code: ') -> str:
        return input(prompt)

class ScannerController:
# Controller to interact with the scanner, model, button, display, and lights.
    def __init__(self):

        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._button = Button(0, "transitionButton", buttonhandler=None)
        self._timer = SoftwareTimer(None)
        self._display = LCDDisplay(sda=20, scl=21, i2cid=0)
        self._scanner = Scanner()
        self._ledLight1 = Light(9, "ScannedLight1")
        self._ledLight2 = Light(13, "ScannedLight2")

        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = Model(3, self, debug=True)

        # Up to 4 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button)
        # add other buttons (up to 3 more) if needed

        # Add any timer you have.
        self._model.addTimer(self._timer)

        # Now add all the transitions that are supported by my Model
        # obviously, you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT

        # some examples:
        self._model.addTransition(0, BTN1_PRESS, 1)
        self._model.addTransition(1, TIMEOUT, 2)
        self._model.addTransition(2, BTN1_PRESS, 0)
        # etc.

    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """

    def run(self):
       
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """

    def stateDo(self, state):

        # Now if you want to do different things for each state you can do it:
        if state == 0:
            # State 0 do/actions
            pass

        elif state == 1:
           # barcode = self._scanner.scanBarcode()
           # print(f'Code scanned is {barcode}')
           pass

        elif state == 2:
            barcode = self._scanner.scanBarcode()
            print(f'Code scanned is {barcode}')
            for product in products:
                found = False
                if barcode == product.sku:
                    self._display.showText(product.expiration_date)
                    found = True
                    self._ledLight1.on()
                    self._ledLight2.off()
                    break
            if not found:
                self._display.showText("No data available")
                self._ledLight1.off()
                self._ledLight2.on()
                        

    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """

    def stateEntered(self, state):
        # Again if statements to do whatever entry/actions you need
        if state == 0:
            # entry actions for state 0
            print('State 0 entered')
            self._display.reset()
            self._ledLight1.off()
            self._ledLight2.off()

        elif state == 1:
            # entry actions for state 1
            
            print('retrieving IMS data')
            self._display.showText("retrieving IMS data")
            self._timer.start(3)

        elif state == 2:
        
            print('Completed')
    
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick

    This is just like stateEntered, perform only exit/actions here
    """

    def stateLeft(self, state):
        pass



