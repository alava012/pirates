from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random

class FinalIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Final island"
        self.symbol = 'F'
        self.visitable = True

        self.locations = {}

        self.locations["southBeach"] = ShipAtBeach(self)

        #self.locations["beached ship"] = BeachedShip(self) #Treasure and Puzzle Location

        self.locations["central square"] = CentSquare(self) # Location

        self.locations["enemy pirate crew camp"] = PirCrewCamp(self) #Encounter Location

        self.locations["pirate captain arena"] = Arena(self) #Boss Location

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

    def enter (self):
        description = "You find yourself at a beached pirate ship, its crew absent from the scene."
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
    #petemade = False
    '''
    A combat encounter with a stranded crew of pirates inhabiting a camp.
    When the event is drawn, creates a combat encounter with 4 to 7 enemy pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " enemy pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with enemy pirates.'''
        result = {}
        result["message"] = "the pirates are defeated!"
        monsters = []
        min = 4
        uplim = 7
        #if not ShorePirates.petemade:
        #ShorePirates.petemade = True
        #min = 1
        #uplim = 5
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
    #petemade = False
    '''
    A combat encounter with a pirate captain.
    When the event is drawn, creates a combat encounter with 1 pirate captain, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " enemy pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with a pirate captain.'''
        result = {}
        result["message"] = "the pirate captain is defeated!"
        monsters = []
        monsters.append(EnemyPirate("Enemy Pirate Captain"))
        monsters[0].health = 7*monsters[0].health
        #n += 1
        display.announce ("You are attacked by a lone pirate captain!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
    
''' 
class ChestPuzzle (event.Event):
    def __init__ (self):
        self.name = " locked chest"
        self.verbs["open chest"] = self
        self.verbs["leave"] = self
        self.verbs["continue"] = self
    
    def process(self, world):
        result = {}

'''

class Musket(item.Item):
    def __init__(self):
        super().__init__("musket", 235) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20,150)
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"