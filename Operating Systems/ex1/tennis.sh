#!bin/bash/
#Tamar Saad 207256991
#tennis.sh

#initialize the variables
game_on=true
first_round=true
ball_in_0=true
ball_location=0
points_1=50
points_2=50
guess_1=0
guess_2=0

#print the board
print_board() {
    echo -e " Player 1: ${points_1}         Player 2: ${points_2} "
    echo -e " --------------------------------- "
    echo -e " |       |       #       |       | "
    echo -e " |       |       #       |       | "
    #the middle row with the ball
    case $ball_location in
        "-3")
        echo -e "O|       |       #       |       | "
        ;;
        "-2")
        echo -e " |   O   |       #       |       | "
        ;;
        "-1")
        echo -e " |       |   O   #       |       | "
        ;;
        0) 
        echo -e " |       |       O       |       | "
        ;;
        1)
        echo -e " |       |       #   O   |       | "
        ;;
        2)
        echo -e " |       |       #       |   O   | "
        ;;
        3)
        echo -e " |       |       #       |       |O "
        ;;
        *)
        echo -e "error in case"
        ;;
    esac
    echo -e " |       |       #       |       | "
    echo -e " |       |       #       |       | "
    echo -e " --------------------------------- "
    if [ $first_round = false ]; then
        echo -e "       Player 1 played: ${guess_1}\n       Player 2 played: ${guess_2}\n\n"
    fi
}

move() {
    number1=$1
    number2=$2
    #if the first player won
    if [ $(($number1 - $number2)) -gt 0 ]; then
        winner='-1'
    #if the second player won
    elif [ $(($number1 - $number2)) -lt 0 ]; then
        winner=1
    #if it's a tie
    else
        winner=0
    fi
    #check if the ball is in the correct side of the field
    if [ $(($winner * $ball_location)) -gt 0 ]; then
    #the ball is in the winner's field and we need to transfer it
        ball_location=$((-1*$winner))
        ball_in_0=false
    elif [ $(($winner * $ball_location)) -lt 0 ]; then
    #the ball is the loser's field and we need to take it further
        ball_location=$(($ball_location - $winner))
        ball_in_0=false
    #if the result is 0- there was a tie and the ball doesn't move, or it's the beggining
    #of the game and the ball hasn't moved yet
    elif [ $ball_in_0 = true ]; then 
        ball_location=$((-1*$winner))
    fi
    points_1=$(($points_1 - $guess_1))
    points_2=$(($points_2 - $guess_2))
    first_round=false
}

get_input_from_players() {
    #get the first player's guess
    echo -e "PLAYER 1 PICK A NUMBER: "
    read -s number1
    #input check
    while :
     do
        if [[ $number1 =~ ^[0-9]+$ ]] && [ $number1 -le $points_1 ] && [ $number1 -ge 0 ]; then
            break
        else
            echo -e "NOT A VALID MOVE !"
            echo -e "PLAYER 1 PICK A NUMBER: "
            read -s number1
        fi
    done
    #get the second player's guess
    echo -e "PLAYER 2 PICK A NUMBER: "
    read -s number2
    #input check
    while :
     do
        if [[ $number2 =~ ^[0-9]+$ ]] && [ $number2 -le $points_2 ] && [ $number2 -ge 0 ]; then
            break
        else
            echo -e "NOT A VALID MOVE !"
            echo -e "PLAYER 2 PICK A NUMBER: "
            read -s number2
        fi
    done
    #update the last gusses
    guess_1=$number1
    guess_2=$number2
    #call to move function
    move $number1 $number2
}


check_victory() {
    win=none
    #if the ball is outside- we have a winner
    if [ $ball_location == 3 ]; then
        win=player_1
    elif [ $ball_location == -3 ]; then
        win=player_2
        #if only one of the players has 0 points- the other one wins
        #if both have 0- the one that doesn't have the ball wins
    elif [ $points_1 == 0 ]; then
        if [ $points_2 == 0 ]; then
            if [ $ball_location -gt 0 ]; then
                win=player_1
            elif [ $ball_location -lt 0 ]; then
                win=player_2
            else 
                win=tie
            fi
        else
            win=player_2
        fi
    elif [ $points_2 == 0 ]; then
        win=player_1
    fi
    #if we have a winner
    if [ $win != "none" ]; then
        game_on=false
        print_board
        if [ $win == "player_1" ]; then
            echo -e "PLAYER 1 WINS !"
        elif [ $win == "player_2" ]; then
            echo -e "PLAYER 2 WINS !"
        else 
            echo -e "IT'S A DRAW !"
        fi
    fi
}

#running the game
while $game_on
do
    print_board
    get_input_from_players
    check_victory
done