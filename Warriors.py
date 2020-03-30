class Warrior:
    def __init__(self, name, health=50, attack=5):
        self.health = health
        self.attack = attack
        self.name = name

    @ property
    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False


class Knight(Warrior):
    def __init__(self, name):
        self.name = name
        super().__init__(attack=7, name=self.name)


def fight_to_death(unit_1, unit_2):
    while True:
        unit_2.health -= unit_1.attack
        print(f'{unit_2.name}\'s health = {unit_2.health}')
        if unit_2.health > 0:
            unit_1.health -= unit_2.attack
            print(f'{unit_1.name}\'s health = {unit_1.health}')
            if unit_1.health > 0:
                continue
            else:
                print(f'{unit_2.name} wins!')
                return False
        else:
            print(f'{unit_1.name} wins!')
            return True


carl = Warrior('Carl')
bruce = Knight('Bruce')
fight_to_death(carl, bruce)
