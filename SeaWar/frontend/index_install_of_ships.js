var  cookie_all = document.cookie.split(";");

let get_user_cookie = function(){
  let cookie_id;



  for (let i = 0; i < cookie_all.length; i++){
    if ( cookie_all[i].split('=')[0].replace( /\s/g, '') == 'id'){
        
        cookie_id = cookie_all[i].split('=')[1];
      }
    }
    return +cookie_id
}


const HOST = '';
var USER = get_user_cookie();
console.log("USER", USER);

var StoragUserIdName = "shots_enemy" + String(USER);
sessionStorage.setItem('shots_enemy', StoragUserIdName)
console.log(StoragUserIdName);
sessionStorage.setItem(StoragUserIdName, []);


function loadPage(){

   $.ajax({
                url: HOST + "/api/v1/ajax/get_id_game/" + USER + "/",
                type: "GET",
                success: function(data, output, status){
                    console.log("responce", data);
                    $("h1").text(data['game']);
                },

            });
}

var hidden_div_message = function(){

  $(".message").attr('hidden', 'true');
}

setTimeout(hidden_div_message, 50000);




function Ship(coordinates){
    this.coordinates = coordinates;
    this.hit_coordinates = [];
}
var arrDiv = document.querySelectorAll ('div');
var harborArr = [

    ];

var VALUE_DECK_SHIP = 0;
var SWITCH_BUTTON = true;
var arrShipsCoordunate = [];
var tempArr =[];
var number_of_ships = {
    "one_deck": 2,
    "two_deck": 1,
    "three_deck": 1,
    "four": 1,
}
    
var style_button;
var data_deck_name;
var e_target;

var ability_create = function(number_deck){
            if (number_of_ships[number_deck] <= 0) return false;
            return true;
}


var get_deck = function(e){
    if( SWITCH_BUTTON)
    {
        data_deck_name = e.target.getAttribute("data-deck-name");
        e_target = e.target;
       
        style_button = e_target.style;
        if (ability_create(data_deck_name))
        {
            VALUE_DECK_SHIP = e.target.getAttribute('data-deck');
            style_button.backgroundColor="red";
            e_target.innerHTML = (number_of_ships[data_deck_name] - 1) + ' кораблей';
            if ((number_of_ships[data_deck_name] - 1) == 0)
                     style_button.backgroundColor="grey";
            lenghtShip = 0;
        }

    }

        return false;
}

var button = $("button").bind('click', get_deck);
    

var check_ban_place = function(index1, data_pole){
        let index = +index1;
         let list_move = [
             index + 1, index - 1, index + 11, index - 11,
             index + 10, index - 10,
             index + 12, index - 12,
         ]; 
        
         for ( let i = 0; i < list_move.length; i++)
         {
             if ( list_move[i] < 140 ||  list_move[i] > 248)
                    list_move [i] = 139;
             if (arrDiv[list_move[i]].getAttribute('data-pole') != 2)
                    arrDiv[list_move[i]].setAttribute('data-pole', data_pole);
         }
    }


let lenghtShip = 0;
var givePlaceShips = function(e){
  SWITCH_BUTTON = false;
        
  if ( lenghtShip >= VALUE_DECK_SHIP){
    if ( VALUE_DECK_SHIP == 0) {
      info.innerText="Капитан выбери корабль";
      SWITCH_BUTTON = true;
      return;
    }
    
    info.innerText = "установка " + VALUE_DECK_SHIP + "-х палубного корабля " + "закончена";
    
    if ( arrShipsCoordunate.length != 0 ){
       harborArr.push( new Ship(arrShipsCoordunate));
       number_of_ships[data_deck_name] = number_of_ships[data_deck_name] - 1;
    }
   
    for ( let i = 0; i < tempArr.length; i++){              
      check_ban_place(tempArr[i], 2);          
    }
    arrShipsCoordunate = [];
    SWITCH_BUTTON = true;
    return false;
  }


 var coordinate = e.target.id;
        
  if(
      arrShipsCoordunate.length !=0 &&
      e.target.getAttribute("data-pole") == 3
  ){
      e.target.style.backgroundImage= "url('image/shipbig.png')";
      e.target.setAttribute("data-pole", 2);
      data_index = e.target.getAttribute("data-index");
      tempArr.push(data_index);
      arrShipsCoordunate.push(coordinate);
      check_ban_place(data_index, 3);
      lenghtShip += 1;
  }
        
        
                 
  if ( 
        e.target.getAttribute("data-pole") == 1 && 
        e.target.getAttribute("data-pole") != 2 && 
        arrShipsCoordunate.length == 0
     )
    {
        e.target.style.backgroundImage= "url('image/shipbig.png')";
        e.target.setAttribute("data-pole", 2);
        let data_index = e.target.getAttribute("data-index");
        tempArr.push(data_index);
        arrShipsCoordunate.push(coordinate);
        check_ban_place(data_index, 3);
        lenghtShip += 1;
    }   
 }

    
var get_funcm = function(){
  info.innerText = "Установите координаты корабля на игровом";
  for ( let i = 140; i < 249; i++ ){
    if (arrDiv[i].id != "numeral"){
       arrDiv[i].setAttribute("data-pole", 1);
       arrDiv[i].setAttribute("data-index", i);
       arrDiv[i].onclick = givePlaceShips;
    }      
 }}


get_funcm();




var img = $("img");




var headers  = {
'id': ''
};



var check_install_ships = function(){

  if (number_of_ships['one_deck'] == 0 && 
    number_of_ships['two_deck'] == 0 && 
    number_of_ships['three_deck'] == 0 && number_of_ships['four'] == 0 ){
    return true;
  }
  return false;
}


var get_name_user_next_move = function(){



    $.ajax({
                url: HOST + "/api/v1/ajax/get_current_move/",
                type: "GET",
                success: function(data, output, status){
                    console.log("responce", data);
                    console.log("type", typeof(data));
                    console.log("user_id", USER);



                    let data_next_move = JSON.parse(data);
                    console.log(data_next_move)
                    console.log("type", typeof(+data_next_move['current_move']))
                    if (+data_next_move['current_move'] == USER){
                        $("#info").text("Ходи Капитан");
                      }
                    else{
                      $("#info").text("Сейчас выстрел противника");
                    }
                },

            });
}


let ready = function(){
  
  if (check_install_ships()){
    
    $.ajax({
            url: HOST + "/api/v1/ajax/update_user/" + USER + "/",
            type: "PATCH",
            data: {
                    "ship": JSON.stringify(harborArr),
                    "status": 1,
                   },
            headers: {
                     "id": USER,
            },
            success: function(data, output, status){
                console.log("request suссessfull", data);
                get_name_user_next_move();
            },
        });
}

  setInterval(get_set_shots_enemy_user, 1000);
}

    

img.on("click", ready);



