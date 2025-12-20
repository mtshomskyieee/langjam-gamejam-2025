init:
    world: 1000 x 30 grid
    furniture:
        grass at all
        # Room 1: Starting Chamber (0-80)
        wall at (0, 0) to (80, 0)
        wall at (0, 29) to (80, 29)
        wall at (80, 0) to (80, 12)
        wall at (80, 17) to (80, 29)
        # Room 2: Goblin Den (81-160)
        wall at (81, 0) to (160, 0)
        wall at (81, 29) to (160, 29)
        wall at (160, 0) to (160, 10)
        wall at (160, 20) to (160, 29)
        # Room 3: Treasure Vault (161-240)
        wall at (161, 0) to (240, 0)
        wall at (161, 29) to (240, 29)
        wall at (240, 0) to (240, 14)
        wall at (240, 16) to (240, 29)
        # Room 4: Orc Stronghold (241-320)
        wall at (241, 0) to (320, 0)
        wall at (241, 29) to (320, 29)
        wall at (320, 0) to (320, 8)
        wall at (320, 22) to (320, 29)
        # Room 5: Crystal Cavern (321-400)
        wall at (321, 0) to (400, 0)
        wall at (321, 29) to (400, 29)
        wall at (400, 0) to (400, 13)
        wall at (400, 17) to (400, 29)
        # Room 6: Shadow Realm (401-480)
        wall at (401, 0) to (480, 0)
        wall at (401, 29) to (480, 29)
        wall at (480, 0) to (480, 11)
        wall at (480, 19) to (480, 29)
        # Room 7: Fire Chamber (481-560)
        wall at (481, 0) to (560, 0)
        wall at (481, 29) to (560, 29)
        wall at (560, 0) to (560, 9)
        wall at (560, 21) to (560, 29)
        # Room 8: Ice Fortress (561-640)
        wall at (561, 0) to (640, 0)
        wall at (561, 29) to (640, 29)
        wall at (640, 0) to (640, 12)
        wall at (640, 18) to (640, 29)
        # Room 9: Ancient Library (641-720)
        wall at (641, 0) to (720, 0)
        wall at (641, 29) to (720, 29)
        wall at (720, 0) to (720, 7)
        wall at (720, 23) to (720, 29)
        # Room 10: Dragon's Lair (721-800)
        wall at (721, 0) to (800, 0)
        wall at (721, 29) to (800, 29)
        wall at (800, 0) to (800, 12)
        wall at (800, 18) to (800, 29)
        # Room 11: Final Approach (801-900)
        wall at (801, 0) to (900, 0)
        wall at (801, 29) to (900, 29)
        wall at (900, 0) to (900, 5)
        wall at (900, 25) to (900, 29)
        # Room 12: Sanctuary of Wisdom (901-999) - Final Room
        wall at (901, 0) to (999, 0)
        wall at (901, 29) to (999, 29)
        wall at (901, 0) to (901, 13)
        wall at (901, 17) to (901, 29)
        # Inner walls in final room for atmosphere
        wall at (950, 5) to (999, 5)
        wall at (950, 24) to (999, 24)
        wall at (950, 5) to (950, 13)
        wall at (950, 17) to (950, 24)
    llm:
        endpoint "http://localhost:1234/v1/chat/completions"
        token "anything"
    items:
        # Room 1 items
        item-heal: unique_name="potion_start_1", place at (20, 5), can be picked up by the user
        item-heal: unique_name="potion_start_2", place at (50, 25), can be picked up by the user
        # Room 2 items
        item-heal: unique_name="potion_goblin_1", place at (120, 8), can be picked up by the user
        item-heal: unique_name="potion_goblin_2", place at (140, 22), can be picked up by the user
        # Room 3 items
        item-heal: unique_name="potion_treasure_1", place at (200, 3), can be picked up by the user
        item-heal: unique_name="potion_treasure_2", place at (220, 26), can be picked up by the user
        # Room 4 items
        item-heal: unique_name="potion_orc_1", place at (280, 6), can be picked up by the user
        item-heal: unique_name="potion_orc_2", place at (300, 24), can be picked up by the user
        # Room 5 items
        item-heal: unique_name="potion_crystal_1", place at (360, 4), can be picked up by the user
        item-heal: unique_name="potion_crystal_2", place at (380, 25), can be picked up by the user
        # Room 6 items
        item-heal: unique_name="potion_shadow_1", place at (440, 7), can be picked up by the user
        item-heal: unique_name="potion_shadow_2", place at (460, 23), can be picked up by the user
        # Room 7 items
        item-heal: unique_name="potion_fire_1", place at (520, 5), can be picked up by the user
        item-heal: unique_name="potion_fire_2", place at (540, 24), can be picked up by the user
        # Room 8 items
        item-heal: unique_name="potion_ice_1", place at (600, 8), can be picked up by the user
        item-heal: unique_name="potion_ice_2", place at (620, 21), can be picked up by the user
        # Room 9 items
        item-heal: unique_name="potion_library_1", place at (680, 3), can be picked up by the user
        item-heal: unique_name="potion_library_2", place at (700, 26), can be picked up by the user
        # Room 10 items
        item-heal: unique_name="potion_dragon_1", place at (760, 6), can be picked up by the user
        item-heal: unique_name="potion_dragon_2", place at (780, 23), can be picked up by the user
        item-heal: unique_name="potion_dragon_3", place at (780, 8), can be picked up by the user
        # Room 11 items
        item-heal: unique_name="potion_final_1", place at (810, 5), can be picked up by the user
        item-heal: unique_name="potion_final_2", place at (870, 5), can be picked up by the user
        item-heal: unique_name="potion_final_3", place at (810, 25), can be picked up by the user
        item-heal: unique_name="potion_final_4", place at (870, 25), can be picked up by the user

    mytics:
        # Room 1 mythics
        mythic-static: unique_name="gem_room1_1", place at (15, 10), can be picked up by the user
        mythic-static: unique_name="gem_room1_2", place at (45, 20), can be picked up by the user
        # Room 2 mythics
        mythic-static: unique_name="gem_room2_1", place at (110, 15), can be picked up by the user
        mythic-static: unique_name="gem_room2_2", place at (130, 5), can be picked up by the user
        # Room 3 mythics
        mythic-static: unique_name="gem_room3_1", place at (190, 18), can be picked up by the user
        mythic-static: unique_name="gem_room3_2", place at (210, 8), can be picked up by the user
        # Room 4 mythics
        mythic-static: unique_name="gem_room4_1", place at (270, 12), can be picked up by the user
        mythic-static: unique_name="gem_room4_2", place at (290, 22), can be picked up by the user
        # Room 5 mythics
        mythic-static: unique_name="gem_room5_1", place at (350, 16), can be picked up by the user
        mythic-static: unique_name="gem_room5_2", place at (370, 6), can be picked up by the user
        # Room 6 mythics
        mythic-static: unique_name="gem_room6_1", place at (430, 14), can be picked up by the user
        mythic-static: unique_name="gem_room6_2", place at (450, 24), can be picked up by the user
        # Room 7 mythics
        mythic-static: unique_name="gem_room7_1", place at (510, 11), can be picked up by the user
        mythic-static: unique_name="gem_room7_2", place at (530, 21), can be picked up by the user
        # Room 8 mythics
        mythic-static: unique_name="gem_room8_1", place at (590, 15), can be picked up by the user
        mythic-static: unique_name="gem_room8_2", place at (610, 5), can be picked up by the user
        # Room 9 mythics
        mythic-static: unique_name="gem_room9_1", place at (670, 19), can be picked up by the user
        mythic-static: unique_name="gem_room9_2", place at (690, 9), can be picked up by the user
        # Room 10 mythics
        mythic-static: unique_name="gem_room10_1", place at (750, 13), can be picked up by the user
        mythic-static: unique_name="gem_room10_2", place at (770, 23), can be picked up by the user
        # Room 11 mythics
        mythic-static: unique_name="gem_room11_1", place at (830, 17), can be picked up by the user
        mythic-static: unique_name="gem_room11_2", place at (850, 7), can be picked up by the user
    monsters:
        # Room 1: Starting Chamber - Easy guards
        monster-static: unique_name="guard_start_1", place at (30, 15), health 2, gives 20 experience
        monster-static: unique_name="guard_start_2", place at (60, 15), health 2, gives 20 experience
        monster-dynamic: unique_name="ninja_start", place at (40, 20), health 2, gives 25 experience
        monster-boss: unique_name="boss_start", place at (50, 10), health 8, gives 100 experience
        # Room 2: Goblin Den - More goblins
        monster-static: unique_name="goblin_den_1", place at (100, 15), health 3, gives 30 experience
        monster-static: unique_name="goblin_den_2", place at (120, 5), health 3, gives 30 experience
        monster-static: unique_name="goblin_den_3", place at (140, 25), health 3, gives 30 experience
        monster-dynamic: unique_name="ninja_goblin", place at (110, 20), health 3, gives 35 experience
        monster-boss: unique_name="boss_goblin", place at (130, 15), health 12, gives 150 experience
        # Room 3: Treasure Vault - Vault guards
        monster-static: unique_name="vault_guard_1", place at (180, 15), health 4, gives 40 experience
        monster-static: unique_name="vault_guard_2", place at (200, 8), health 4, gives 40 experience
        monster-static: unique_name="vault_guard_3", place at (220, 22), health 4, gives 40 experience
        monster-dynamic: unique_name="ninja_vault", place at (190, 20), health 4, gives 45 experience
        monster-boss: unique_name="boss_vault", place at (200, 15), health 16, gives 200 experience
        # Room 4: Orc Stronghold - Orcs
        monster-static: unique_name="orc_warrior_1", place at (260, 15), health 5, gives 50 experience
        monster-static: unique_name="orc_warrior_2", place at (280, 10), health 5, gives 50 experience
        monster-static: unique_name="orc_warrior_3", place at (300, 20), health 5, gives 50 experience
        monster-static: unique_name="orc_warrior_4", place at (270, 5), health 4, gives 40 experience
        monster-dynamic: unique_name="ninja_orc", place at (270, 20), health 5, gives 55 experience
        monster-boss: unique_name="boss_orc", place at (280, 15), health 20, gives 250 experience
        # Room 5: Crystal Cavern - Crystal guardians
        monster-static: unique_name="crystal_guard_1", place at (340, 15), health 5, gives 50 experience
        monster-static: unique_name="crystal_guard_2", place at (360, 10), health 5, gives 50 experience
        monster-static: unique_name="crystal_guard_3", place at (380, 20), health 5, gives 50 experience
        monster-dynamic: unique_name="ninja_crystal", place at (350, 20), health 5, gives 55 experience
        monster-boss: unique_name="boss_crystal", place at (360, 15), health 20, gives 250 experience
        # Room 6: Shadow Realm - Shadow creatures
        monster-static: unique_name="shadow_beast_1", place at (420, 15), health 6, gives 60 experience
        monster-static: unique_name="shadow_beast_2", place at (440, 8), health 6, gives 60 experience
        monster-static: unique_name="shadow_beast_3", place at (460, 22), health 6, gives 60 experience
        monster-dynamic: unique_name="ninja_shadow", place at (430, 20), health 6, gives 65 experience
        monster-boss: unique_name="boss_shadow", place at (440, 15), health 24, gives 300 experience
        # Room 7: Fire Chamber - Fire elementals
        monster-static: unique_name="fire_elemental_1", place at (500, 15), health 6, gives 60 experience
        monster-static: unique_name="fire_elemental_2", place at (520, 9), health 6, gives 60 experience
        monster-static: unique_name="fire_elemental_3", place at (540, 21), health 6, gives 60 experience
        monster-dynamic: unique_name="ninja_fire", place at (510, 20), health 6, gives 65 experience
        monster-boss: unique_name="boss_fire", place at (520, 15), health 24, gives 300 experience
        # Room 8: Ice Fortress - Ice guardians
        monster-static: unique_name="ice_guardian_1", place at (580, 15), health 7, gives 70 experience
        monster-static: unique_name="ice_guardian_2", place at (600, 11), health 7, gives 70 experience
        monster-static: unique_name="ice_guardian_3", place at (620, 19), health 7, gives 70 experience
        monster-dynamic: unique_name="ninja_ice", place at (590, 20), health 7, gives 75 experience
        monster-boss: unique_name="boss_ice", place at (600, 15), health 28, gives 350 experience
        # Room 9: Ancient Library - Librarian guardians
        monster-static: unique_name="librarian_guard_1", place at (660, 15), health 7, gives 70 experience
        monster-static: unique_name="librarian_guard_2", place at (680, 7), health 7, gives 70 experience
        monster-static: unique_name="librarian_guard_3", place at (700, 23), health 7, gives 70 experience
        monster-dynamic: unique_name="ninja_library", place at (670, 20), health 7, gives 75 experience
        monster-boss: unique_name="boss_library", place at (680, 15), health 28, gives 350 experience
        # Room 10: Dragon's Lair - Dragon minions
        monster-static: unique_name="dragon_minion_1", place at (740, 15), health 8, gives 80 experience
        monster-static: unique_name="dragon_minion_2", place at (760, 10), health 8, gives 80 experience
        monster-static: unique_name="dragon_minion_3", place at (780, 20), health 8, gives 80 experience
        monster-static: unique_name="dragon_minion_4", place at (750, 5), health 7, gives 70 experience
        monster-dynamic: unique_name="ninja_dragon", place at (750, 20), health 8, gives 85 experience
        monster-boss: unique_name="boss_dragon", place at (760, 15), health 32, gives 400 experience
        # Room 11: Final Approach - Elite guards
        monster-static: unique_name="elite_guard_1", place at (820, 15), health 9, gives 90 experience
        monster-static: unique_name="elite_guard_2", place at (840, 3), health 9, gives 90 experience
        monster-static: unique_name="elite_guard_3", place at (860, 27), health 9, gives 90 experience
        monster-static: unique_name="elite_guard_4", place at (830, 10), health 8, gives 80 experience
        monster-static: unique_name="elite_guard_5", place at (850, 20), health 8, gives 80 experience
        monster-dynamic: unique_name="ninja_elite", place at (830, 20), health 9, gives 95 experience
        monster-boss: unique_name="boss_elite", place at (840, 15), health 36, gives 450 experience
        # Room 12: Final Room Guardian - Goblin guarding the entrance
        monster-static: unique_name="final_room_goblin_guard", place at (901, 15), health 10, gives 100 experience
        monster-dynamic: unique_name="ninja_final", place at (920, 15), health 10, gives 105 experience
        monster-boss: unique_name="boss_final", place at (950, 15), health 40, gives 500 experience
    npc:
        # Room 1
        npc-static: unique_name="intro_guide" place at (7, 15) response "Skulls attack, Red Goblins obstruct.  Use the enter-key to fight them.  Diamonds Heal. Enemies get progressively harder.  You may have to outrun opponents to get to your goal."
        # Room 12
        npc-dynamic: unique_name="ancient_wisdom_keeper" place at (975, 15) context "You are the Ancient Wisdom Keeper, a powerful entity who has guarded the secrets of the dungeon for millennia. You have watched countless adventurers journey through the 12 chambers, facing goblins, orcs, shadow beasts, fire elementals, ice guardians, and dragon minions. You are wise, mysterious, and know the true purpose of this dungeon. You can answer questions about the journey, the monsters, the treasures, or the deeper meaning of the quest. Be enigmatic but helpful, and congratulate adventurers who have made it this far." response "If I were connected to the LLM I could tell you anything, but the connection is down. All I can say is congratulations!"
    user: unique_name="player", context "adventurer", at (5, 15)
