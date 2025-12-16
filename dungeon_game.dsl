init:
    world: 20 x 20 grid
    furniture:
        grass at all
        # Outer wall (15x15, centered at 10,10, so from 3,3 to 17,17)
        wall at (3, 3) to (9, 3)
        wall at (11, 3) to (17, 3)
        wall at (3, 17) to (9, 17)
        wall at (11, 17) to (17, 17)
        wall at (3, 3) to (3, 9)
        wall at (3, 11) to (3, 17)
        wall at (17, 3) to (17, 9)
        wall at (17, 11) to (17, 17)
        # Inner wall (around wizard at 10,10)
        wall at (8, 8) to (9, 8)
        wall at (11, 8) to (12, 8)
        wall at (8, 12) to (9, 12)
        wall at (11, 12) to (12, 12)
        wall at (8, 9) to (8, 10)
        wall at (8, 11) to (8, 11)
        wall at (12, 9) to (12, 10)
        wall at (12, 11) to (12, 11)
    llm:
        endpoint "http://localhost:1234/v1/chat/completions"
        token "anything"
    items:
        item-heal: unique_name="healing_potion_1", place at (1, 5), can be picked up by the user
        item-heal: unique_name="healing_potion_2", place at (19, 15), can be picked up by the user
    mytics:
        mythic-static: unique_name="gem1", place at (1, 1), can be picked up by the user
        mythic-static: unique_name="gem2", place at (19, 1), can be picked up by the user
        mythic-static: unique_name="gem3", place at (1, 19), can be picked up by the user
        mythic-static: unique_name="gem4", place at (19, 19), can be picked up by the user
        mythic-static: unique_name="gem5", place at (10, 1), can be picked up by the user
        # Gems between outer and inner walls
        mythic-static: unique_name="gem6", place at (5, 5), can be picked up by the user
        mythic-static: unique_name="gem7", place at (15, 5), can be picked up by the user
        mythic-static: unique_name="gem8", place at (5, 15), can be picked up by the user
        mythic-static: unique_name="gem9", place at (15, 15), can be picked up by the user
    monsters:
        # Outer wall entrance guard
        monster-static: unique_name="goblin_guard_entrance", place at (3, 10), health 3, gives 25 experience
        # Inner wall entrance guards
        monster-static: unique_name="goblin_guard_top", place at (10, 8), health 3, gives 25 experience
        monster-static: unique_name="goblin_guard_bottom", place at (10, 12), health 3, gives 25 experience
        # Goblins between outer and inner walls
        monster-static: unique_name="goblin_patrol_1", place at (6, 6), health 2, gives 15 experience
        monster-static: unique_name="goblin_patrol_2", place at (14, 6), health 2, gives 15 experience
        monster-static: unique_name="goblin_patrol_3", place at (6, 14), health 2, gives 15 experience
        monster-static: unique_name="goblin_patrol_4", place at (14, 14), health 2, gives 15 experience
    npc:
        npc-dynamic: unique_name="wizard" place at (10, 10) context "You are a wise wizard living in the center of a dungeon. You can answer questions about magic, the dungeon, or help guide adventurers. Be mysterious but helpful."
    user: unique_name="player", context "adventurer", at (1, 1)
quests:
    gem_quest:
        if user has item "gem1" and user has item "gem2" and user has item "gem3" and user has item "gem4" and user has item "gem5" and user has item "gem6" and user has item "gem7" and user has item "gem8" and user has item "gem9" then level up
    knowledge_quest:
        if user talked to wizard then level up
end_game:
    if wizard responded then win the game
    win_the_game: show "Congratulations! You gained the wizards knowledge!"

