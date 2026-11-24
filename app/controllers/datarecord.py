import json
import os

from app.models.rpg_engine import ChildOfHades, ChildOfPoseidon, ChildOfZeus, Enemy

FILE_PATH = "app/controllers/db/creatures.json"


class DataRecord():
    """Guarda os semideuses (fixos) e as criaturas (CRUD, salvas em JSON)."""

    def __init__(self):
        self.__demigods = []
        self.__enemies = []
        self.read()

    def read(self):
        self.__demigods = []
        self.__demigods.append(ChildOfZeus("Thalia"))
        self.__demigods.append(ChildOfPoseidon("Percy"))
        self.__demigods.append(ChildOfHades("Nico"))

        try:
            with open(FILE_PATH, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                self.__enemies = [Enemy(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
            self.__enemies = []
            self.__enemies.append(Enemy("Asterius, o Minotauro", "Fera do Labirinto", 130, 24, 10, 9, 100, 1))
            self.__enemies.append(Enemy("Hidra de Lerna", "Serpente dos Pântanos", 170, 27, 14, 8, 160, 2))
            self.save()

    def save(self):
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        data = []
        for enemy in self.__enemies:
            data.append(enemy.to_dict())
        with open(FILE_PATH, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def __next_id(self):
        biggest = 0
        for enemy in self.__enemies:
            if enemy.id > biggest:
                biggest = enemy.id
        return biggest + 1

    def get_demigods(self):
        return self.__demigods

    def get_enemies(self):
        return self.__enemies

    def get_enemy(self, enemy_id):
        for enemy in self.__enemies:
            if enemy.id == enemy_id:
                return enemy
        return None

    def add_enemy(self, data):
        enemy = Enemy(data["name"], data["title"], data["hp"], data["attack"],
                      data["defense"], data["speed"], data["xp"], self.__next_id())
        self.__enemies.append(enemy)
        self.save()

    def update_enemy(self, enemy_id, data):
        enemy = self.get_enemy(enemy_id)
        if enemy is None:
            return False
        enemy.name = data["name"]
        enemy.title = data["title"]
        enemy.hp = data["hp"]
        enemy.max_hp = data["hp"]
        enemy.attack = data["attack"]
        enemy.defense = data["defense"]
        enemy.speed = data["speed"]
        enemy.xp = data["xp"]
        self.save()
        return True

    def delete_enemy(self, enemy_id):
        enemy = self.get_enemy(enemy_id)
        if enemy is None:
            return False
        self.__enemies.remove(enemy)
        self.save()
        return True