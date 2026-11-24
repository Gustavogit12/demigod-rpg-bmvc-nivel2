class Ability:
    def __init__(self, name, energy_cost, damage_multiplier, description):
        self.name = name
        self.energy_cost = energy_cost
        self.damage_multiplier = damage_multiplier
        self.description = description


class Entity:
    def __init__(self, name, max_hp, attack, defense, speed):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed


class Demigod(Entity):
    def __init__(self, name, godly_parent, max_hp, max_energy, attack, defense, speed, level=1):
        super().__init__(name, max_hp, attack, defense, speed)
        self.godly_parent = godly_parent
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.level = level
        self.abilities = []

    def scale_to_level(self, new_level):
        diff = new_level - self.level
        self.level = new_level
        self.max_hp += diff * 15
        self.current_hp = self.max_hp
        self.max_energy += diff * 10
        self.current_energy = self.max_energy
        self.attack += diff * 4
        self.defense += diff * 3
        self.speed += diff * 2


class ChildOfZeus(Demigod):
    def __init__(self, name, level=1):
        super().__init__(name, "Zeus", max_hp=110, max_energy=100, attack=24, defense=14, speed=22)
        self.lore = "Domínio sobre raios e ventos; alto ataque e velocidade inicial."
        self.abilities = [
            Ability("Raio Celestial", 30, 1.8, "Descarga elétrica de alto impacto."),
            Ability("Corrente de Vento", 15, 1.2, "Rajada rápida com boa iniciativa.")
        ]
        if level > 1:
            self.scale_to_level(level)


class ChildOfPoseidon(Demigod):
    def __init__(self, name, level=1):
        super().__init__(name, "Poseidon", max_hp=130, max_energy=90, attack=20, defense=18, speed=18)
        self.lore = "Alta vitalidade e defesa; excelente resistência em lutas longas."
        self.abilities = [
            Ability("Fúria das Marés", 25, 1.6, "Onda de pressão marítima."),
            Ability("Pulso Sísmico", 35, 1.9, "Tremor concentrado contra o alvo.")
        ]
        if level > 1:
            self.scale_to_level(level)


class ChildOfHades(Demigod):
    def __init__(self, name, level=1):
        super().__init__(name, "Hades", max_hp=105, max_energy=120, attack=26, defense=15, speed=17)
        self.lore = "Grande reserva de energia e alto dano bruto com habilidades ctônicas."
        self.abilities = [
            Ability("Viagem nas Sombras", 25, 1.5, "Ataque furtivo das sombras."),
            Ability("Fissura do Submundo", 40, 2.1, "Golpe pesado de energia sombria.")
        ]
        if level > 1:
            self.scale_to_level(level)


class Enemy(Entity):
    def __init__(self, name, enemy_type, max_hp, attack, defense, speed):
        super().__init__(name, max_hp, attack, defense, speed)
        self.enemy_type = enemy_type


ENEMY_PRESETS = {
    "Minotauro": Enemy("Minotauro do Labirinto", "Besta Mitológica", max_hp=140, attack=22, defense=12, speed=14),
    "Hidra de Lerna": Enemy("Hidra de Lerna", "Monstro Multi-Cabeças", max_hp=180, attack=25, defense=15, speed=12),
    "Empusa": Enemy("Empusa das Sombras", "Espírito Ctônico", max_hp=95, attack=24, defense=10, speed=21),
}


def create_demigod_instance(godly_parent, level):
    level = max(1, min(20, int(level)))
    if godly_parent == "Zeus":
        return ChildOfZeus(f"Semideus de Zeus (Nv. {level})", level)
    if godly_parent == "Poseidon":
        return ChildOfPoseidon(f"Semideus de Poseidon (Nv. {level})", level)
    if godly_parent == "Hades":
        return ChildOfHades(f"Semideus de Hades (Nv. {level})", level)
    raise ValueError("Linhagem inválida.")


def create_enemy_instance(enemy_key, custom_defense=None):
    preset = ENEMY_PRESETS.get(enemy_key, ENEMY_PRESETS["Minotauro"])
    enemy = Enemy(preset.name, preset.enemy_type, preset.max_hp, preset.attack, preset.defense, preset.speed)
    if custom_defense is not None:
        enemy.defense = max(0, min(100, int(custom_defense)))
    return enemy


class CombatSimulation:
    def __init__(self, sim_id, title, godly_parent, level, enemy_key, ability_index=0, custom_defense=None):
        self.id = int(sim_id)
        self.title = title
        self.godly_parent = godly_parent
        self.level = max(1, min(20, int(level)))
        self.enemy_key = enemy_key if enemy_key in ENEMY_PRESETS else "Minotauro"
        self.ability_index = max(0, min(1, int(ability_index)))
        self.custom_defense = int(custom_defense) if custom_defense is not None and str(custom_defense).isdigit() else None

        self.demigod = create_demigod_instance(self.godly_parent, self.level)
        self.enemy = create_enemy_instance(self.enemy_key, self.custom_defense)
        self.chosen_ability = self.demigod.abilities[self.ability_index]

        raw = self.demigod.attack * self.chosen_ability.damage_multiplier
        mitigated = max(5.0, round(raw - (self.enemy.defense * 0.45), 1))
        counter = max(3.0, round(self.enemy.attack - (self.demigod.defense * 0.40), 1))
        turns = max(1, (self.enemy.max_hp + int(mitigated) - 1) // int(mitigated))

        self.raw_damage = round(raw, 1)
        self.estimated_damage = mitigated
        self.enemy_counter_damage = counter
        self.turns_to_defeat = turns
        self.first_strike = self.demigod.name if self.demigod.speed >= self.enemy.speed else self.enemy.name

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "godly_parent": self.godly_parent,
            "level": self.level,
            "enemy_key": self.enemy_key,
            "ability_index": self.ability_index,
            "custom_defense": self.custom_defense
        }