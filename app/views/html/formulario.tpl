<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demigod RPG - {{titulo}}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

    <header class="topo">
        <h1>🐉 {{titulo}}</h1>
        <p>Usuário autenticado: <strong>{{current_user.username}}</strong> • Preencha os atributos e salve.</p>
        <nav class="menu">
            <a href="/inicio">Início</a>
            <a href="/bestiario">Bestiário</a>
            <a href="/logout">Sair ({{current_user.username}})</a>
        </nav>
    </header>

    <main class="container">
        <section>
            <h2>{{titulo}}</h2>
            <div class="painel formulario">

                % if error:
                <p class="erro">{{error}}</p>
                % end

                <p id="aviso-form" class="aviso"></p>

                <form id="form-criatura" method="post" action="{{action}}" novalidate>
                    <label for="name">Nome</label>
                    <input type="text" id="name" name="name" value="{{valores['name']}}">

                    <label for="title">Título (descrição curta)</label>
                    <input type="text" id="title" name="title" value="{{valores['title']}}">

                    <label for="hp">HP (vida)</label>
                    <input type="number" id="hp" name="hp" min="1" value="{{valores['hp']}}">

                    <label for="attack">Ataque</label>
                    <input type="number" id="attack" name="attack" min="0" value="{{valores['attack']}}">

                    <label for="defense">Defesa</label>
                    <input type="number" id="defense" name="defense" min="0" value="{{valores['defense']}}">

                    <label for="speed">Velocidade</label>
                    <input type="number" id="speed" name="speed" min="0" value="{{valores['speed']}}">

                    <label for="xp">XP concedido ao derrotar</label>
                    <input type="number" id="xp" name="xp" min="0" value="{{valores['xp']}}">

                    <div class="botoes">
                        <button type="submit">Salvar</button>
                        <a class="botao secundario" href="/bestiario">Cancelar</a>
                    </div>
                </form>
            </div>
        </section>
    </main>

    <footer>
        <p>Estrutura BMVC Nível 3 • Python + Bottle • Projeto de Gustavo</p>
    </footer>

    <script src="/static/js/script.js"></script>
</body>
</html>