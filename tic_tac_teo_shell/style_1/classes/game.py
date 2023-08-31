from .board import Board
from .constants import *
from .robot import Robot
from random import choice

class Game:
    def __init__(self):
        self.robot_symbole=1 # =1 if the robot will play with 'x' elif 2 if it will play with 'o'
        self.player=1 # indicate which player will play at this turn
        self.bd=Board() 
        self.robot1=Robot(1) #if robot vs robot mode
        self.robot2=Robot(2) #if robot vs robot mode
        self.mode='ia' #ia mode or random mode

    def next_player(self)->int:
        return 1+ self.player%2

    def put_in_random_position(self)->None:
        #for a game random mode
        pos=choice(self.bd.empty_boxes())
        print("The robot chosen {} as a random position: ".format(pos))
        self.bd.add_symbole_to_position(self.player,pos)

    def put_in_the_best_position(self,robot:Robot,n_robot='')->None:
        #for a game ai mode
        if len(self.bd.empty_boxes())==9:
            #to variate the game start: the robot will choose always the first box '0' in the beginning of the game
            self.put_in_random_position()
            return
        value,best_move=robot.max_value(self.bd)
        print(f"The robot {n_robot and str(n_robot)+' '}chosen {best_move} as the best position with the value {value}: ")      
        self.bd.add_symbole_to_position(self.player,best_move)  

    def play_p1_vs_p2(self,function_for_player1,function_for_player2,print_symbol=False)->None:
        for i in range(9):
            self.bd.print_board()
            if print_symbol:
                print("\tIt is the turn of the player with the symbol '{}':".format(PLAYER_TO_SYMBOLE[self.player]))
        
            print("\n\n")
            if self.player==self.robot_symbole:
                function_for_player1()
            else :
                function_for_player2()
            
            if self.bd.is_here_a_winner()[0] :
                self.bd.print_board()
                print(f"\n\n'{PLAYER_TO_SYMBOLE[self.player]}' wins!")
                break
            self.player=self.next_player()
        
        else:
            self.bd.print_board()
            print("\n\nIt is a tie!")

    def robot_vs_robot_random_mode(self)->None:
        self.play_p1_vs_p2(self.put_in_random_position,self.put_in_random_position)
    
    def robot_vs_robot_ai_mode(self)->None:
        self.play_p1_vs_p2(lambda:self.put_in_the_best_position(self.robot1,n_robot=1),
                           lambda:self.put_in_the_best_position(self.robot2,n_robot=2))

    def get_a_choice_from_the_player(self)->None:
        player_choice=input("Enter your choice: ").strip()
        try:
            player_choice= int(player_choice)
            if not player_choice in self.bd.empty_boxes():
                raise 
            self.bd.add_symbole_to_position(self.player,player_choice)
        except:
            print("Invalid choice")
            self.get_a_choice_from_the_player()
    
    def get_game_info_from_player(self)->None:
        #which symbol will be used by the player
        while True:
            symbole=input("Do you want to play with 'O' or 'X': ").lower().strip()
            if symbole=='o':
                self.robot_symbole=1
                break
            elif symbole=='x':
                self.robot_symbole=2
                break
            else :
                print("Invalid choice!")
            
        #who will begin the game
        while True:
            start=input("Do you want to start the game (y/n): ").lower().strip()
            if start in ['y', 'n']:
                self.player=self.robot_symbole
                if start == 'y': 
                    self.player=self.next_player() 
                break
            else:
                print("Invalid choice!")
        self.robot=Robot(self.robot_symbole)
   
    def robot_vs_player_ai_mode(self)->None:
        self.get_game_info_from_player()
        self.play_p1_vs_p2(lambda:self.put_in_the_best_position(self.robot),
                           self.get_a_choice_from_the_player)
    
    def robot_vs_player_random_mode(self)->None:
        self.get_game_info_from_player()
        self.play_p1_vs_p2(self.put_in_random_position,
                           self.get_a_choice_from_the_player)

    def player_vs_player(self):
        self.play_p1_vs_p2(self.get_a_choice_from_the_player,
                           self.get_a_choice_from_the_player,print_symbol=True)
