from bottle import template, redirect, request

from app.controllers.datarecord import DataRecord

FIELDS = ['name', 'title', 'hp', 'attack', 'defense', 'speed', 'xp']
NUMBER_FIELDS = ['hp', 'attack', 'defense', 'speed', 'xp']

NOTICES = {
    'criada': 'Criatura cadastrada com sucesso.',
    'editada': 'Criatura atualizada com sucesso.',
    'excluida': 'Criatura excluída com sucesso.'
}


class Application():

    def __init__(self):
        self.pages = {
            'inicio': self.inicio,
            'bestiario': self.bestiario,
            'formulario': self.formulario
        }
        self.__model = DataRecord()

    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)

    def helper(self):
        return template('app/views/html/helper')

    def inicio(self):
        return template('app/views/html/inicio',
                        demigods=self.__model.get_demigods(),
                        enemies=self.__model.get_enemies())

    def bestiario(self):
        notice = NOTICES.get(request.query.get('aviso', ''))
        return template('app/views/html/bestiario',
                        enemies=self.__model.get_enemies(),
                        aviso=notice)

    def formulario(self, enemy_id=None, error=None, valores=None):
        if enemy_id is None:
            titulo = 'Nova criatura'
            action = '/bestiario/novo'
            base = {'name': '', 'title': '', 'hp': '', 'attack': '',
                    'defense': '', 'speed': '', 'xp': ''}
        else:
            enemy = self.__model.get_enemy(enemy_id)
            if enemy is None:
                redirect('/bestiario')
            titulo = 'Editar criatura'
            action = '/bestiario/editar/' + str(enemy_id)
            base = enemy.to_dict()

        if valores is not None:
            base = valores

        return template('app/views/html/formulario',
                        titulo=titulo, action=action, valores=base, error=error)

    def form_values(self, form):
        values = {}
        for field in FIELDS:
            values[field] = form.get(field, '')
        return values

    def create_enemy(self, form):
        data, error = self.__read_form(form)
        if error:
            return error
        self.__model.add_enemy(data)
        return None

    def update_enemy(self, enemy_id, form):
        if self.__model.get_enemy(enemy_id) is None:
            redirect('/bestiario')
        data, error = self.__read_form(form)
        if error:
            return error
        self.__model.update_enemy(enemy_id, data)
        return None

    def delete_enemy(self, enemy_id):
        self.__model.delete_enemy(enemy_id)

    def __read_form(self, form):
        name = form.get('name', '').strip()
        title = form.get('title', '').strip()
        if name == '' or title == '':
            return None, 'Preencha o nome e o título da criatura.'

        data = {'name': name, 'title': title}
        for field in NUMBER_FIELDS:
            try:
                value = int(form.get(field, '').strip())
            except ValueError:
                return None, 'Os campos numéricos precisam ser números inteiros.'
            if value < 0:
                return None, 'Os campos numéricos não podem ser negativos.'
            data[field] = value

        if data['hp'] < 1:
            return None, 'O HP precisa ser maior que zero.'
        return data, None