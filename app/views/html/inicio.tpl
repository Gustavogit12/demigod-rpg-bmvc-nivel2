<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demigod RPG - Guia das Linhagens</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

    <header class="topo">
        <h1 Demigod RPG: Guia das Linhagens </h1>
        <p>Consulte as classes divinas, conheça as criaturas do labirinto e teste um ataque.</p>
        <nav class="menu">
            <a href="/inicio">Início</a>
            % if current_user:
            <a href="/bestiario">Bestiário</a>
            <a href="/logout">Sair ({{current_user.username}})</a>
            % else:
            <a href="/login">Login</a>
            % end
        </nav>
    </header>

    <main class="container">

        <section>
            <h2>Propósito deste portal</h2>
            <div class="painel">
                <p>Este portal é o guia de consulta do <strong>Demigod RPG</strong>. Aqui o jogador compara os atributos de cada linhagem olímpica, conhece os monstros que vai enfrentar e simula um ataque antes de escolher o seu semideus. O cadastro das criaturas fica na área restrita do <strong>Bestiário</strong>.</p>
            </div>
        </section>

        <section>
            <h2>Linhagens olímpicas</h2>
            <div class="grade">
                % for d in demigods:
                <article class="cartao">
                    <h3>{{d.lineage}}</h3>
                    <p class="subtitulo">{{d.name}} • {{d.title}} • Elemento {{d.element}}</p>
                    <div class="selos">
                        <span class="selo">❤️ HP: {{d.hp}}</span>
                        <span class="selo">⚡ EN: {{d.energy}}</span>
                        <span class="selo">⚔️ ATQ: {{d.attack}}</span>
                        <span class="selo">🛡️ DEF: {{d.defense}}</span>
                        <span class="selo">💨 VEL: {{d.speed}}</span>
                    </div>
                    <p>{{d.perk}}</p>
                    <p class="rotulo">Habilidades:</p>
                    <ul>
                        % for a in d.abilities:
                        <li>{{a.name}} (nível {{a.required_level}})</li>
                        % end
                    </ul>
                </article>
                % end
            </div>
        </section>

        <section>
            <h2>Criaturas do labirinto</h2>
            % if enemies:
            <div class="grade">
                % for e in enemies:
                <article class="cartao">
                    <h3>{{e.name}}</h3>
                    <p class="subtitulo">{{e.title}}</p>
                    <div class="selos">
                        <span class="selo">❤️ HP: {{e.hp}}</span>
                        <span class="selo">⚔️ ATQ: {{e.attack}}</span>
                        <span class="selo">🛡️ DEF: {{e.defense}}</span>
                        <span class="selo">⭐ XP: +{{e.xp}}</span>
                    </div>
                </article>
                % end
            </div>
            % else:
            <p class="vazio">Nenhuma criatura cadastrada no momento.</p>
            % end
        </section>

        % if enemies:
        <section>
            <h2>Simulador de combate</h2>
            <div class="painel" id="simulador"
                 data-inimigo="{{enemies[0].name}}" data-defesa="{{enemies[0].defense}}">
                <p>Escolha um semideus para atacar <strong>{{enemies[0].name}}</strong>, ou sorteie os atributos de um novo semideus:</p>
                <div class="botoes">
                    % for d in demigods:
                    <button type="button" class="btn-atacar"
                            data-nome="{{d.name}}" data-ataque="{{d.attack}}">Atacar com {{d.name}}</button>
                    % end
                    <button type="button" id="btn-sortear" class="secundario">Sortear atributos</button>
                </div>
                <div id="resultado" class="resultado oculto">
                    <p><strong id="resultado-titulo"></strong></p>
                    <p id="resultado-texto"></p>
                </div>
            </div>
        </section>
        % end

    </main>

    <footer>
        <p>Estrutura BMVC Nível 3 • Python + Bottle • Projeto de Gustavo</p>
    </footer>

    <script src="/static/js/script.js"></script>
</body>
</html>