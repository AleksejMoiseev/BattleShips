console.log(headers);
const HOST = 'http://battleships.lo';


    let create_user_game = function(){
    
            $.ajax({
                url: HOST + "/api/v1/ajax/createuser/",
                type: "POST",
                headers: headers,
                data: {
                        "name": $("#usercreate").val(),
                       },
                success: function(data, output, status){
                    console.log("request suссessfull", data);
                    
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
                    cookie_all = document.cookie.split(";")[1].split('=');
                    headers['id'] = cookie_all[1];
                    console.log("request suссessfull", data);
                    console.log("request suссessfull", headers);
                    getAllHeaders = status.getAllResponseHeaders();
                    headers_request = create_dict_of_headers(getAllHeaders);
                    console.log("header = ",  headers_request);
                    console.log("headers_request id", headers_request.get('id'));
                    console.log('cookie_all', cookie_all);
                    console.log('cookie_all', cookie_all[1]);
                    console.log(data['id']);
                    console.log("headers_id", headers["id"]);
                    console.log('status', output);
                    console.log('status',status.status);
                    if ( status.status >199 && status.status < 300)
                        document.location.href = 'index.html';


                }

            });

    }


//          $.post(
            
//             HOST + "/api/v1/ajax/user/",
//                 {
//                     "name": $("#useradd").val(),
//                     "ship": "{}",
//                     "game": $("#inputkey").val(),
//                 },
//             function(data, output, status){
//                 console.log("data", data);
//                 console.log("output", output);
//                 console.log("status", status);
//                 console.log("status", status.getAllResponseHeaders());
//                 USER2 = data['id'];
//                 console.log(USER2);
//             }
            
            
//             );
        
// //            setTimeout(
// //                function(){
// //                document.location.href = 'index.html';
// //                }, 
// //                3 * 1000
// //            );

        
//         console.log($("#useradd").val());
//         console.log($("#inputkey").val());
//         let cookieid = document.cookie[2];
//         console.log('cookieid', cookieid);
//         console.log("coookie", document.cookie);
// //       document.location.href = 'index.html';
    

    $("button[data-gamecreare]").on('click', create_user_game);
    $("button[data-userAdd]").on('click', bind_game);
    
    
    