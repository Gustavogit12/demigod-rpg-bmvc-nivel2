from bottle import Bottle, redirect, request, run, static_file

from app.controllers.application import Application

app = Bottle()
ctl = Application()


# -----------------------------------------------------------------------------
# Arquivos estáticos e helper:

@app.route("/static/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root="./app/static")


@app.route("/helper")
def helper(info=None):
    return ctl.render("helper")


# -----------------------------------------------------------------------------
# Rotas públicas e de autenticação:

@app.route("/", method="GET")
@app.route("/inicio", method="GET")
def action_inicio():
    return ctl.render("inicio")


@app.route("/login", method="GET")
def action_login_get():
    if ctl.current_user() is not None:
        redirect("/inicio")
    return ctl.render("login")


@app.route("/login", method="POST")
def action_login_post():
    form = request.forms.decode()
    error = ctl.login_user(form)
    if error:
        return ctl.login(error=error, username_value=form.get("username", ""))
    redirect("/inicio")


@app.route("/logout", method="GET")
@app.route("/logout", method="POST")
def action_logout():
    ctl.logout_user()
    redirect("/login?aviso=saiu")


# -----------------------------------------------------------------------------
# Rotas restritas do Bestiário (exigem login):

@app.route("/bestiario", method="GET")
def action_bestiario():
    return ctl.render("bestiario")


@app.route("/bestiario/novo", method="GET")
def action_novo_get():
    return ctl.render("formulario")


@app.route("/bestiario/novo", method="POST")
def action_novo_post():
    form = request.forms.decode()
    error = ctl.create_enemy(form)
    if error:
        return ctl.formulario(None, error, ctl.form_values(form))
    redirect("/inicio ?aviso=criada")


@app.route("/bestiario/editar/<enemy_id:int>", method="GET")
def action_editar_get(enemy_id):
    return ctl.render("formulario", enemy_id)


@app.route("/bestiario/editar/<enemy_id:int>", method="POST")
def action_editar_post(enemy_id):
    form = request.forms.decode()
    error = ctl.update_enemy(enemy_id, form)
    if error:
        return ctl.formulario(enemy_id, error, ctl.form_values(form))
    redirect("/inicio?aviso=editada")


@app.route("/bestiario/excluir/<enemy_id:int>", method="POST")
def action_excluir(enemy_id):
    ctl.delete_enemy(enemy_id)
    redirect("/inicio?aviso=excluida")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080, debug=True)