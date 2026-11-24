import random


class Ability:
    """Habilidade de um semideus."""

    def __init__(self, name, cost, power, required_level):
        self.name = name
        self.cost = cost
        self.power = power
        self.required_level = required_level


class Entity:
    """Classe base: tudo que luta tem nome, vida, ataque, defesa e velocidade."""

    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        real_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - real_damage)
        return real_damage


class Demigod(Entity):
    """Semideus jogável. Herda de Entity e adiciona linhagem, energia e habilidades."""

    def __init__(self, name, god, title, element, hp, energy, attack, defense, speed):
        super().__init__(name, hp, attack, defense, speed)
        self.god = god
        self.lineage = "Filho de " + god
        self.title = title
        self.element = element
        self.energy = energy
        self.level = 1
        self.perk = ""
        self.abilities = []

    def unlocked_abilities(self):
        result = []
        for ability in self.abilities:
            if ability.required_level <= self.level:
                result.append(ability)
        return result

    def basic_attack(self, target):
        return target.take_damage(self.attack)


class ChildOfZeus(Demigod):
    """Filho de Zeus: tem chance de acerto crítico."""

    def __init__(self, name):
        super().__init__(name, "Zeus", "Mestre dos Raios", "Elétrico", 110, 80, 28, 12, 16)
        self.perk = "Tempest Surge: chance de acerto crítico nos ataques."
        self.abilities = [
            Ability("Raio Celeste", 15, 14, 1),
            Ability("Cadeia de Relâmpagos", 25, 24, 1),
            Ability("Fúria do Olimpo", 40, 40, 3),
        ]

    def basic_attack(self, target):
        damage = self.attack
        if random.random() < 0.25:
            damage = damage * 2
        return target.take_damage(damage)


class ChildOfPoseidon(Demigod):
    """Filho de Poseidon: recebe menos dano."""

    def __init__(self, name):
        super().__init__(name, "Poseidon", "Senhor dos Mares", "Aquático", 145, 70, 22, 18, 11)
        self.perk = "Oceanic Vitality: reduz o dano recebido."
        self.abilities = [
            Ability("Jato d'Água", 12, 12, 1),
            Ability("Maremoto", 25, 22, 1),
            Ability("Tridente Abissal", 40, 36, 3),
        ]

    def take_damage(self, damage):
        reduced = int(damage * 0.9)
        return super().take_damage(reduced)


class ChildOfHades(Demigod):
    """Filho de Hades: rouba vida quando ataca."""

    def __init__(self, name):
        super().__init__(name, "Hades", "Rei do Submundo", "Sombrio", 125, 85, 26, 14, 13)
        self.perk = "Death's Embrace: rouba 25% do dano causado."
        self.abilities = [
            Ability("Toque Sombrio", 14, 13, 1),
            Ability("Chamado dos Mortos", 28, 24, 1),
            Ability("Eclipse do Submundo", 42, 38, 3),
        ]

    def basic_attack(self, target):
        damage = super().basic_attack(target)
        self.hp = min(self.max_hp, self.hp + int(damage * 0.25))
        return damage


class Enemy(Entity):
    """Criatura mitológica. É o modelo usado no CRUD do Bestiário."""

    def __init__(self, name, title, hp, attack, defense, speed, xp, id=None):
        super().__init__(name, hp, attack, defense, speed)
        self.id = id
        self.title = title
        self.xp = xp

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
            "xp": self.xp,
        }