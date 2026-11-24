import json
import os
from filelock import FileLock
from app.models.demigod_sim import CombatSimulation


class SimulationRecord:
    """Gerencia o CRUD completo das simulações em app/controllers/db/simulations.json."""

    def __init__(self, db_path="app/controllers/db/simulations.json"):
        self.db_path = db_path
        self.lock_path = f"{db_path}.lock"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.simulations = []
        self.read_all()

    def _read_raw_list(self):
        if not os.path.exists(self.db_path):
            return []
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_raw_list(self, raw_list):
        with FileLock(self.lock_path):
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(raw_list, f, indent=2, ensure_ascii=False)

    def read_all(self):
        raw_list = self._read_raw_list()
        self.simulations = [CombatSimulation(**item) for item in raw_list]
        return self.simulations

    def get_by_id(self, sim_id):
        sim_id = int(sim_id)
        for sim in self.read_all():
            if sim.id == sim_id:
                return sim
        return None

    def create(self, title, godly_parent, level, enemy_key, ability_index=0, custom_defense=None):
        raw_list = self._read_raw_list()
        next_id = max([int(item.get("id", 0)) for item in raw_list], default=0) + 1
        sim = CombatSimulation(next_id, title, godly_parent, level, enemy_key, ability_index, custom_defense)
        raw_list.append(sim.to_dict())
        self._write_raw_list(raw_list)
        self.read_all()
        return sim

    def update(self, sim_id, title, godly_parent, level, enemy_key, ability_index=0, custom_defense=None):
        sim_id = int(sim_id)
        raw_list = self._read_raw_list()
        updated_sim = None

        for idx, item in enumerate(raw_list):
            if int(item.get("id", -1)) == sim_id:
                updated_sim = CombatSimulation(sim_id, title, godly_parent, level, enemy_key, ability_index, custom_defense)
                raw_list[idx] = updated_sim.to_dict()
                break

        if updated_sim is None:
            return None

        self._write_raw_list(raw_list)
        self.read_all()
        return updated_sim

    def delete(self, sim_id):
        sim_id = int(sim_id)
        raw_list = self._read_raw_list()
        new_list = [item for item in raw_list if int(item.get("id", -1)) != sim_id]
        if len(new_list) == len(raw_list):
            return False
        self._write_raw_list(new_list)
        self.read_all()
        return True