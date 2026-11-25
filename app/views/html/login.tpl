<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demigod RPG - Login do Mestre</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

    <header class="topo">
        <h1>🔐 Acesso Restrito — Bestiário do Labirinto</h1>
        <p>Entre com sua conta de mestre para gerenciar as criaturas do Demigod RPG.</p>
        <nav class="menu">
            <a href="/inicio">Início</a>
            % if current_user:
            <a href="/bestiario">Bestiário (restrito)</a>
            <a href="/logout">Sair ({{current_user.username}})</a>
            % else:
            <a href="/login">Login</a>
            % end
        </nav>
    </header>

    <main class="container">
        <section>
            <h2>Entrar na área restrita</h2>
            <div class="painel formulario">
                <p>Use uma conta de teste cadastrada (ex.: usuário <strong>mestre</strong>, senha <strong>olimpo123</strong>).</p>

                % if aviso:
                <p class="aviso">{{aviso}}</p>
                % end

                % if error:
                <p class="erro">{{error}}</p>
                % end

                <form method="post" action="/login">
                    <label for="username">Usuário</label>
                    <input type="text" id="username" name="username" value="{{username_value}}">

                    <label for="password">Senha</label>
                    <input type="password" id="password" name="password">

                    <div class="botoes">
                        <button type="submit">Entrar</button>
                        <a class="botao secundario" href="/inicio">Voltar ao início</a>
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