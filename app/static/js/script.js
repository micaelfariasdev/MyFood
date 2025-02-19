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
  

  e.target.value = value; // Atualiza o valor do campo de entrada
});




