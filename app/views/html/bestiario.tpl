<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demigod RPG - Bestiário (Área Restrita)</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

    <header class="topo">
        <h1>🐉 Bestiário do Labirinto</h1>
        <p>Área restrita do mestre (<strong>{{current_user.username}}</strong>): cadastre, consulte, edite e remova criaturas.</p>
        <nav class="menu">
            <a href="/inicio">Início</a>
            <a href="/bestiario">Bestiário</a>
            <a href="/logout">Sair ({{current_user.username}})</a>
        </nav>
    </header>

    <main class="container"> 

        <section>
            <h2>Propósito desta área restrita</h2>
            <div class="painel">
                <p>Esta página é a ferramenta restrita do mestre do <strong>Demigod RPG</strong>. Somente usuários autenticados podem cadastrar novos monstros, alterar atributos e remover criaturas do jogo.</p>
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

            <div class="painel" id="ws-status-box">
                <p><strong>Tempo real (WebSocket):</strong> <span id="ws-status">Conectando...</span></p>
                <p id="ws-evento">Aguardando alterações no Bestiário.</p>
                <div class="barra">
                    <button type="button" class="botao secundario btn-dado" data-lados="6">🎲 d6</button>
                    <button type="button" class="botao secundario btn-dado" data-lados="10">🎲 d10</button>
                    <button type="button" class="botao secundario btn-dado" data-lados="20">🎲 d20</button>
                </div>
            </div>
            <div class="tabela-rolagem" id="area-tabela" % if not enemies: style="display: none;" % end>
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
                    <tbody id="corpo-criaturas">
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
            <p class="vazio" id="mensagem-vazio" % if enemies: style="display: none;" % end>
                Nenhuma criatura cadastrada. Clique em "Nova criatura" para começar.
            </p>
        </section>

    </main>

    <footer>
        <p>Estrutura BMVC Nível 3 • Python + Bottle • Projeto de Gustavo</p>
    </footer>

    <script src="/static/js/script.js"></script>
</body>
</html>