quests:
    collection_quest:
        if user has item "gem_room1_1" and user has item "gem_room1_2" and user has item "gem_room2_1" and user has item "gem_room2_2" and user has item "gem_room3_1" and user has item "gem_room3_2" and user has item "gem_room4_1" and user has item "gem_room4_2" and user has item "gem_room5_1" and user has item "gem_room5_2" and user has item "gem_room6_1" and user has item "gem_room6_2" and user has item "gem_room7_1" and user has item "gem_room7_2" and user has item "gem_room8_1" and user has item "gem_room8_2" and user has item "gem_room9_1" and user has item "gem_room9_2" and user has item "gem_room10_1" and user has item "gem_room10_2" and user has item "gem_room11_1" and user has item "gem_room11_2" then level up
    wisdom_quest:
        if user talked to ancient_wisdom_keeper then level up
end_game:
    if ancient_wisdom_keeper responded then win the game
    win_the_game: show "Congratulations! You have reached the Sanctuary of Wisdom and gained the knowledge of the Ancient Wisdom Keeper! Your journey through the 12 chambers is complete!"
on_game_start:
    display_title: "The Great Dungeon Journey!"
    display_text: "Journey through 12 chambers from left to right"
    display_text: "Each room is guarded by monsters and contains treasures"
    display_text: "Reach the Sanctuary of Wisdom at the end to meet the Ancient Wisdom Keeper"
    display_text: "Commands: [arrow-keys] for movement, [Space] and [Enter] to talk/fight"
    display_text: "Use Shift+Arrow keys to pan the camera across the large world"
    display_text: "2025 Langjam" 
    display_link: "github", "https://github.com/mtshomskyieee/langjam-gamejam-2025"

