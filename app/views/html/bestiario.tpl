<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demigod RPG - Bestiário</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

    <header class="topo">
        <h1>🐉 Bestiário do Labirinto</h1>
        <p>Cadastre, consulte, edite e remova as criaturas que os semideuses vão enfrentar.</p>
        <nav class="menu">
            <a href="/inicio">Início</a>
            <a href="/bestiario">Bestiário (cadastro de criaturas)</a>
        </nav>
    </header>

    <main class="container">

        <section>
            <h2>Propósito desta página</h2>
            <div class="painel">
                <p>Esta página é a ferramenta do mestre do <strong>Demigod RPG</strong>. Aqui ele administra as criaturas do jogo: cadastra monstros novos, ajusta os atributos dos que já existem e remove os que não serão usados.</p>
            </div>
        </section>

        <section>
            <h2>Criaturas cadastradas</h2>

            % if aviso:
            <p class="sucesso">{{aviso}}</p>
            % end

            <div class="barra">
                <input type="text" id="filtro" placeholder="Filtrar por nome...">
                <a class="botao" href="/bestiario/novo">+ Nova criatura</a>
            </div>

            % if enemies:
            <div class="tabela-rolagem">
                <table class="tabela" id="tabela-criaturas">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Título</th>
                            <th>HP</th>
                            <th>ATQ</th>
                            <th>DEF</th>
                            <th>VEL</th>
                            <th>XP</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for e in enemies:
                        <tr>
                            <td>{{e.name}}</td>
                            <td>{{e.title}}</td>
                            <td>{{e.hp}}</td>
                            <td>{{e.attack}}</td>
                            <td>{{e.defense}}</td>
                            <td>{{e.speed}}</td>
                            <td>{{e.xp}}</td>
                            <td class="acoes">
                                <a class="botao secundario" href="/bestiario/editar/{{e.id}}">Editar</a>
                                <form method="post" action="/bestiario/excluir/{{e.id}}"
                                      class="form-excluir" data-nome="{{e.name}}">
                                    <button type="submit" class="perigo">Excluir</button>
                                </form>
                            </td>
                        </tr>
                        % end
                    </tbody>
                </table>
            </div>
            % else:
            <p class="vazio">Nenhuma criatura cadastrada. Clique em "Nova criatura" para começar.</p>
            % end
        </section>

    </main>

    <footer>
        <p>Estrutura BMVC • Python + Bottle • Projeto de Gustavo</p>
    </footer>

    <script src="/static/js/script.js"></script>
</body>
</html>