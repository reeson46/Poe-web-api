$(document).ready(function(){

    $(".characterWindow").click(function(){
         $.ajax({
            url: 'https://www.pathofexile.com/character-window/get-items?accountName=R33son&character='+ $(this).attr('value'),
            headers : {'User-Agent': 'Mozilla/5.0 '},
            cookies : {'POESESSID': '16418e854515def66e5d3a14c74bfc6a'},
            type: 'GET',
            dataType: 'json',
            success: function(res){
                console.log(res);
            }
        });

    });

});