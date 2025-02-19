function LoginConteiner() {
  let cont1 = document.querySelector("#conteiner-body");
  let cont2 = document.querySelector("#conteiner-float");
  cont1.classList.add("show");
  cont2.classList.add("show");
}

function LoginConteinerF() {
  let cont1 = document.querySelector("#conteiner-body");
  let cont2 = document.querySelector("#conteiner-float");
  cont1.classList.remove("show");
  cont2.classList.remove("show");
}
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("codigo").disabled = true;
});

document.querySelector("input#telefone").addEventListener("input", function (e) {
  let value = e.target.value.replace(/\D/g, "");

  if (value.length > 11) {
    value = value.slice(0, 11); // Limita a 11 dígitos
  }

  if (value.length === 11) {
    value = `(${value.slice(0, 2)}) ${value.slice(2, 3)} ${value.slice(3, 7)}-${value.slice(7, 11)}`;
  } else if (value.length >= 7) {
    value = `(${value.slice(0, 2)}) ${value.slice(2, 6)}-${value.slice(6)}`;
  } else if (value.length >= 3) {
    value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
  } else if (value.length > 0) {
    value = `(${value}`;
  }

  e.target.value = value;
});

document.querySelector("input#cnpj").addEventListener("input", function (e) {
  let value = e.target.value.replace(/\D/g, ""); // Remove caracteres não numéricos

  if (value.length > 14) {
    value = value.slice(0, 14); // Limita a 14 dígitos
  }

  // Formatação para o CNPJ completo (14 dígitos)
  if (value.length === 14) {
    value = `${value.slice(0, 2)}.${value.slice(2, 5)}.${value.slice(5, 8)}/${value.slice(8, 12)}-${value.slice(12, 14)}`;
  }

document.querySelectorAll("#valor").addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, ""); // Remove tudo que não for número

    if (value.length === 0) {
        e.target.value = ""; // Se estiver vazio, mantém em branco
        return;
    }

    // Se houver apenas centavos, adicionamos "0,"
    if (value.length === 1) {
        value = "0" + value;
    }

    // Obtém a parte inteira e os centavos
    let intPart = value.slice(0, -2) || "0"; // Parte inteira (ou "0" se não houver)
    let decimalPart = value.slice(-2).padStart(2, "0"); // Garante dois dígitos nos centavos

    // Formata com separadores de milhar
    intPart = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    e.target.value = `R$ ${intPart},${decimalPart}`;
});

  




