"""
Assignment for the University of Bath as part of MSc in Artificial Intelligence

Welcome to my Enigma Machine Simulator!

The machine is set up in a modular way, with each module represented by a class and combining to form the complete
Enigma machine. There are a few points which may be helpful to explain what I am trying to achieve:

- PlugLeads - simply take a mapping of 2 letters and swap their values

- Plugboard - houses PlugLeads

- Rotors - I have used this class to capture both rotors and reflectors. In my implementation, a rotor contains an
            attribute called self.connections which is a list of mappings from one letter to another, defined by the
            rotors wiring. Rotors can rotate, which I have implemented by shifting the self.connections list forwards
            the relative indexes of letters are then used to map letters across various rotors. Ring settings and
            initial positions both work in the same way (by defining the inital order of self.connections). Notches are
            modelled seperately as numbers to account for the difference between ring setting (which doesn't change
            notch position), and initial position (which does).

- RotorCombination - Houses up to 4 rotors and a reflector

- Enigma - Houses the Plugboard and the RotorCombination. Unlike the Rotor and PlugLead classes, which can only encode
            a single letter, the enigma class encode function inputs and outputs a string of uppercase letters.
"""
class PlugLead:

    def __init__(self, mapping):
        self.character1 = mapping[0]
        self.character2 = mapping[1]
        if self.character1 == self.character2:
            raise ValueError("Letters cannot connect to themselves!")

    def encode(self, character):
        if character == self.character1:
            return self.character2
        elif character == self.character2:
            return self.character1
        else:
            return character


class Plugboard:

    def __init__(self):
        self.connections = set()

    def add(self, pluglead):
        if type(pluglead) != PlugLead:
            raise ValueError("You can only add plug leads to the plugboard")
        if len(self.connections) >= 10:
            raise ValueError("There are already 10 plug leads in the plugboard")
        for item in self.connections:
            if item.character1 == pluglead.character1 or item.character1 == pluglead.character2 or \
                    item.character2 == pluglead.character1 or item.character2 == pluglead.character2:
                raise ValueError("One or more letters already connected")
        self.connections.add(pluglead)

    def encode(self, character):
        for item in self.connections:
            character = item.encode(character)
        return character


class Rotor:

    def __init__(self, name, initial_position="A", ring_setting=1):
        self.name = name
        self.connections = []
        if name == "Beta":
            string = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
            self.notch = 30
        elif name == "Gamma":
            string = "FSOKANUERHMBTIYCWLQPZXVGJD"
            self.notch = 30
        elif name == "I":
            string = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            self.notch = 16
        elif name == "II":
            string = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
            self.notch = 4
        elif name == "III":
            string = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
            self.notch = 21
        elif name == "IV":
            string = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
            self.notch = 9
        elif name == "V":
            string = "VZBRGITYUPSDNHLXAWMJQOFECK"
            self.notch = 25
        elif name == "A":
            string = "EJMZALYXVBWFCRQUONTSPIKHGD"
            self.notch = 30
        elif name == "B":
            string = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
            self.notch = 30
        elif name == "C":
            string = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
            self.notch = 30
        else:
            raise ValueError("Invalid Rotor name")
        i = 0
        for char in string:
            mapping = [chr(65+i), char]
            self.connections.append(mapping)
            i += 1


        # Initial Position

        if ord(initial_position) not in range(65,91):
            raise ValueError("Initial Positions must be a single letter A - Z")
        else:
            offset = ord(initial_position) - ord("A")
            self.connections = self.connections[offset:] + self.connections[:offset]
            if self.notch < 30:
                self.notch -= offset
                if self.notch < 0:
                    self.notch = 26 + self.notch


        # Ring Setting:

        if ring_setting not in range(1, 27):
            raise ValueError("Ring settings must be integers between 1 and 26")
        if ring_setting != 1:
            self.connections = self.connections[(27 - ring_setting):] + self.connections[:(27 - ring_setting)]

        # Letter Encoding:

    def encode_right_to_left(self, character):
        temp = ""
        for mapping in self.connections:
            if mapping[0] == character:
                temp = mapping[1]
        character = temp
        return character


    def encode_left_to_right(self, character):
        temp = ""
        for mapping in self.connections:
            if mapping[1] == character:
                temp = mapping[0]
        character = temp
        return character

    def rotate(self):
        self.connections = self.connections[1:] + [self.connections[0]]
        if self.notch < 30:
            self.notch -= 1



