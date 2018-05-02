import rpsttt

p1 = rpsttt.Player("Joe")
p2 = rpsttt.Player("AlsoeJoe")

game = rpsttt.GameInstance(p1, p2)
game.mark_board(0, 0, rpsttt.Mark.X)
game.mark_board(0, 1, rpsttt.Mark.X)
game.mark_board(0, 2, rpsttt.Mark.X)

game.check_for_winner()
game.pretty_print()
print("Row Winner: " + game.winner.name)


game = rpsttt.GameInstance(p1,p2)
game.mark_board(0, 0, rpsttt.Mark.O)
game.mark_board(1, 0, rpsttt.Mark.O)
game.mark_board(2, 0, rpsttt.Mark.O)

game.check_for_winner()
game.pretty_print()
print("Column Winner: " + game.winner.name)

def deanstest():
    p1 = rpsttt.Player("Joe")
    p2 = rpsttt.Player("Doe")
    game = rpsttt.GameInstance(p1, p2)
    game.gameloop()
    print(game.winner.name)

deanstest()

