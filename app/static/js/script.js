document.addEventListener("DOMContentLoaded", function () {

    // ---------- Página inicial: simulador de combate ----------
    var simulador = document.getElementById("simulador");

    if (simulador) {
        var caixa = document.getElementById("resultado");
        var titulo = document.getElementById("resultado-titulo");
        var texto = document.getElementById("resultado-texto");
        var botoesAtaque = document.querySelectorAll(".btn-atacar");
        var botaoSortear = document.getElementById("btn-sortear");

        var nomeInimigo = simulador.getAttribute("data-inimigo");
        var defesaInimigo = Number(simulador.getAttribute("data-defesa"));

        function mostrar(tituloTexto, mensagem) {
            titulo.textContent = tituloTexto;
            texto.textContent = mensagem;
            caixa.classList.remove("oculto");
        }

        function numeroEntre(minimo, maximo) {
            return Math.floor(Math.random() * (maximo - minimo + 1)) + minimo;
        }

        for (var i = 0; i < botoesAtaque.length; i++) {
            botoesAtaque[i].addEventListener("click", function () {
                var nome = this.getAttribute("data-nome");
                var ataque = Number(this.getAttribute("data-ataque"));

                var critico = Math.random() < 0.25;
                var danoBruto = critico ? ataque * 2 : ataque;
                var danoFinal = Math.max(1, danoBruto - defesaInimigo);

                if (critico) {
                    mostrar("⚡ Acerto crítico!",
                        nome + " causou " + danoFinal + " de dano a " + nomeInimigo + ".");
                } else {
                    mostrar("🗡️ Ataque normal",
                        nome + " causou " + danoFinal + " de dano a " + nomeInimigo + ".");
                }
            });
        }

        botaoSortear.addEventListener("click", function () {
            var hp = numeroEntre(105, 150);
            var energia = numeroEntre(65, 90);
            var ataque = numeroEntre(20, 31);
            var defesa = numeroEntre(10, 19);

            mostrar("🎲 Ficha sorteada",
                "HP: " + hp + " | Energia: " + energia +
                " | Ataque: " + ataque + " | Defesa: " + defesa);
        });
    }

    // ---------- Bestiário: confirmar antes de excluir ----------
    var formsExcluir = document.querySelectorAll(".form-excluir");

    for (var j = 0; j < formsExcluir.length; j++) {
        formsExcluir[j].addEventListener("submit", function (evento) {
            var nome = this.getAttribute("data-nome");
            if (!confirm('Deseja realmente excluir "' + nome + '"?')) {
                evento.preventDefault();
            }
        });
    }

    // ---------- Bestiário: filtro por nome em tempo real ----------
    var filtro = document.getElementById("filtro");

    if (filtro) {
        filtro.addEventListener("input", function () {
            var termo = filtro.value.toLowerCase();
            var linhas = document.querySelectorAll("#tabela-criaturas tbody tr");

            for (var k = 0; k < linhas.length; k++) {
                var nomeLinha = linhas[k].cells[0].textContent.toLowerCase();
                if (nomeLinha.indexOf(termo) !== -1) {
                    linhas[k].style.display = "";
                } else {
                    linhas[k].style.display = "none";
                }
            }
        });
    }

    // ---------- Formulário: validação antes de enviar ----------
    var formCriatura = document.getElementById("form-criatura");

    if (formCriatura) {
        var aviso = document.getElementById("aviso-form");
        var camposTexto = ["name", "title"];
        var camposNumero = ["hp", "attack", "defense", "speed", "xp"];

        formCriatura.addEventListener("submit", function (evento) {
            var mensagem = "";
            var n;

            for (n = 0; n < camposTexto.length; n++) {
                var campoTexto = document.getElementById(camposTexto[n]);
                campoTexto.classList.remove("invalido");
                if (campoTexto.value.trim() === "") {
                    campoTexto.classList.add("invalido");
                    mensagem = "Preencha todos os campos com valores válidos.";
                }
            }

            for (n = 0; n < camposNumero.length; n++) {
                var campoNumero = document.getElementById(camposNumero[n]);
                var valor = campoNumero.value.trim();
                campoNumero.classList.remove("invalido");
                if (valor === "" || !Number.isInteger(Number(valor)) || Number(valor) < 0) {
                    campoNumero.classList.add("invalido");
                    mensagem = "Preencha todos os campos com valores válidos.";
                }
            }

            if (mensagem === "" && Number(document.getElementById("hp").value) < 1) {
                document.getElementById("hp").classList.add("invalido");
                mensagem = "O HP precisa ser maior que zero.";
            }

            if (mensagem !== "") {
                evento.preventDefault();
                aviso.textContent = mensagem;
            } else {
                aviso.textContent = "";
            }
        });
    }
    // ---------- Bestiário: atualização assíncrona via WebSocket ----------
    var corpoCriaturas = document.getElementById("corpo-criaturas");
    var wsStatus = document.getElementById("ws-status");
    var wsEvento = document.getElementById("ws-evento");

    if (corpoCriaturas && window.WebSocket) {
        var areaTabela = document.getElementById("area-tabela");
        var mensagemVazio = document.getElementById("mensagem-vazio");
        var protocolo = window.location.protocol === "https:" ? "wss://" : "ws://";
        var ws = new WebSocket(protocolo + window.location.host + "/ws/bestiario");

        function escaparTexto(valor) {
            return String(valor)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;");
        }

        function vincularConfirmacaoExclusao() {
            var forms = document.querySelectorAll(".form-excluir");
            for (var i = 0; i < forms.length; i++) {
                forms[i].onsubmit = function (evento) {
                    var nome = this.getAttribute("data-nome");
                    if (!confirm('Deseja realmente excluir "' + nome + '"?')) {
                        evento.preventDefault();
                    }
                };
            }
        }

        function aplicarFiltroAtual() {
            var campoFiltro = document.getElementById("filtro");
            if (!campoFiltro) {
                return;
            }
            var termo = campoFiltro.value.toLowerCase();
            var linhas = corpoCriaturas.querySelectorAll("tr");
            for (var i = 0; i < linhas.length; i++) {
                var nomeLinha = linhas[i].cells[0].textContent.toLowerCase();
                linhas[i].style.display = nomeLinha.indexOf(termo) !== -1 ? "" : "none";
            }
        }

        function renderizarCriaturas(enemies) {
            if (!enemies || enemies.length === 0) {
                corpoCriaturas.innerHTML = "";
                if (areaTabela) areaTabela.style.display = "none";
                if (mensagemVazio) mensagemVazio.style.display = "";
                return;
            }

            if (areaTabela) areaTabela.style.display = "";
            if (mensagemVazio) mensagemVazio.style.display = "none";

            var html = "";
            for (var i = 0; i < enemies.length; i++) {
                var e = enemies[i];
                html += "<tr>" +
                    "<td>" + escaparTexto(e.name) + "</td>" +
                    "<td>" + escaparTexto(e.title) + "</td>" +
                    "<td>" + escaparTexto(e.hp) + "</td>" +
                    "<td>" + escaparTexto(e.attack) + "</td>" +
                    "<td>" + escaparTexto(e.defense) + "</td>" +
                    "<td>" + escaparTexto(e.speed) + "</td>" +
                    "<td>" + escaparTexto(e.xp) + "</td>" +
                    '<td class="acoes">' +
                        '<a class="botao secundario" href="/bestiario/editar/' + escaparTexto(e.id) + '">Editar</a> ' +
                        '<form method="post" action="/bestiario/excluir/' + escaparTexto(e.id) + '" ' +
                              'class="form-excluir" data-nome="' + escaparTexto(e.name) + '">' +
                            '<button type="submit" class="perigo">Excluir</button>' +
                        "</form>" +
                    "</td>" +
                "</tr>";
            }
            corpoCriaturas.innerHTML = html;
            vincularConfirmacaoExclusao();
            aplicarFiltroAtual();
        }

        var botoesDado = document.querySelectorAll(".btn-dado");
        for (var d = 0; d < botoesDado.length; d++) {
            botoesDado[d].addEventListener("click", function () {
                if (ws.readyState === WebSocket.OPEN) {
                    var lados = Number(this.getAttribute("data-lados"));
                    ws.send(JSON.stringify({ type: "dice_roll", sides: lados }));
                }
            });
        }

        ws.onopen = function () {
            if (wsStatus) wsStatus.textContent = "Conectado (ao vivo)";
        };

        ws.onmessage = function (evento) {
            try {
                var dados = JSON.parse(evento.data);
                if (dados.type === "bestiario_sync") {
                    renderizarCriaturas(dados.enemies);
                    if (wsEvento && dados.message) {
                        var hora = dados.timestamp ? "[" + dados.timestamp + "] " : "";
                        wsEvento.textContent = hora + dados.message;
                    }
                } else if (dados.type === "dice_roll") {
                    if (wsEvento && dados.message) {
                        var horaDado = dados.timestamp ? "[" + dados.timestamp + "] " : "";
                        wsEvento.textContent = horaDado + dados.message;
                    }
                }
            } catch (err) {
                console.error("Erro ao processar mensagem WebSocket:", err);
            }
        };

        ws.onclose = function () {
            if (wsStatus) wsStatus.textContent = "Desconectado";
        };
    }
});