class RotorCombination:
    def __init__(self, number_of_rotors):
        self.contents = []
        self.number_of_rotors = number_of_rotors

    def add_rotor_left_to_right(self, rotor):

        if type(rotor) != Rotor:
            raise ValueError("You can only add rotors or reflectors")

        if self.contents == []:
            if rotor.name != "A":
                if rotor.name != "B":
                    if rotor.name != "C":
                        raise ValueError("You must add a reflector in the leftmost position")


        if len(self.contents) == 1:
            if rotor.name == "A" or rotor.name == "B" or rotor.name == "C":
                raise ValueError("You can only add 1 reflector")

        if self.number_of_rotors == 3:
            if len(self.contents) == 4:
                raise ValueError("There is no more space for rotors")

        if len(self.contents) == 5:
            raise ValueError("There is no more space for rotors")

        self.contents.append(rotor)

    def remove_rotors(self):
        self.contents = []

    def encode(self, character):

        if len(self.contents) != 4:
            if len(self.contents) != 5:
                raise ValueError("You must only use 3 or 4 rotors plus 1 reflector")

        character_index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(character)
        rotor1 = self.contents[-1]
        rotor2 = self.contents[-2]
        rotor3 = self.contents[-3]
        if self.number_of_rotors == 3:
            reflector = self.contents[-4]
        elif self.number_of_rotors == 4:
            rotor4 = self.contents[-4]
            reflector = self.contents[-5]


        # Rotating of the Rotors:

        if rotor2.notch == 0:
            rotor3.rotate()
            rotor2.rotate()

        if rotor1.notch == 0:
            if rotor2.notch != -1:
                rotor2.rotate()

        rotor1.rotate()

        if rotor1.notch < 0:
            rotor1.notch = 26 + rotor1.notch

        if rotor2.notch < 0:
            rotor2.notch = 26 + rotor2.notch


        # encoding right to left

        character = rotor1.connections[character_index][0]
        character = rotor1.encode_right_to_left(character)
        for mapping in rotor1.connections:
            if mapping[0] == character:
                character_index = rotor1.connections.index(mapping)

        character = rotor2.connections[character_index][0]
        character = rotor2.encode_right_to_left(character)
        for mapping in rotor2.connections:
            if mapping[0] == character:
                character_index = rotor2.connections.index(mapping)

        character = rotor3.connections[character_index][0]
        character = rotor3.encode_right_to_left(character)
        for mapping in rotor3.connections:
            if mapping[0] == character:
                character_index = rotor3.connections.index(mapping)

        if self.number_of_rotors == 4:
            character = rotor4.connections[character_index][0]
            character = rotor4.encode_right_to_left(character)
            for mapping in rotor4.connections:
                if mapping[0] == character:
                    character_index = rotor4.connections.index(mapping)

        character = reflector.connections[character_index][0]
        character = reflector.encode_right_to_left(character)
        for mapping in reflector.connections:
            if mapping[0] == character:
                character_index = reflector.connections.index(mapping)


        # encoding left to right

        if self.number_of_rotors == 4:
            character = rotor4.connections[character_index][1]
            character = rotor4.encode_left_to_right(character)
            for mapping in rotor4.connections:
                if mapping[1] == character:
                    character_index = rotor4.connections.index(mapping)

        character = rotor3.connections[character_index][1]
        character = rotor3.encode_left_to_right(character)
        for mapping in rotor3.connections:
            if mapping[1] == character:
                character_index = rotor3.connections.index(mapping)

        character = rotor2.connections[character_index][1]
        character = rotor2.encode_left_to_right(character)
        for mapping in rotor2.connections:
            if mapping[1] == character:
                character_index = rotor2.connections.index(mapping)

        character = rotor1.connections[character_index][1]
        character = rotor1.encode_left_to_right(character)
        for mapping in rotor1.connections:
            if mapping[1] == character:
                character_index = rotor1.connections.index(mapping)

        character = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[character_index]

        return character




class Enigma:

    def __init__(self, plugboard, rotorcombination):
        self.plugboard = plugboard
        self.rotorcombination = rotorcombination
        if type(self.plugboard) != Plugboard or type(self.rotorcombination) != RotorCombination:
            raise ValueError("You must initialise with exactly 1 plugboard and 1 rotor combination")

    def encode(self, string):
        out_string = ""
        for character in string:
            character = self.plugboard.encode(character)
            character = self.rotorcombination.encode(character)
            character = self.plugboard.encode(character)
            out_string += character
        return out_string






if __name__ == "__main__":

    # Enigma Test

    test_plugboard = Plugboard()
    test_plugboard.add(PlugLead("HL"))
    test_plugboard.add(PlugLead("MO"))
    test_plugboard.add(PlugLead("AJ"))
    test_plugboard.add(PlugLead("CX"))
    test_plugboard.add(PlugLead("BZ"))
    test_plugboard.add(PlugLead("SR"))
    test_plugboard.add(PlugLead("NI"))
    test_plugboard.add(PlugLead("YW"))
    test_plugboard.add(PlugLead("DG"))
    test_plugboard.add(PlugLead("PK"))

    test_combination7 = RotorCombination(3)
    test_combination7.add_rotor_left_to_right(Rotor("B"))
    test_combination7.add_rotor_left_to_right(Rotor("I","A",1))
    test_combination7.add_rotor_left_to_right(Rotor("II","A",1))
    test_combination7.add_rotor_left_to_right(Rotor("III","Z",1))

    test_enigma = Enigma(test_plugboard, test_combination7)

    if test_enigma.encode("HELLOWORLD") == "RFKTMBXVVW":
        print("Implementation successful")
    else:
        print("Issue detected")








