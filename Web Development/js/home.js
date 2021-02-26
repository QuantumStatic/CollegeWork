var index = Math.floor(Math.random() * 3);

function promotionSet(){
  var promotionHeads = [
    'Breakfast Time Special Offer:',
    'Lunch Time Special Offer:',
    'Dinner Time Special Offer:'
  ];
  var promotionSubHeads = [
    '$144 Margarita, 4 Drinks',
    '$188 Sushi Set, 12 Pieces',
    'Dessert only for 40$'
  ];

  document.querySelector('#promotion > h2').innerHTML = promotionHeads[index % 3];
  document.querySelector('#promotion > h3').innerHTML = promotionSubHeads[index % 3];
  index++;
}

function promotionCycle(){
  promotionSet();
  setInterval(promotionSet, 3000);
}

function vidSwitch(){
  var vid = document.querySelector('video');
  vid.pause();
  if (document.querySelector('source[type=\'video/mp4\']').src == "https://courses.cs.cityu.edu.hk/cs2204/barbecue.mp4"){
    document.querySelector('source[type=\'video/mp4\']').src = 'https://courses.cs.cityu.edu.hk/cs2204/cakemaking-s.mp4';
    document.querySelector('source[type=\'video/ogg\']').src = 'https://courses.cs.cityu.edu.hk/cs2204/cakemaking-s.ogg';
    vid.load();
  }
  else{
    document.querySelector('source[type=\'video/mp4\']').src = 'https://courses.cs.cityu.edu.hk/cs2204/barbecue.mp4';
    document.querySelector('source[type=\'video/ogg\']').src = 'https://courses.cs.cityu.edu.hk/cs2204/barbecue.ogg';
    vid.load();
  }
  vid.play();
}

function checkFormEmpty(){
  var valueofdate = document.querySelector('input[name="date"]').value;
  var valueofGuestno = document.querySelector('input[name="guestno"]').value;

  if (!valueofdate || !valueofGuestno){
    document.querySelector('#Err').style.display = 'block';
    document.querySelector('#msg-1').style.display = 'none';
    document.querySelector('#msg-2').style.display = 'none';
    return true;
  }
  else{
    document.querySelector('#Err').style.display = 'none';
    return false;
  }
}

function clearError() {
  document.querySelector('#Err').style.display = 'none';
}

function init(){
  promotionCycle();
  clearError();

  document.querySelector('#msg-1').style.display = 'none';
  document.querySelector('#msg-2').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function(){
  document.body.addEventListener('load', init());
});
