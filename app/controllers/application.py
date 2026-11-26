import json
from datetime import datetime
from bottle import redirect, request, response, template

from app.controllers.datarecord import DataRecord
from app.controllers.ws_hub import hub
SESSION_COOKIE = "demigod_session"

FIELDS = ["name", "title", "hp", "attack", "defense", "speed", "xp"]
NUMBER_FIELDS = ["hp", "attack", "defense", "speed", "xp"]

NOTICES = {
    "criada": "Criatura cadastrada com sucesso.",
    "editada": "Criatura atualizada com sucesso.",
    "excluida": "Criatura excluída com sucesso.",
    "login_necessario": "Faça login para acessar o portal Demigod RPG",
    "saiu": "Sessão encerrada com sucesso.",
}


class Application:

    def __init__(self):
        self.pages = {
            "inicio": self.inicio,
            "login": self.login,
            "bestiario": self.bestiario,
            "formulario": self.formulario,
        }
        self.__model = DataRecord()

    def current_user(self):
        token = request.get_cookie(SESSION_COOKIE)
        return self.__model.get_user_by_session(token)

    def require_login(self):
        user = self.current_user()
        if user is None:
            redirect("/login?aviso=login_necessario")
        return user

    def login_user(self, form):
        username = form.get("username", "").strip()
        password = form.get("password", "")
        if username == "" or password == "":
            return "Preencha o usuário e a senha."

        user = self.__model.authenticate(username, password)
        if user is None:
            return "Usuário ou senha inválidos."

        token = self.__model.create_session(user.username)
        response.set_cookie(SESSION_COOKIE, token, path="/")
        return None

    def logout_user(self):
        token = request.get_cookie(SESSION_COOKIE)
        self.__model.logout_session(token)
        response.delete_cookie(SESSION_COOKIE, path="/")

    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        return content(parameter)

    def helper(self):
        return template("app/views/html/helper", current_user=self.current_user())
    def inicio(self):
        user = self.require_login()
        return template(
            "app/views/html/inicio",
            demigods=self.__model.get_demigods(),
            enemies=self.__model.get_enemies(),
            current_user=user,
        )

    def login(self, error=None, username_value=""):
        notice = NOTICES.get(request.query.get("aviso", ""))
        return template(
            "app/views/html/login",
            error=error,
            aviso=notice,
            username_value=username_value,
            current_user=self.current_user(),
        )

    def bestiario(self):
        user = self.require_login()
        notice = NOTICES.get(request.query.get("aviso", ""))
        return template(
            "app/views/html/bestiario",
            enemies=self.__model.get_enemies(),
            aviso=notice,
            current_user=user,
        )

    def formulario(self, enemy_id=None, error=None, valores=None):
        user = self.require_login()
        if enemy_id is None:
            titulo = "Nova criatura"
            action = "/bestiario/novo"
            base = {
                "name": "",
                "title": "",
                "hp": "",
                "attack": "",
                "defense": "",
                "speed": "",
                "xp": "",
            }
        else:
            enemy = self.__model.get_enemy(enemy_id)
            if enemy is None:
                redirect("/bestiario")
            titulo = "Editar criatura"
            action = "/bestiario/editar/" + str(enemy_id)
            base = enemy.to_dict()

        if valores is not None:
            base = valores

        return template(
            "app/views/html/formulario",
            titulo=titulo,
            action=action,
            valores=base,
            error=error,
            current_user=user,
        )

    def form_values(self, form):
        values = {}
        for field in FIELDS:
            values[field] = form.get(field, "")
        return values

    def create_enemy(self, form):
        user = self.require_login()
        data, error = self.__read_form(form)
        if error:
            return error
        self.__model.add_enemy(data)
        self.__notify_ws(f"Criatura '{data['name']}' adicionada por {user.username}.")
        return None

    def update_enemy(self, enemy_id, form):
        user = self.require_login()
        if self.__model.get_enemy(enemy_id) is None:
            redirect("/bestiario")
        data, error = self.__read_form(form)
        if error:
            return error
        self.__model.update_enemy(enemy_id, data)
        self.__notify_ws(f"Criatura '{data['name']}' atualizada por {user.username}.")
        return None

    def delete_enemy(self, enemy_id):
        user = self.require_login()
        enemy = self.__model.get_enemy(enemy_id)
        nome = enemy.name if enemy else f"ID {enemy_id}"
        self.__model.delete_enemy(enemy_id)
        self.__notify_ws(f"Criatura '{nome}' removida por {user.username}.")
        
    def __read_form(self, form):
        name = form.get("name", "").strip()
        title = form.get("title", "").strip()
        if name == "" or title == "":
            return None, "Preencha o nome e o título da criatura."

        data = {"name": name, "title": title}
        for field in NUMBER_FIELDS:
            try:
                value = int(form.get(field, "").strip())
            except ValueError:
                return None, "Os campos numéricos precisam ser números inteiros."
            if value < 0:
                return None, "Os campos numéricos não podem ser negativos."
            data[field] = value

        if data["hp"] < 1:
            return None, "O HP precisa ser maior que zero."
        return data, None
    def bestiario_snapshot_json(self, event_message="Atualização no Bestiário"):
        enemies = [e.to_dict() for e in self.__model.get_enemies()]
        payload = {
            "type": "bestiario_sync",
            "message": event_message,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "enemies": enemies,
        }
        return json.dumps(payload, ensure_ascii=False)

    def __notify_ws(self, event_message):
        enemies = [e.to_dict() for e in self.__model.get_enemies()]
        hub.broadcast({
            "type": "bestiario_sync",
            "message": event_message,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "enemies": enemies,
        })