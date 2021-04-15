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



var check;
var check_move = function(e){

   

    $.ajax({
                url: HOST + "/api/v1/ajax/get_current_move/",
                type: "GET",
                success: function(data, output, status){
                    console.log("responce", data);
                    console.log("type", typeof(data));
                    console.log("user_id", USER);
                    if (USER == +data){
                        console.log('выстрел');
                        fire(e);
                    }
                    else{
                        console.log("не твой ход");
                    }
                },
            });

}


$("#check").on('click', check_move) 
    
 var fire = function ( e ) {


    var coordinate = e.target.id;
    console.log(coordinate);
    if (contains ( arrShots, coordinate)) {
        return;
    }
    arrShots.push(coordinate);
     
     
     
      $.ajax({
                url: HOST + "/api/v1/ajax/faire/",
                type: "POST",
                data: {
                        "coordinate": coordinate,
                       },
                success: function(data, output, status){
                    console.log("request suссessfull", data);
                },
            });
     
     
     
     
     
     
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
    
    
//    var harborArr = [
////    new Ship (['A1']),
////    new Ship (['A3', 'A4']),
////    new Ship (['A9', 'B9', 'C9'])
//    ];
    var arrShots =[];
//    var arrDiv = document.querySelectorAll ('div');
    for ( let i = 16; i < 125; i++ ){
        if (arrDiv[i].id != "numeral"){
            // arrDiv[i].onclick = fire;
            arrDiv[i].onclick = check_move;

        }
        
    }
