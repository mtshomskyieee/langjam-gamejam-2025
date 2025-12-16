init:
    world: 20 x 20 grid
    furniture:
        grass at all
    npc:
        npc-static: unique_name="sheila" place at (2, 2) response "gooday"
        npc-static: unique_name="todd" place at (8, 8) response "hello my name is todd"
    user: unique_name="player", context "hero", at (10, 10)
quests:
end_game:
