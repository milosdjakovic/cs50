const colors = [
  '#ADADFF',
  '#A9A6C9',
  '#9FB4C7',
  '#84B4D7',
  '#9FB798'
];

function main() {
  const navbarBrandElement = document.querySelector('.navbar-brand');

  if (!navbarBrandElement) return

  let index = 0;

  navbarBrandElement.style.background = colors[index % colors.length];
  setInterval(function() {
    navbarBrandElement.style.background = colors[index % colors.length];
    index++;
  }, 1000);
}

document.addEventListener('DOMContentLoaded', main);
