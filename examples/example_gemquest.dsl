init:
    world: 10 x 10 grid
    furniture:
        grass at all
    mytics:
        mythic-static: unique_name="gem1", place at (2, 2), can be picked up by the user
        mythic-static: unique_name="gem2", place at (5, 3), can be picked up by the user
        mythic-static: unique_name="gem3", place at (8, 2), can be picked up by the user
        mythic-static: unique_name="gem4", place at (3, 5), can be picked up by the user
        mythic-static: unique_name="gem5", place at (7, 5), can be picked up by the user
        mythic-static: unique_name="gem6", place at (2, 8), can be picked up by the user
        mythic-static: unique_name="gem7", place at (5, 7), can be picked up by the user
        mythic-static: unique_name="gem8", place at (9, 9), can be picked up by the user
        mythic-static: unique_name="gem9", place at (3, 3), can be picked up by the user
        mythic-static: unique_name="gem10", place at (4, 9), can be picked up by the user
    user: unique_name="player", context "hero", at (1, 1)
quests:
end_game:
    if user has item "gem1" and user has item "gem2" and user has item "gem3" and user has item "gem4" and user has item "gem5" and user has item "gem6" and user has item "gem7" and user has item "gem8" and user has item "gem9" and user has item "gem10" then win the game
    win_the_game: show "Congratulations! You collected all the gems and won the game!"
on_game_start:
    display_title: "Gem Quest, collect them all!"

