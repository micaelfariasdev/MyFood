let trilho = document.getElementById("trilho");
let body = localStorage.getItem("darkmode");

const enableDarkmode = () => {
  document.body.classList.add("darkmode");
  localStorage.setItem("darkmode", "active");
};

const disableDarkmode = () => {
  document.body.classList.remove("darkmode");
  localStorage.setItem("darkmode", "inactive");
};

// Verifica o estado do darkmode ao carregar a página
if (body === "active") {
  enableDarkmode();
} else {
  disableDarkmode();
}

// Alterna entre os modos de tema
trilho.addEventListener("click", () => {
  if (document.body.classList.contains("darkmode")) {
    trilho.classList.toggle("dark");
    disableDarkmode();
  } else {
    trilho.classList.toggle("dark");
    enableDarkmode();
  }
});

document
  .querySelector("input#telefone")
  .addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, "");

    if (value.length > 11) {
      value = value.slice(0, 11); // Limita a 11 dígitos
    }

    
    if (value.length === 11) {
      value = `(${value.slice(0, 2)}) ${value.slice(2, 3)} ${value.slice(
        3,
        7
      )}-${value.slice(7, 11)}`;
    } else if (value.length >= 7) {
      value = `(${value.slice(0, 2)}) ${value.slice(2, 6)}-${value.slice(6)}`;
    } else if (value.length >= 3) {
      value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
    } else if (value.length > 0) {
      value = `(${value}`;
    }

    e.target.value = value;
  });

document.addEventListener("DOMContentLoaded", function () {
  // Exibe o conteúdo "Cursos" por padrão ao carregar a página
  let cursos = document.getElementById("cursos");
  cursos.style.display = "block"; // Exibe a seção de cursos inicialmente

  // Função para exibir o conteúdo correspondente ao menu
  document.querySelectorAll(".menulat a").forEach((item) => {
    item.addEventListener("click", function (event) {
      event.preventDefault(); // Impede o comportamento de navegação padrão

      // Pega o ID do conteúdo a ser exibido
      let targetId = item.getAttribute("data-target");
      let targetContent = document.getElementById(targetId);

      // Esconde todos os conteúdos
      document.querySelectorAll(".conteudos").forEach((content) => {
        content.style.display = "none";
      });

      // Exibe o conteúdo selecionado
      targetContent.style.display = "block";
    });
  });
});

function dash(a) {
  let hash = a; // Pega o hash da URL
  let cursos = document.querySelector("#cursos");
  let habilidade = document.querySelector("#habilidades");

  // Mostra ou esconde o conteúdo baseado no hash
  if (hash === "#curso") {
    cursos.style.display = "grid";
  } else {
    cursos.style.display = "none";
  }

  if (hash === "#habilidade") {
    habilidade.style.display = "grid";
  } else {
    habilidade.style.display = "none";
  }
}

function insert(a) {
  let bnt = document.querySelector(a);
  
  bnt.style.display = (bnt.style.display === "none" || bnt.style.display === "") ? "flex" : "none";
}
