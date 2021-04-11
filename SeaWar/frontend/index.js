function contains(arr, elem) {
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] === elem) {
            return true;
        }
    }}
    var messangArr = [];
        messangArr[0] = "Вот это шарахнуло, ранил чорт возьми";
        messangArr[1] = "Полундра свистать всех на верх ранили";
        messangArr[2] = "Чертово пекло ранение";
        messangArr[3] = "Отличный выстрел, соколиный глаз";
        messangArr[4] = "Попал, ранил";
function randChoice (){
   var randvalue = Math.floor ( Math.random() * 5 );
   return randvalue;
}

function wound (){
   var randWound = randChoice ();
   var coordinateWound = messangArr[ randWound ];
   return coordinateWound;
}

function soundClick() {
    var audio = new Audio(); // Создаём новый элемент Audio
    audio.src = 'media/V.mp3'; // Указываем путь к звуку "клика"
    audio.autoplay = true; // Автоматически запускаем
    }

function soundClickPast() {
    var audio = new Audio();
    audio.src = 'media/soundPast.mp3';
    audio.autoplay = true;
}
function output ( value ){
    if ( value == 'killed') {
        info.innerText = "Убит";
        soundClick();
    }
    else if ( value == 'ranen') {
        info.innerText = wound();
        soundClick();
    }
    else {
        info.innerText = "Промах";
        soundClickPast();
    }
}
//function Ship(coordinates){
//    this.coordinates = coordinates;
//    this.hit_coordinates = [];
//}
    
    
 var fire = function ( e ) {
    var coordinate = e.target.id;
    if (contains ( arrShots, coordinate)) {
        return;
    }
     
    arrShots.push(coordinate);
     
    for ( var i = 0; i < harborArr.length; i++ ){
        var ship = harborArr[i];
        var hit_result = check_hit(ship, coordinate);
        output(hit_result);
        if ( hit_result == "ranen" || hit_result == "killed" ){
             e.target.style.backgroundImage = "url('image/scelet.png')";
             break;
        } 
        else{
             e.target.style.backgroundImage = "url('image/krest.png')";
        }
    }
}
 function check_hit(ship, coordinate) {
    if (!(contains ( ship.coordinates, coordinate))) {
        return 'mimo'
    }

    if (!contains ( ship.hit_coordinates, coordinate)) {
        ship.hit_coordinates.push(coordinate)
    }

    if (ship.coordinates.length == ship.hit_coordinates.length) {
        return 'killed'
    }

    return 'ranen'
}
    
    
    var harborArr = [
//    new Ship (['A1']),
//    new Ship (['A3', 'A4']),
//    new Ship (['A9', 'B9', 'C9'])
    ];
    var arrShots =[];
//    var arrDiv = document.querySelectorAll ('div');
    for ( let i = 16; i < 125; i++ ){
        if (arrDiv[i].id != "numeral"){
            arrDiv[i].onclick = fire;
        }
        
    }

// Функция описывающая свое поле

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

    var ability_create = function(number_deck)
    {
                if (number_of_ships[number_deck] <= 0) return false;
                return true;
    }


    var get_deck = function(e)
    {
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
    

    var check_ban_place = function(index1, data_pole)
    {
        let index = +index1;
         let list_move = [
             index + 1, index - 1, index + 11, index - 11,
             index + 10, index - 10,
             index + 12, index - 12,
         ]; 
        
         for ( let i = 0; i < list_move.length; i++)
         {
             if ( list_move[i] < 138 ||  list_move[i] > 246)
                    list_move [i] = 137;
             if (arrDiv[list_move[i]].getAttribute('data-pole') != 2)
                    arrDiv[list_move[i]].setAttribute('data-pole', data_pole);
         }
    }

    let lenghtShip = 0;
    var givePlaceShips = function(e)
    {
        SWITCH_BUTTON = false;
        if ( lenghtShip >= VALUE_DECK_SHIP)
        {
            if ( VALUE_DECK_SHIP == 0) 
            {
                info.innerText="Капитан выбери корабль";
                SWITCH_BUTTON = true;
                return;
            }
            
            info.innerText = "установка " + VALUE_DECK_SHIP + "-х палубного корабля " + "закончена";
            
            if ( arrShipsCoordunate.length != 0 )
            {
                 harborArr.push( new Ship(arrShipsCoordunate));
                 number_of_ships[data_deck_name] = number_of_ships[data_deck_name] - 1;
            }
           
            for ( let i = 0; i < tempArr.length; i++)
            {              
                check_ban_place(tempArr[i], 2);          
            }
            arrShipsCoordunate = [];
            SWITCH_BUTTON = true;
            return false;
        }
             var coordinate = e.target.id;
        
        if
        (
            arrShipsCoordunate.length !=0 &&
            e.target.getAttribute("data-pole") == 3
        )
        {
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
    
    var get_funcm = function()
    {
     info.innerText = "Установите координаты корабля на игровом поле";
     for ( let i = 138; i < 247; i++ )
     {
          if (arrDiv[i].id != "numeral")
          {
             arrDiv[i].setAttribute("data-pole", 1);
             arrDiv[i].setAttribute("data-index", i);
             arrDiv[i].onclick = givePlaceShips;
          }      
     }
        
    }


    get_funcm();

var img = $("img");
var USER = 10;

console.log(JSON.stringify(harborArr));
    let ready = function(){
        
        $.ajax({
                url: "http://127.0.0.1:8000/api/v1/ajax/update_user/" + USER + "/",
                type: "PATCH",
                data: {
                        "ship": JSON.stringify(harborArr),
                        "status": 1,
                       },
                success: function(data, output, status){
                    console.log("request suссessfull", data);
                },
            });
    }

    

img.on("click", ready);






