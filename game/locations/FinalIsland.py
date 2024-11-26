from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
from game.context import Context
import game.player as player
import random

class FinalIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Final island"
        self.symbol = 'F'
        self.visitable = True

        self.locations = {}

        self.locations["southBeach"] = ShipAtBeach(self) # Parking location

        self.locations["beached ship"] = BeachedShip(self) # Treasure and Puzzle Location

        self.locations["central square"] = CentSquare(self) # Seagull Location

        self.locations["enemy pirate crew camp"] = PirCrewCamp(self) # Enemy Encounter Location

        self.locations["pirate captain arena"] = Arena(self) # Special Enemy Location

        self.starting_location = self.locations["southBeach"]

    def enter (self, ship):
        display.announce ("You have arrived at a wartorn island.", pause=True)
        

class ShipAtBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter (self):
        display.announce ("You arrive at the beach of an island currently drenched in conflict.\n" +
                  "Your ship is at anchor in a small bay to the south.\n" +
                  "A ship was beached on this island and hostile pirate crews are present.\n" +
                  "Up ahead, you can see the central square of the island's small ghost town.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["central square"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["enemy pirate crew camp"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beached ship"]

class CentSquare (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "town square"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append (seagull.Seagull())

    def enter (self):
        description = "You arrive at the town's central square, the buildings mostly destroyed and its residents long gone."
        display.announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["enemy pirate crew camp"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["pirate captain arena"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beached ship"]
    

class BeachedShip (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beached ship"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append (ChestPuzzle())

    def enter (self):
        description = "You find yourself at a beached pirate ship, its crew absent from the scene. There is a locked chest visible inside the ship."
        display.announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["central square"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["pirate captain arena"]

class PirCrewCamp (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "enemy pirate crew camp"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append(PirateCamp())

    def enter (self):
        description = "You stumble upon a camp made by the pirates of the beached ship."
        display.announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["central square"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["pirate captain arena"]

class Arena (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "pirate captain arena"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append(PirateCaptainFight())

    def enter (self):
        description = "You arrive at a lifeless battlefield of dead pirates, in the center of it all stands the last captain."
        display.announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beached ship"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["central square"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["enemy pirate crew camp"]

class EnemyPirate(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["cutless slash"] = ["cutlass slashes",random.randrange(70,101), (10,15)]
        attacks["flintlock shot"] = ["flintlock shots",random.randrange(70,101), (8,13)]
        super().__init__(name, random.randrange(14,41), attacks, 100 + random.randrange(-40,41)) # 14-40 HP, Attacks, 110-190 Speed (100 total normal)
        self.type_name = "Enemy pirate"

class PirateCaptain(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["cutless slash"] = ["cutlass slashes",random.randrange(70,101), (10,15)]
        attacks["flintlock shot"] = ["flintlock shots",random.randrange(70,101), (8,13)]
        attacks["canon blast"] = ["canon blasts",random.randrange(70,101), (30, 51)]
        attacks["parrot peck"] = ["parrot pecks",random.randrange(70,101), (5,11)]
        super().__init__(name, 1000, attacks, 150 + random.randrange(-10,11)) # 1000-1100 HP?, Attacks, 140-160 Speed
        self.type_name = "Enemy pirate"

class PirateCamp (event.Event):
    '''
    A combat encounter with a stranded crew of pirates inhabiting a camp.
    When the event is drawn, creates a combat encounter with 4 to 7 enemy pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " enemy pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with enemy pirates.'''
        result = {}
        result["message"] = "The pirates are defeated!"
        monsters = []
        min = 4
        uplim = 7
        monsters.append(EnemyPirate("Stranded Enemy Pirate"))
        self.type_name = ""
        monsters[0].health = 3*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(EnemyPirate("Stranded Enemy Pirate "+str(n)))
            n += 1
        display.announce ("You are attacked by a crew of pirates!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
    
class PirateCaptainFight (event.Event):
    '''
    A combat encounter with a pirate captain.
    When the event is drawn, creates a combat encounter with 1 pirate captain, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " enemy pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with a pirate captain.'''
        result = {}
        result["message"] = "The pirate captain is defeated!"
        monsters = []
        monsters.append(EnemyPirate("Enemy Pirate Captain"))
        monsters[0].health = 7*monsters[0].health
        #n += 1
        display.announce ("You are attacked by a lone pirate captain!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
    
class Musket(item.Item):
    def __init__(self):
        super().__init__("musket", 500) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20,150)
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"


class ChestPuzzle (Context, event.Event):
    def __init__ (self):
        super().__init__()
        self.name = " locked chest"
        self.verbs['open'] = self
        self.verbs['leave'] = self
        self.go = False
        self.result = {}
        self.item_in_chest = Musket()


    def process(self, sublocation):
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "You leave the now empty chest."
        self.sublocation = sublocation

        display.announce(f"Before you stands a locked chest, will you attempt to open the chest or leave it?", pause=False)
        player.Player.get_interaction ([self])

        return self.result

    def process_verb (self, verb, cmd_list, nouns):
        if verb == "leave":
            self.result["message"] = "You leave the chest."
            config.the_player.next_loc = self.sublocation.main_location.locations["central square"]
            config.the_player.go = True

        elif verb == "open":
            lockcount = 0
            num1 = random.randint(1, 3)
            num2 = random.randint(1, 6)
            num3 = random.randint(1, 9)
            if lockcount == 0:
                guess = 0
                while guess != num1:
                    guess = int(input("Enter a number from 1 to 3 to attempt to pick the lock: "))
                    if (guess < num1) or (guess > num1):
                        print("The lock did not budge.")
                    if guess == num1:
                        print("You unlocked the first lock.")
                        lockcount += 1
            
            if lockcount == 1:
                guess = 0
                while guess != num2:
                    guess = int(input("Enter a number from 1 to 6 to attempt to pick the lock: "))
                    if (guess < num2) or (guess > num2):
                        display.announce ("The lock did not budge.")
                    if guess == num2:
                        display.announce ("You unlocked the second lock.")
                        lockcount += 1

            if lockcount == 2:
                guess = 0
                while guess != num3:
                    guess = int(input("Enter a number from 1 to 9 to attempt to pick the lock: "))
                    if (guess < num3) or (guess > num3):
                        display.announce ("The lock did not budge.")
                    if guess == num3:
                        display.announce ("You unlocked the final lock.")
                        lockcount += 1
                
            if lockcount == 3:
                display.announce ("The chest was successfully unlocked, inside it lies a fancy and powerful-looking musket.")
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_chest
                #if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                display.announce(f"You take the {item.name} from the chest.")
                config.the_player.add_to_inventory([item])
                self.item_in_chest = None
                config.the_player.go = True
                at_least_one = True
                self.result["newevents"] = [ ]