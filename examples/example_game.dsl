init:
    world: 100 x 100 grid
    furniture:
        grass at all
    mytics:
        mythic-static: unique_name="gem1", place at (20, 20), can be picked up by the user
        mythic-static: unique_name="gem2", place at (80, 80), can be picked up by the user
    monsters:
        monster-static: unique_name="goblin", place at (50, 50), health 3, gives 50 experience
    user: unique_name="player", context "hero", at (10, 10)
quests:
    if user has item "gem1" and user has item "gem2" then level up
end_game:
    if user has item "gem1" and user has item "gem2" then win the game
    win_the_game: show "Congratulations! You found both gems and won the game!"

