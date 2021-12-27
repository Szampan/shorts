import random
from time import sleep
from icecream import ic

def game():
    repeat = True
    while repeat:
        player_move = get_player_move()
        sleep(0.5)
        cpu_move = get_cpu_move()
        print('Ruch komputera:', cpu_move)
        sleep(0.5)
        result = fight(cpu_move, player_move)

        winner = get_winner(result)
        print(f"\nWygrał {winner}.")
        repeat = repeat_or_not()

def get_player_move():
    while True:
        print("\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
        move = input("[P]apier, [K]amień, [N]ożyce\nTwój ruch: ").lower()
        if move not in list("pkn"):
            print("Twój wybór jespt inwalidą.")
        else: 
            return move
    
def get_cpu_move():
    return random.choice(list("pkn"))

def fight(p1_move: str, p2_move: str):
    if p1_move == p2_move:
        return 0
    elif p1_move == "p" and p2_move == "k" or p1_move == "k" and p2_move == "n" or p1_move == "n" and p2_move == "p":
        return -1
    else:
        return 1

def get_winner(result):
    if result == -1:
        return "KOMPUTER"
    elif result == 1:
        return "GRACZ"
    else:
        return "nikt"

def repeat_or_not():
    answer = input("Jeszcze raz? [T]/[N]\n").lower()
    if answer == "t":
        return True
    

if __name__ == '__main__':
    game()
