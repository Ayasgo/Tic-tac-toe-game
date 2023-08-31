from classes.game import *

if __name__ == '__main__':
    game=Game()
    while True:
        print(
        """
        ----------------------------------------------
        0. To quit the game.
        1. To play with the robot in the ia mode.
        2. To play with the robot in the ramdom mode.
        3. To play with your friend
        4. Robot vs robot in the ia mode.
        5. Robot vs robot in the ramdom mode.
        ----------------------------------------------

        """)
        choice=input("Enter your choice: ")
        
        match choice:
            case '0':
                break
            case '1':
                game.robot_vs_player_ai_mode()
            case '2':
                game.robot_vs_player_random_mode()
            case '3':
                game.player_vs_player()
            case '4':
                game.robot_vs_robot_ai_mode()
            case '5':
                game.robot_vs_robot_random_mode()
            case default:
                print("Invalid choice!")

    


