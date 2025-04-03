
# This is the Player class, where all of the information for each player is created
class Player:
    def __init__(self, playerNum, panel, pieceID=None, position=None, clues_found=None):
        '''
        The following is a list of what information we need about each player:
        1. Player number -> playerNum, assigned upon creation
        2. Panel number -> panel, assigned upon creation
        3. The piece that the player is using -> pieceID, assigned during player's first move (we want the choice of what piece the player uses to be natural)
        4. Player position -> position, assigned upon player's first move, after discovering assiened pieceID
        5. List of clues found -> clues_found, initially empty 
        '''
        self.pieceID = pieceID  # The piece the player is using
        self.position = position  # Tracks the player's current position on the board
        self.clues_found = []  # List of clues collected by the player
        self.panel = panel  # The LED panel assigned to the player
        #self.panel_leds_lit = []  # List of LEDs lit on the panel (I don't think this is needed)

    def assign_panel(self, panel):
        """Assign a panel to the player."""
        self.panel = panel

    def set_piece(self, piece):
        """Set the player's piece after the first move."""
        if self.pieceID is None:  # Piece can only be set once
            self.pieceID = piece


    def add_clue(self, clue):
        """Add a clue (integer) to the player's list of cluesFound and update the panel."""
        self.clues_found.append(clue)
        self.update_panel()

    def move(self, new_position):
        """Update the player's position."""
        self.position = new_position
        self.update_panel()  # Light up the new position on the panel

    def update_position(self, new_position=None):
        """
        Move the player to a new position and update the panel.
        :param new_position: The new position to move to, optional if using sensor_reader.
        """
        if new_position is not None:
            self.position = new_position
        else:
            print("Error: No new position provided.")
        
        self.update_panel()  # Update the LED panel after moving

    def get_position(self):
        """Get the player's current position."""
        return self.position

    def update_panel(self):
        """Update the player's panel by lighting up the player's current position."""
        if self.panel is not None:
            # Ensure we only light up the player's position on the panel
            if self.position not in self.panel_leds_lit:
                self.panel_leds_lit.append(self.position)
                # Light up the position on the panel
                self.panel.lightLED(self.position)
        else:
            print("No panel assigned to this player.")

    def display_panel_status(self):
        """Display the status of the player's panel."""
        print(f"Player {self.pieceID}'s panel LEDs: {self.panel_leds_lit}")

    def __str__(self):
        return f"Player {self.pieceID} is at position {self.position} with clues {self.clues_found}"