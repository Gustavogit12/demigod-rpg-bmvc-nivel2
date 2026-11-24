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
});