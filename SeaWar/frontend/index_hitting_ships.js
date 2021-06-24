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
//var col = document.getElementById('V');
//var soundPast = document.getElementById('soundPast');

function soundClick() {
     var audio = new Audio(); // Создаём новый элемент Audio
     audio.src = 'media/V.mp3'; // Указываем путь к звуку "клика"
     audio.autoplay = true; // Автоматически запускаем
//    col.play();
    }

function soundClickPast() {
     var audio = new Audio();
     audio.src = 'media/soundPast.mp3';
     audio.autoplay = true;
//    soundPast.play();
}

function soundClickBoom() {
    var audio = new Audio();
    audio.src = 'media/vzryv.mp3';
    audio.autoplay = true;
}

function output ( value ){
    if ( value == 'killed') {
        info.innerText = "Убит";
        soundClickBoom();
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


var show_hit = function(coordinate){

    t = ".second #"+coordinate;

    for ( var i = 0; i < harborArr.length; i++ ){
        var ship = harborArr[i];
        var hit_result = check_hit(ship, coordinate);
         output(hit_result);
        if ( hit_result == "ranen" || hit_result == "killed" ){
             $(".second #"+coordinate).css('background-image', "url('image/scelet.png')");
             break;
        } 
        else{
             $(".second #"+coordinate).css('background-image', "url('image/krest.png')");
        }
    }


}



var check;
var check_move = function(e){

        $.ajax({
                    url: HOST + "/api/v1/ajax/get_current_move/",
                    type: "GET",
                    success: function(data, output, status){
                        let data_cuurent_move = JSON.parse(data);
                        if (+data_cuurent_move['current_move'] == USER){
                            $("#info").text("Выстрел");
                            fire(e);
                            // setTimeout(get_set_shots_enemy_user, 1000);
                        }
                        else if (+data_cuurent_move['status'] == 0){
                            $("#info").text("Игра Окончена: Победитель - " + data_cuurent_move['winner']);

                        }
                        else{
                            $("#info").text("Ходит противник");
                        }
                    },
                });

}




var get_set_shots_enemy_user = function(){


        $.ajax({
                url: HOST + "/api/v1/ajax/get_shots_enemy/",
                type: "GET",
                success: function(data, output, status){
                    let set_enemy = JSON.parse(data);
                    let sessionStoragUserId = sessionStorage.getItem('shots_enemy');
                    let arrB = sessionStorage.getItem(sessionStoragUserId);
                    let difference = set_enemy.filter(x => !arrB.includes(x));
                    if ( difference != 0){
                        sessionStorage.setItem(sessionStoragUserId, set_enemy);
                        let coordinate_enemy_shot = difference[0];
                        show_hit(coordinate_enemy_shot);
                    }

                },
            });

}

var arrShots =[];
   
var fire = function ( e ) {
    var coordinate = e.target.id;
    do{
        $("#info").text("Капитан твой выстрел");
    }while (contains ( arrShots, coordinate))
    arrShots.push(coordinate);
    $(".first #"+coordinate).css('background-image', "url('image/hourglass.png')");
    soundClick();
     
        $.ajax({
                url: HOST + "/api/v1/ajax/faire/",
                type: "POST",
                data: {
                        "coordinate": coordinate,
                       },
                success: function(data, output, status){
                    let hitResult = JSON.parse(data);
                    if (hitResult['hit_result'] == 'mimo'){
                        $(".first #"+coordinate).css('background-image', "url('image/krest.png')");
                        $("#info").text("Стреляет противник");
                    }
                    else if (hitResult['hit_result'] == 'ranen' || hitResult['hit_result'] == 'killed'){
                        $(".first #"+coordinate).css('background-image', "url('image/bum.png')");
                        $("#info").text("Капитан твой выстрел");
                    }
                    else if (hitResult['hit_result'] == 'win'){
                        $(".first #"+coordinate).css('background-image', "url('image/bum.png')");
                        $("#info").text("Ура победа: Победитель: " + hitResult['winner']);
                    }
                },
            });
   
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
    

for ( let i = 16; i < 125; i++ ){
    if (arrDiv[i].id != "numeral"){
        // arrDiv[i].onclick = fire;
        arrDiv[i].onclick = check_move;
    } 
}
