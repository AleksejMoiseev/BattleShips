const HOST = '';


let create_user_game = function(){

    $.ajax({
        url: HOST + "/api/v1/ajax/createuser/",
        type: "POST",
        headers: headers,
        data: {
                "name": $("#usercreate").val(),
               },
        success: function(data, output, status){
            getAllHeaders = status.getAllResponseHeaders();
            headers_request = create_dict_of_headers(getAllHeaders);
            if ( status.status >199 && status.status < 300)
                document.location.href = 'index.html';
          

            
        },
    });
         
}



let bind_game = function(){ 



    $.ajax({
            url: HOST + "/api/v1/ajax/user/",
            type: "POST",
            headers: headers,
            data: {
                    "name": $("#useradd").val(),
                    "ship": "{}",
                    "game": $("#inputkey").val(),
                   },
            success: function(data, output, status){
                getAllHeaders = status.getAllResponseHeaders();
                headers_request = create_dict_of_headers(getAllHeaders);
                if ( status.status >199 && status.status < 300)
                    document.location.href = 'index.html';


            }

        });

}


    $("button[data-gamecreare]").on('click', create_user_game);
    $("button[data-userAdd]").on('click', bind_game);
    
    
    