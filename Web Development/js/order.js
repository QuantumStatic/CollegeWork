var menu = {
  "Sushi 1": "Nigiri Sushi ",
  "Sushi 2": "Sashimi Sushi",
  "Sushi 3": "Maki Sushi",
  "Sushi 4": "Temaki Sushi",
  "Drink 1": "Fresh Grapefruit Pomegranate Margarita",
  "Drink 2": "Peach Margarita",
  "Drink 3": "Blackberry Grapefruit Margarita",
  "Dessert 1": "Raspberry Tuxedo Cheesecake"
};
document.addEventListener("DOMContentLoaded", function() {
  document.querySelector("#total_quantity").innerText = recal();
  document.querySelector("div.menu-section.sushi").style.display =
    "inline-block";
  document.querySelector("h3.menu-section.sushi").style.backgroundColor =
    "white";
var divisionHeaders = document.querySelectorAll("h3.menu-section");

  var menuSwitch = function(){
    this.style.backgroundColor = "white";
    var divisionHeaders = document.querySelectorAll("h3.menu-section");
    for (var j = 0; j < divisionHeaders.length; j++) {
      if (divisionHeaders[j] !== this) {
        divisionHeaders[j].style.backgroundColor = "#eb939c";
      }
    }

    var divisionName = this.className;
      var divisions = document.querySelectorAll("div.menu-section");
      for (var x = 0; x < divisions.length; x++) {
        if (divisions[x].className === divisionName) {
          divisions[x].style.display = "inline-block";
        } else {
          divisions[x].style.display = "none";
        }
      }
    };
    for (var i = 0; i < divisionHeaders.length; i++) {
      divisionHeaders[i].addEventListener('click', menuSwitch);
     }

  var buttons = document.querySelectorAll('input[name="submit"]');
  var addItem = function(){
    var row = document.querySelector("tbody").insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);

    cell1.className = "desc";
    cell2.className = "qty";

    cell1.innerHTML =
      menu[this.previousElementSibling.previousElementSibling.alt];
    cell2.innerHTML = this.previousElementSibling.value;
    document.querySelector("#total_quantity").innerText = recal();
  };
  for (var y = 0; y < buttons.length; y++) {
    buttons[y].addEventListener('click', addItem);
  }
});

function recal() {
  var sum = 0;
  var quantities = document.querySelectorAll("td.qty");
  for (var i = 0; i < quantities.length; i++) {
    sum += parseInt(quantities[i].innerText);
  }

  console.log(sum);
  return sum;
}

function undo() {
  document.querySelector("tbody").deleteRow(-1);
  document.querySelector("#total_quantity").innerText = recal();
}
