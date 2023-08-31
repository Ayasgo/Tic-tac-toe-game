player_can_choose = true;
game_over = false;
$(document).ready(function(){
    $(".box").click(function(){
        if(game_over) return;
        chosen_box = $(this).find("img")
        if( !player_can_choose | chosen_box.attr('src') !== undefined) return;
        player_can_choose = false;

        let player_move = $(this).attr("name");	
        let boxes = $(".box").toArray();
        let text_info = $("#text_info");

        // filling the board array
        let board=[];
        boxes.forEach(element => {
            let img = $(element).find('img');
            if (img.attr('src') === robotImgSrc) board.push(1);
            else if(img.attr('src') === playerImgSrc) board.push(2);
            else board.push(0);
        });
        let data = JSON.stringify({
            'player_move': player_move,
            'board': board,
        })
        
        // changing the text info and the clicked img
        let loaders_points = $(".loader__element").toArray();
        text_info.text('Thinking');
        loaders_points.forEach(element =>{
            $(element).show();
        });
        chosen_box.attr('src', playerImgSrc);
        chosen_box.show();

        $.ajax({
            'url': '/',
            'method': 'POST',
            'contentType': "application/json; charset=utf-8",
            'dataType' : 'json', // The expected data type
            'data': data,
            'success' : function(resonse){
                // changing the text info
                text_info.text('Choose an empty box');
                loaders_points.forEach(element =>{
                    $(element).hide();
                });
                player_can_choose = true;
                // uploading the data arguments
                let is_terminal = resonse.is_terminal,
                    winner = resonse.winner,
                    winning_combination = resonse.winning_combination,
                    new_board = resonse.new_board;
                
                // filling boxes with images
                for (let i = 0; i < board.length; i++) {
                    if (board[i] !== new_board[i]){
                        console.log(new_board);
                        let symbol = new_board[i];
                        let img = $(boxes[i]).find('img');
                        $(img).show();
                        if(symbol == 1)  img.attr('src', robotImgSrc);
                        else if(symbol == 2) img.attr('src', playerImgSrc);
                        else {
                            img.attr('src', undefined);
                            $(img).hide();
                        };
                    };
                };
                // checking if the game is over
                if(is_terminal){
                    game_over = true;
                    // reloading the game
                    text_info.click(function(){
                        location.reload();
                    });
                    if(winner === 'tie'){
                        text_info.text("It's a draw !");
                    } else {
                        for( box_index of winning_combination){
                            $(boxes[box_index]).find('img').addClass('oscillating-image');
                        };
                        if( winner == 'bot' ){
                            text_info.text("The bot wins !");
                        } else{
                            text_info.text("You wins !");
                        };
                    };
                    text_info.text( text_info.text() + "  Play Again ?");
                    text_info.css('cursor', 'pointer');
                };
            },
            'error' : function(xhr, status, error){
                console.log(error);
            },
        });
    });
});