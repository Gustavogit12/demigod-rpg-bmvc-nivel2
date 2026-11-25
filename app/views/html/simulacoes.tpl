<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demigod RPG — Informações e Simulações (BMVC)</title>
    <link rel="stylesheet" type="text/css" href="/static/css/demigod_sim.css">
</head>
<body>
    <header class="top-header">
        <div class="container header-row">
            <div>
                <span class="kicker">DEMIGOD RPG • BMVC NÍVEL 2</span>
                <h1>Portal de Informações e Simulações</h1>
                <p>Consulte linhagens, regras adicionais do jogo e gerencie simulações de combate.</p>
            </div>
            <div class="header-links">
                <a href="/helper" class="nav-link">Ver Helper BMVC</a>
                <span class="count-pill">Total: <strong>{{len(simulations)}}</strong></span>
            </div>
        </div>
    </header>

    <main class="container">
        <!-- Informações das Linhagens -->
        <section class="block">
            <h2>Linhagens Divinas e Atributos Base</h2>
            <div class="grid-3">
                % for g in lineage_guide:
                <article class="card god-{{g['god'].lower()}}">
                    <span class="god-tag">{{g['god']}}</span>
                    <h3>{{g['title']}}</h3>
                    <p class="mono-box">{{g['stats']}}</p>
                    <p class="muted">{{g['info']}}</p>
                </article>
                % end
            </div>
        </section>

        <!-- Informações Adicionais do Jogo -->
        <section class="block">
            <h2>Informações Adicionais e Mecânicas</h2>
            <div class="card extra-info-card">
                <ul class="info-list">
                    % for tip in additional_info:
                    <li>{{tip}}</li>
                    % end
                </ul>
            </div>
        </section>

        <!-- CRUD: Formulário + Lista -->
        <section class="block crud-layout">
            <div class="card form-box">
                % if editing_sim:
                    <h2>Editar Simulação #{{editing_sim.id}}</h2>
                    <form id="sim-form" action="/simulacoes/update/{{editing_sim.id}}" method="POST" novalidate>
                % else:
                    <h2>Nova Simulação</h2>
                    <form id="sim-form" action="/simulacoes/create" method="POST" novalidate>
                % end

                    <div id="form-error" class="alert alert-error hidden"></div>

                    <div class="form-field">
                        <label for="title">Título da Simulação *</label>
                        <input
                            type="text"
                            id="title"
                            name="title"
                            value="{{editing_sim.title if editing_sim else ''}}"
                            placeholder="Ex: Raio vs Hidra Nv. 5"
                            required
                        >
                    </div>

                    <div class="form-field">
                        <label for="godly_parent">Linhagem Divina *</label>
                        <select id="godly_parent" name="godly_parent" required>
                            <option value="">-- Selecione --</option>
                            <option value="Zeus" {{'selected' if editing_sim and editing_sim.godly_parent == 'Zeus' else ''}}>Zeus</option>
                            <option value="Poseidon" {{'selected' if editing_sim and editing_sim.godly_parent == 'Poseidon' else ''}}>Poseidon</option>
                            <option value="Hades" {{'selected' if editing_sim and editing_sim.godly_parent == 'Hades' else ''}}>Hades</option>
                        </select>
                    </div>

                    <div class="form-grid-2">
                        <div class="form-field">
                            <label for="level">Nível (1–20)</label>
                            <input
                                type="number"
                                id="level"
                                name="level"
                                min="1"
                                max="20"
                                value="{{editing_sim.level if editing_sim else 1}}"
                                required
                            >
                        </div>

                        <div class="form-field">
                            <label for="ability_index">Habilidade</label>
                            <select id="ability_index" name="ability_index">
                                <option value="0" {{'selected' if editing_sim and editing_sim.ability_index == 0 else ''}}>Habilidade 1</option>
                                <option value="1" {{'selected' if editing_sim and editing_sim.ability_index == 1 else ''}}>Habilidade 2</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-grid-2">
                        <div class="form-field">
                            <label for="enemy_key">Inimigo</label>
                            <select id="enemy_key" name="enemy_key">
                                % for ek in enemy_keys:
                                    <option value="{{ek}}" {{'selected' if editing_sim and editing_sim.enemy_key == ek else ''}}>{{ek}}</option>
                                % end
                            </select>
                        </div>

                        <div class="form-field">
                            <label for="custom_defense">Defesa Inimigo (Opc.)</label>
                            <input
                                type="number"
                                id="custom_defense"
                                name="custom_defense"
                                min="0"
                                max="100"
                                value="{{editing_sim.custom_defense if editing_sim and editing_sim.custom_defense is not None else ''}}"
                                placeholder="Padrão"
                            >
                        </div>
                    </div>

                    <div id="sim-preview" class="preview-box">
                        Selecione linhagem e nível para prévia rápida.
                    </div>

                    <div class="btn-group">
                        <button type="submit" class="btn btn-gold">
                            {{'Salvar Alterações' if editing_sim else 'Criar Simulação'}}
                        </button>
                        % if editing_sim:
                            <a href="/simulacoes" class="btn btn-gray">Cancelar</a>
                        % end
                    </div>
                </form>
            </div>

            <div class="list-box">
                % if msg:
                    <div class="alert alert-{{msg_type}}">{{msg}}</div>
                % end

                <div class="list-topbar">
                    <h2>Simulações Salvas</h2>
                    <input type="text" id="filter-input" placeholder="Buscar simulação...">
                </div>

                % if not simulations:
                    <div class="card muted">Nenhuma simulação cadastrada.</div>
                % else:
                    <div class="grid-2" id="sim-list">
                        % for sim in simulations:
                        <article class="card sim-item god-{{sim.godly_parent.lower()}}" data-filter="{{(sim.title + ' ' + sim.godly_parent + ' ' + sim.enemy_key).lower()}}">
                            <div class="sim-head">
                                <div>
                                    <span class="god-tag">{{sim.godly_parent}} • Nv. {{sim.level}}</span>
                                    <h3>{{sim.title}}</h3>
                                </div>
                                <span class="badge-turns">~{{sim.turns_to_defeat}} turno(s)</span>
                            </div>

                            <p class="small-line"><strong>Classe:</strong> {{sim.demigod.__class__.__name__}} | <strong>Skill:</strong> {{sim.chosen_ability.name}} ({{sim.chosen_ability.damage_multiplier}}x)</p>
                            <p class="small-line"><strong>Alvo:</strong> {{sim.enemy.name}} (HP {{sim.enemy.max_hp}} • DEF {{sim.enemy.defense}})</p>

                            <div class="stats-mini">
                                <div><span>Bruto</span><strong>{{sim.raw_damage}}</strong></div>
                                <div><span>Estimado</span><strong>{{sim.estimated_damage}}</strong></div>
                                <div><span>Contra-ataque</span><strong>{{sim.enemy_counter_damage}}</strong></div>
                                <div><span>Iniciativa</span><strong>{{sim.first_strike.split()[0]}}</strong></div>
                            </div>

                            <div class="item-actions">
                                <a href="/simulacoes/edit/{{sim.id}}" class="btn btn-sky">Editar</a>
                                <form action="/simulacoes/delete/{{sim.id}}" method="POST" class="delete-form" data-title="{{sim.title}}">
                                    <button type="submit" class="btn btn-red">Excluir</button>
                                </form>
                            </div>
                        </article>
                        % end
                    </div>
                % end
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container">Demigod RPG • Base BMVC (Bottle + JSON)</div>
    </footer>

    <script src="/static/js/demigod_sim.js"></script>
</body>
</html>