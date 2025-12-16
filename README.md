# compile_dungeon - the straight to web dungeon compiler

- Craft your web-deployable dungeon using our dungeon specific language.
- Imbue your npcs with the ability to talk using LLM connectivity
- Experience your emoji-filled dungeon in your favorite browser

## Example Dungeon Specific Language 
```
init:
    world: 100 x 100 grid
    furniture:
        grass at all
    llm:
        endpoint "http://localhost:1234/v1/chat/completions"
        token "sometoken"
    mytics:
        mythic-static: unique_name="gem1", place at (20, 20), can be picked up by the user
        mythic-static: unique_name="gem2", place at (80, 80), can be picked up by the user
    monsters:
        monster-static: unique_name="goblin", place at (50, 50), health 3, gives 50 experience
    npc:
        npc-dynamic: unique_name="lammad" place at (10, 10) context "You are an elf, who playfuly says everything back as prose."
    user: unique_name="player", context "hero", at (10, 10)
quests:
    if user has item "gem1" and user has item "gem2" then level up
end_game:
    if user has item "gem1" and user has item "gem2" then win the game
    win_the_game: show "Congratulations Dungeon Crawler! You found both gems and won the game!"
```

# Tl;Dr How to Compile examples

## Prerequisites
python > 3.11

## Compile an example 
cd examples
python ../src/compile_dungeon.py example_game.dsl example_game.html

## Open up the game in a browser (NO LLM ACCESS)
```chrome-stable example_game.html``` or open op the browser

## Open up the game in a browser (WITH LLM ACCESS)
- ```cd examples``` (or change to whatever directory you want to serve)
- ```python3 -m http.server 8000```
- ```chrome-stable localhots:8000``` or open up a browser to http://localhost:8000
### It is necessary to serve it this way due to CORS issues with static files

# Game Language: How To Create a Game

### Create and Populate a Game

A game file (`.dsl`) consists of several epic sections:

```dsl
init:
    world: 100 x 100 grid
    furniture:
        grass at all
        house at (10, 20)
    user: unique_name="player", context "hero", at (10, 10)
quests:
    if user has 1000 experience then level up
end_game:
    if user has 0 health then die and lose the game
    win_the_game: show "Congratulations!"
```

**Basic structure:**
- `init:` - Defines the game world, entities, and starting conditions
- `quests:` - Defines quest conditions and rewards
- `end_game:` - Defines win/lose conditions
- `rules:` (optional) - Defines game rules and interactions

### How to Add NPCs

NPCs can be static (fixed responses), dynamic (LLM-powered), or state-machine based.

#### Static NPCs
```dsl
init:
    npc:
        npc-static: unique_name="sheila" place at (2, 2) response "Hello there!"
```

#### Dynamic NPCs (LLM-powered)
```dsl
init:
    llm:
        endpoint "http://localhost:1234/v1/chat/completions"
        token "anything"
    npc:
        npc-dynamic: unique_name="echo" place at (10, 10) context "You are Echo, a helpful assistant."
```

#### State Machine NPCs
```dsl
init:
    npc:
        npc-state-machine: unique_name="jim" place at (5, 5) state_machine "idle"
```

**NPC Properties:**
- `unique_name` - Unique identifier for the NPC
- `place at (x, y)` - Starting position
- `context` - Context string for LLM NPCs
- `response` - Static response for static NPCs
- `emoji` - Optional emoji representation (defaults to person emoji)
- `agenda` - Free text that guides LLM-based NPC behavior

### How to Add Items

Items can be placed in the world and picked up by the player:

```dsl
init:
    items:
        item: unique_name="healing_potion" place at (50, 50) can be picked up by the user, can be used to heal the user 100 health
        item: unique_name="sword" place at random (30%) damage 10
```

**Item Properties:**
- `unique_name` - Unique identifier
- `place at (x, y)` - Fixed position, or `place at random (percentage%)` for random placement
- `can be picked up by the user` - Makes item collectible
- `can be used to heal the user N health` - Item effect
- `damage N` - Damage value if used as a weapon

### How to Add Monsters

Monsters can be placed and have combat properties:

```dsl
init:
    monsters:
        monster-static: unique_name="goblin" place at (50, 50) health 3, gives 50 experience
        monster-static: unique_name="goblin-king" place at random (10%) health 10, gives 1000 experience
```

**Monster Properties:**
- `unique_name` - Unique identifier
- `place at (x, y)` - Fixed position, or `place at random (percentage%)` for random placement
- `health N` - Health points
- `killable N hit` - Alternative: dies after N hits (deprecated, use health instead)
- `gives N experience` - Experience points awarded when defeated

### How to Add LLM NPCs with Locally Hosted LLMs

1. **Start your local LLM server** (see "How to Install / Run Local LLM" above)

2. **Configure LLM endpoint in your DSL:**
   ```dsl
   init:
       llm:
           endpoint "http://localhost:1234/v1/chat/completions"
           token "anything"
   ```

3. **Add dynamic NPCs:**
   ```dsl
   init:
       npc:
           npc-dynamic: unique_name="quest_giver" place at (10, 10) context "You are a wise quest giver in a fantasy world."
   ```

4. **Add rules for interaction:**
   ```dsl
   rules:
       if user is at (10, 10) and npc-dynamic is at (10, 10) then talk-dynamic
   ```

5. **Compile and run:**
   ```bash
   python compile_dungeon.py your_game.dsl game.html
   ```

The compiled game will automatically connect to your local LLM server when players interact with dynamic NPCs.



# License
MIT License

Copyright (c) 2025 Michael Shomsky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
