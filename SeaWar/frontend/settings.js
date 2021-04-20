var headers  = {
'id': ''
};

var headers_request;

var cookie_all;



var getAllHeaders;


var create_dict_of_headers = function(counter){
        var arrHeader = [];
        let arrCounter = counter.split('\n');


        for (var i = 0; i < arrCounter.length; i++) {
            arrHeader.push(arrCounter[i].split(':'));
        }

        return new Map(arrHeader);
    }