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
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById('codigo').disabled = true;
});

