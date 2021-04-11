//import User1
//console.log(USER1)

//var csrftoken = getCookie('csrftoken');
//console.log("crfdddddddddd");

const HOST = 'http://battleships.lo';

    function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.getResponseHeader);
      console.log(this.response);
      console.log(this.getAllResponseHeaders("Set-Cookie"));
    }
  };
        
  xhttp.open("POST", HOST + "/api/v1/ajax/createuser/", true);
let input = $("#usercreate");
let form = new FormData(input);
  xhttp.send();
}



    let create_user_game = function(){
    
            $.ajax({
                url: HOST + "/api/v1/ajax/createuser/",
                type: "POST",
                data: {
                        "name": $("#usercreate").val(),
                       },
                success: function(data, output, status){
                    console.log("request suссessfull", data);
                    console.log("request suссessfull", status.getResponseHeader("Set-Cookie"));
                    console.log("request suссessfull", status.getAllResponseHeaders());
                    console.log("coookie", document.cookie.split(";"));
                    console.log(data['id']);
                  

                    
                },
            });
//                 setTimeout(
//                function(){
//                document.location.href = 'index.html';
//                }, 
//                3 * 1000
//                 );
        
               
    }
    
    let bind_game = function(){
        
         $.post(
            
            HOST + "/api/v1/ajax/user/",
                {
                    "name": $("#useradd").val(),
                    "ship": "{}",
                    "game": $("#inputkey").val(),
                },
            function(data, output, status){
                console.log("data", data);
                console.log("output", output);
                console.log("status", status);
                console.log("status", status.getAllResponseHeaders());
                USER2 = data['id'];
                console.log(USER2);
            }
            
            
            );
        
//            setTimeout(
//                function(){
//                document.location.href = 'index.html';
//                }, 
//                3 * 1000
//            );

        
        console.log($("#useradd").val());
        console.log($("#inputkey").val());
        console.log("coookie", document.cookie)
//       document.location.href = 'index.html';
    }

    $("button[data-gamecreare]").on('click', create_user_game);
    $("button[data-userAdd]").on('click', bind_game);
    
    
    