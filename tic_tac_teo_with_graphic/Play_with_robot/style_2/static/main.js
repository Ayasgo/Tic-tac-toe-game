player_can_choose = true;
game_over = false;
$(document).ready(function(){
    $(".box").click(function(){
        if(game_over) return;
        let chosen_box = $(this).find('.atvImg-rendered-layer').eq(1);
        if( !player_can_choose | chosen_box.attr('style').indexOf('url("")') === -1) return;
        player_can_choose = false;

        let player_move = $(this).attr("name");	
        let boxes = $(".box").toArray();
        let text_info = $("#text_info");

        // filling the board array
        let board=[];
        boxes.forEach(element => {
            let img = $(element).find('.atvImg-rendered-layer').eq(1);
            if (img.attr('style').indexOf(robotImgSrc) !== -1) board.push(1);
            else if(img.attr('style').indexOf(playerImgSrc) !== -1) board.push(2);
            else board.push(0);
        });
        let data = JSON.stringify({
            'player_move': player_move,
            'board': board,
        })
        
        // changing the text info and the clicked img
        text_info.text('Thinking...');
        chosen_box.attr('style',chosen_box.attr('style').replace('""','"'+playerImgSrc+'"'));

        $.ajax({
            'url': '/',
            'method': 'POST',
            'contentType': "application/json; charset=utf-8",
            'dataType' : 'json', // The expected data type
            'data': data,
            'success' : function(resonse){
                // changing the text info
                text_info.text('Choose your move');
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
                        let img = $(boxes[i]).find('.atvImg-rendered-layer').eq(1);
                        if(symbol == 1)  img.attr('style',img.attr('style').replace('""','"'+robotImgSrc+'"'));
                        else if(symbol == 2) img.attr('style',img.attr('style').replace('""','"'+playerImgSrc+'"'));
                        else {
                            img.attr('style', 'background-image: url(""); transform: translateX(-0.179688px) translateY(-0.0644531px);');
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
                        text_info.text("A draw!");
                    } else {
                        for( box_index of winning_combination){
                            $(boxes[box_index]).addClass('oscillating-image');
                        };
                        if( winner == 'bot' ){
                            text_info.text("Bot wins!");
                        } else{
                            text_info.text("You wins!");
                        };
                    };
                    text_info.text( text_info.text() + " New game?");
                    text_info.css('cursor', 'pointer');
                };
            },
            'error' : function(xhr, status, error){
                console.log(error);
            },
        });
    });
});