class ContaUsuario:
    """Conta de usuário para controle de acesso do Bestiário."""

    def __init__(self, username, password, role="mestre"):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
        }