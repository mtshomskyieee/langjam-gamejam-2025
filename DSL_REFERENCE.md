# Dungeon Game DSL - Complete Language Reference

## Table of Contents
1. [Language Structure](#language-structure)
2. [Comments](#comments)
3. [Variables](#variables)
4. [Init Section](#init-section)
5. [World Declaration](#world-declaration)
6. [Furniture](#furniture)
7. [Mythics](#mythics)
8. [Items](#items)
9. [Monsters](#monsters)
10. [User/Player](#userplayer)
11. [NPCs](#npcs)
12. [LLM Configuration](#llm-configuration)
13. [Placement Syntax](#placement-syntax)
14. [Rules Section](#rules-section)
15. [Quests Section](#quests-section)
16. [End Game Section](#end-game-section)
17. [On Game Start Section](#on-game-start-section)
18. [Conditions](#conditions)
19. [Actions](#actions)
20. [Operators](#operators)
21. [Data Types](#data-types)
22. [Game Mechanics](#game-mechanics)

---

## Language Structure

A DSL program consists of optional top-level sections in any order:

```
[let declarations]
init:
    [world, furniture, mythics, items, monsters, user, npc, llm declarations]
rules:
    [rule declarations]
quests:
    [quest declarations]
end_game:
    [end game conditions]
on_game_start:
    [splash screen configuration]
```

**Required:** `init:` section must be present.

**Optional:** `rules:`, `quests:`, `end_game:`, `on_game_start:`, variable declarations.

---

## Comments

Single-line comments using `#`:

```
# This is a comment
world: 100 x 100 grid  # Inline comment
```

---

## Variables

Global variables declared with `let`:

```
let variable_name = value
```

**Value types:** number, string, boolean, identifier

**Examples:**
```
let max_health = 100
let player_name = "hero"
let debug_mode = true
let default_level = 1
```

**Usage:** Variables are stored in game state and accessible via `state.variables`.

---

## Init Section

The `init:` section defines the game world and all entities. Structure:

```
init:
    world: [world declaration]
    furniture: [furniture items]
    mytics: [mythic items]
    items: [item declarations]
    monsters: [monster declarations]
    user: [user declaration]
    npc: [NPC declarations]
    llm: [LLM configuration]
```

All subsections are optional except at least one must be present.

---

## World Declaration

Defines the game world grid dimensions:

```
world: [width] x [height] grid
world: grid  # Default: 100 x 100
```

**Examples:**
```
world: 100 x 100 grid
world: 1000 x 30 grid
world: grid  # 100x100 default
```

**Default:** 100 x 100 if not specified.

---

## Furniture

Furniture items placed in the world. Furniture types: `wall`, `stone`, `grass`, `house`, or any identifier.

**Syntax:**
```
furniture:
    [furniture_name] at [placement]
```

**Placement types:**
- `all` - Place on every cell
- `(x, y)` - Single coordinate
- `(x1, y1) to (x2, y2)` - Range (inclusive rectangle)

**Examples:**
```
furniture:
    grass at all
    wall at (10, 20)
    stone at (5, 5) to (10, 10)
    house at (50, 50)
```

**Behavior:**
- `wall` and `stone` block movement (impassible)
- Other furniture types are decorative (passable)
- Furniture renders with emoji: 🧱 (wall/stone), 🟩 (grass), 🏠 (default)

---

## Mythics

Special collectible items with unique names. More valuable than regular items.

**Syntax:**
```
mytics:
    mythic-static:
        unique_name="[name]"
        [, place at [placement]]
        [, can be picked up by the user]
        [, catch "[message]"]
```

**Properties:**
- `unique_name` (required) - String identifier, must be unique across all entities
- `place at [placement]` (optional) - Where mythic is placed
- `can be picked up by the user` (optional) - Makes item collectible
- `catch "[message]"` (optional) - Message shown when user tries to pick up non-pickup mythic

**Examples:**
```
mytics:
    mythic-static: unique_name="gem1", place at (20, 20), can be picked up by the user
    mythic-static: unique_name="crystal", place at random (30%), can be picked up by the user
    mythic-static: unique_name="locked_treasure", place at (50, 50), catch "This treasure is locked!"
```

**Rendering:** 💠 emoji

**Behavior:**
- If `can be picked up by the user`: Auto-collected when user steps on cell, added to inventory
- If not pickup-able: Shows `catch_message` when user steps on cell
- Once picked up, removed from world

---

## Items

Regular items with types, effects, and properties.

**Syntax:**
```
items:
    [item_type]:
        unique_name="[name]"
        [, place at [placement]]
        [, can be picked up by the user]
        [, can be used to [effect_description]]
        [, damage [number]]
        [, catch "[message]"]
```

**Item Types:**
- `item` - Generic item
- `item-heal` - Healing item (restores 25% max health when picked up)

**Properties:**
- `unique_name` (required) - String identifier, must be unique
- `place at [placement]` (optional) - Placement location
- `can be picked up by the user` (optional) - Makes collectible
- `can be used to [effect_description]` (optional) - Effect description (string or identifier sequence)
- `damage [number]` (optional) - Damage value (for weapons)
- `catch "[message]"` (optional) - Message for non-pickup items

**Examples:**
```
items:
    item-heal: unique_name="potion", place at (10, 10), can be picked up by the user
    item: unique_name="sword", place at (20, 20), can be picked up by the user, damage 10
    item: unique_name="locked_chest", place at (30, 30), catch "The chest is locked!"
    item: unique_name="tool", place at random (25%), can be picked up by the user, can be used to "repair equipment"
```

**Rendering:** 💎 emoji

**Behavior:**
- `item-heal`: When picked up, restores 25% of max health (100), shows heal amount
- Other items: Added to inventory when picked up
- Items with `can be used to` have effect descriptions (future use)

---

## Monsters

Enemies that can be fought. Three types: static, dynamic, boss.

**Syntax:**
```
monsters:
    [monster_type]:
        unique_name="[name]"
        [, place at [placement]]
        [, health [number]]
        [, killable [number] hit]  # Legacy, use health instead
        [, gives [number] experience]
```

**Monster Types:**
- `monster-static` - Stationary enemy, doesn't move
- `monster-dynamic` - Chases player when within 10 units, attacks when adjacent
- `monster-boss` - Like dynamic but 4x larger, deals 2 damage, has more health

**Properties:**
- `unique_name` (required) - String identifier, must be unique
- `place at [placement]` (optional) - Starting position
- `health [number]` (optional) - Health points (default: 1, or `killable_hits` if specified)
- `killable [number] hit` (optional, legacy) - Number of hits to kill (converted to health)
- `gives [number] experience` (optional) - Experience points awarded on defeat (default: 0)

**Examples:**
```
monsters:
    monster-static: unique_name="goblin", place at (50, 50), health 3, gives 50 experience
    monster-dynamic: unique_name="ninja", place at (30, 30), health 2, gives 25 experience
    monster-boss: unique_name="dragon", place at (80, 80), health 40, gives 500 experience
    monster-static: unique_name="guard", place at random (10%), health 5, gives 100 experience
```

**Rendering:**
- `monster-static`: 👹 emoji
- `monster-dynamic` / `monster-boss`: 💀 emoji
- `monster-boss`: 4x larger size

**Combat Mechanics:**
- Player attacks: Default punch does 1 damage (Enter/Space when adjacent)
- Monster counter-attacks: 1 damage (static/dynamic), 2 damage (boss)
- Dynamic monsters: Chase player within 10 units, move every 10 frames
- Dynamic monsters: Auto-attack when adjacent (3 second cooldown)
- Health bars shown during combat (3 seconds)
- Defeated monsters: Removed from blocking position, experience awarded
- Player death: Health <= 0 triggers lose condition check

---

## User/Player

Defines the player character.

**Syntax:**
```
user:
    unique_name="[name]"
    [, context "[description]"]
    [, at (x, y)]
```

**Properties:**
- `unique_name` (optional) - Player identifier (default: "player")
- `context "[description]"` (optional) - Context string for game state
- `at (x, y)` (optional) - Starting position (default: [50, 50] if not specified, but validator requires position)

**Examples:**
```
user: unique_name="player", context "hero", at (10, 10)
user: unique_name="adventurer", at (5, 15)
```

**Player State:**
- `health`: 100 (default)
- `experience`: 0 (default)
- `level`: 1 (default)
- `inventory`: [] (empty array)
- `position`: [x, y]
- `talked_to_npcs`: [] (list of NPC unique_names)
- `context`: String from declaration

**Rendering:** 🧙 emoji

**Movement:**
- Arrow keys: Move one cell (up/down/left/right)
- Shift + Arrow keys: Pan camera (doesn't move player)
- Boundaries: Cannot move outside world bounds (0 to width-1, 0 to height-1)
- Collisions: Cannot move into walls, stones, NPCs, or undefeated monsters

---

## NPCs

Non-player characters. Three types: static, dynamic (LLM), state-machine.

**Syntax:**
```
npc:
    [npc_type]:
        unique_name="[name]"
        [, place at [placement]]
        [, context "[description]"]
        [, response "[message]"]
        [, state_machine="[state]"]
        [, emoji="[emoji]"]
        [, agenda="[text]"]
        [, if user has [condition] then [action] [value]]
        [, catch "[message]"]
```

**NPC Types:**
- `npc-static` - Fixed response, no LLM
- `npc-dynamic` - LLM-powered conversation (requires LLM config)
- `npc-state-machine` - State-based responses

**Properties:**
- `unique_name` (required) - String identifier, must be unique
- `place at [placement]` (required for `npc-static`, optional for others) - Position
- `context "[description]"` (optional) - System prompt for LLM NPCs
- `response "[message]"` (optional) - Static response or fallback for LLM NPCs
- `state_machine="[state]"` (optional) - State identifier (default: "idle")
- `emoji="[emoji]"` (optional) - Emoji representation (default: 👤)
- `agenda="[text]"` (optional) - Additional context for LLM NPCs
- `if user has [condition] then [action] [value]` (optional, repeatable) - Conditional responses
- `catch "[message]"` (optional) - Message when interaction unavailable

**Conditional Response Syntax:**
```
if user has item "[item_name]" then response "[message]"
if user has experience [operator] [number] then response "[message]"
if user has health [operator] [number] then response "[message]"
if user has item "[item_name]" then context "[context_string]"
if user has experience [operator] [number] then context "[context_string]"
if user has health [operator] [number] then context "[context_string]"
```

**Operators:** `>`, `<`, `>=`, `<=`, `==`, `!=` (default: `==`)

**Examples:**
```
npc:
    npc-static: unique_name="sheila" place at (2, 2) response "Hello there!"
    npc-static: unique_name="guard" place at (10, 10) response "No entry!" catch "The guard blocks your path"
    
    npc-dynamic: unique_name="echo" place at (10, 10) context "You are Echo, a helpful assistant." response "Fallback message"
    npc-dynamic: unique_name="wizard" place at (20, 20) context "You are a wise wizard." agenda "Help the player find gems" emoji="🧙"
    
    npc-static: unique_name="merchant" place at (5, 5) response "Welcome!" if user has item "gold" then response "Ah, you have gold! I can help you."
    npc-static: unique_name="trainer" place at (15, 15) response "Hello" if user has experience > 100 then response "You're experienced! Here's a tip."
    
    npc-state-machine: unique_name="jim" place at (5, 5) state_machine="idle" response "I am idle."
```

**Rendering:** Custom emoji or default 👤

**Interaction:**
- Press Enter/Space when adjacent (same cell or distance <= 1)
- Static NPCs: Show response immediately (supports `|` separator for random selection)
- Dynamic NPCs: Open dialog with input field, send messages to LLM
- State-machine NPCs: Show response based on state
- Conditional responses: Checked in order, first match wins
- `has_responded` flag: Set to `true` after NPC responds (for quest conditions)
- `talked_to_npcs`: Player's list updated when dialog opens

**LLM Integration:**
- Requires `llm:` configuration in `init:` section
- Endpoint: OpenAI-compatible API (e.g., `http://localhost:1234/v1/chat/completions`)
- Request format: `{messages: [{role: 'system', content: context}, ...history]}`
- Response format: `{choices: [{message: {content: "..."}}]}`
- Fallback: Uses `response` if LLM unavailable
- CORS: Must be served via HTTP server (not `file://`)

---

## LLM Configuration

Configures LLM endpoint for dynamic NPCs.

**Syntax:**
```
llm:
    endpoint "[url]"
    token "[token]"
```

**Properties:**
- `endpoint "[url]"` (optional) - LLM API endpoint URL
- `token "[token]"` (optional) - Authorization token

**Examples:**
```
llm:
    endpoint "http://localhost:1234/v1/chat/completions"
    token "anything"
```

**Requirements:**
- Both properties optional, but both needed for LLM functionality
- Endpoint must be OpenAI-compatible API
- Token used in `Authorization: Bearer [token]` header
- CORS must be enabled on server for browser access

---

## Placement Syntax

Defines where entities are placed in the world.

**Placement Types:**

1. **All cells:**
   ```
   at all
   ```

2. **Single coordinate:**
   ```
   at (x, y)
   ```

3. **Coordinate range:**
   ```
   at (x1, y1) to (x2, y2)
   ```
   Places entity in rectangle from (x1, y1) to (x2, y2) inclusive.

4. **Random percentage:**
   ```
   at random (percentage%)
   ```
   Each cell has `percentage%` chance of containing entity.

**Examples:**
```
place at all
place at (10, 20)
place at (5, 5) to (10, 10)
place at random (30%)
```

**Behavior:**
- `all`: Places on every cell (typically for furniture like grass)
- Coordinate: Exact position
- Range: Fills rectangle (for walls, furniture areas)
- Random: Evaluated at game start, percentage chance per cell

---

## Rules Section

Defines game rules that trigger actions when conditions are met.

**Syntax:**
```
rules:
    if [condition] [and [condition]]* then [action]
```

**Structure:**
- Multiple rules allowed
- Each rule: `if` + one or more conditions (joined with `and`) + `then` + action
- Rules evaluated on every player movement
- Rules can trigger multiple times (unless action prevents re-triggering)

**Examples:**
```
rules:
    if user is at (50, 50) then level up
    if user has item "key" and user is at (100, 100) then level up
    if user has experience > 100 then level up
    if user talked to wizard then level up
```

**See [Conditions](#conditions) and [Actions](#actions) for details.**

---

## Quests Section

Defines quests with conditions and rewards. Quests complete once and mark as completed.

**Syntax (Unnamed Quest):**
```
quests:
    if [condition] [and [condition]]* then [action]
```

**Syntax (Named Quest):**
```
quests:
    [quest_name]:
        if [condition] [and [condition]]* then [action]
```

**Structure:**
- Multiple quests allowed
- Named quests: Identifier followed by colon, then quest definition
- Unnamed quests: Direct `if` statement
- Quests evaluated on every player movement and after NPC interactions
- Quest completes when all conditions met, executes action once, marks as completed

**Examples:**
```
quests:
    if user has item "gem1" and user has item "gem2" then level up
    
    collection_quest:
        if user has item "gem1" and user has item "gem2" and user has item "gem3" then level up
    
    talk_quest:
        if user talked to wizard then level up
    
    experience_quest:
        if user has experience >= 500 then level up
```

**Quest State:**
- `status`: "active" (default) or "completed"
- `completed`: boolean flag
- `id`: Quest name or `quest_{index}` for unnamed quests

---

## End Game Section

Defines win and lose conditions, plus win/lose messages.

**Syntax:**
```
end_game:
    if [condition] [and [condition]]* then [win_result]
    if [condition] [and [condition]]* then [lose_result]
    win_the_game: show "[message]"
    lose_the_game: show "[message]"
```

**Win/Lose Results:**
- `win the game` - Triggers win condition
- `die and lose the game` - Triggers lose condition

**Properties:**
- Multiple win/lose conditions allowed
- All conditions in a single `if` statement must be true (AND logic)
- `win_the_game: show "[message]"` - Custom win message
- `lose_the_game: show "[message]"` - Custom lose message
- Default messages: "You won!" / "You lost!"

**Special Lose Condition:**
- Player health <= 0 automatically triggers lose (if lose condition exists)

**Examples:**
```
end_game:
    if user has item "gem1" and user has item "gem2" then win the game
    if user has 0 health then die and lose the game
    if wizard responded then win the game
    win_the_game: show "Congratulations! You found both gems!"
    lose_the_game: show "Game Over! You were defeated."
```

**Evaluation:**
- Checked after every player movement, combat, item pickup, and quest completion
- Win conditions: All must be true simultaneously
- Lose conditions: All must be true simultaneously OR health <= 0

---

## On Game Start Section

Defines splash screen shown at game start.

**Syntax:**
```
on_game_start:
    display_title: [title_string_or_text]
    display_text: "[message]"
    display_link: "[anchor_text]", "[url]"
```

**Properties:**
- `display_title` (optional) - Title text (string or unquoted text until next `display_` command)
- `display_text` (optional, repeatable) - Text lines shown as paragraphs
- `display_link` (optional, repeatable) - Links with anchor text and URL

**Title Syntax:**
- Quoted string: `display_title: "My Game Title"`
- Unquoted text: `display_title: My Game Title` (collects tokens until next `display_` command)

**Examples:**
```
on_game_start:
    display_title: "The Great Dungeon Journey!"
    display_text: "Journey through 12 chambers"
    display_text: "Defeat monsters and collect gems"
    display_text: "Reach the final chamber to win"
    display_link: "github", "https://github.com/user/repo"
    display_link: "documentation", "https://docs.example.com"
```

**Behavior:**
- Splash screen shown on game load
- User clicks "Start Game" button to close
- Title: Large gold text at top
- Text: White paragraphs below title
- Links: Styled buttons that open in new tab
- Background: Dark overlay with gradient blue box

---

## Conditions

Conditions used in rules, quests, and end_game sections.

### Position Condition

Checks if entity is at specific coordinate.

**Syntax:**
```
[entity] is at (x, y)
```

**Examples:**
```
user is at (50, 50)
goblin is at (10, 20)
```

**Entity Types:** `user`, NPC unique_name, monster unique_name, item unique_name, mythic unique_name

---

### Has Item Condition

Checks if entity (typically user) has item in inventory.

**Syntax:**
```
[entity] has item "[item_name]"
```

**Examples:**
```
user has item "gem1"
user has item "sword"
```

**Entity:** Usually `user`, but can be any entity (though only user has inventory)

---

### Has Attribute Condition (Comparison)

Checks if entity has attribute value meeting comparison.

**Syntax:**
```
[entity] has [attribute] [operator] [number]
```

**Attributes:**
- `experience` - Experience points
- `health` - Health points

**Operators:** `>`, `<`, `>=`, `<=`, `==`, `!=` (default: `==` if omitted)

**Examples:**
```
user has experience > 100
user has health < 50
user has experience >= 500
user has health == 100
```

**Entity:** Usually `user`, but can be any entity with numeric attributes

---

### Talked To Condition

Checks if user has talked to specific NPC.

**Syntax:**
```
user talked to [npc_name]
```

**Examples:**
```
user talked to wizard
user talked to merchant
```

**Behavior:**
- `npc_name` is NPC's `unique_name`
- Condition true after dialog opens (not after response)
- Tracked in `user.talked_to_npcs` array

---

### Responded To Condition

Checks if specific NPC has responded (for LLM NPCs).

**Syntax:**
```
[npc_name] responded
[npc_name] responds
```

**Examples:**
```
wizard responded
ancient_wisdom_keeper responds
```

**Behavior:**
- `npc_name` is NPC's `unique_name`
- Condition true after NPC sends response (LLM or fallback)
- Sets `npc.has_responded = true`
- Used for quests requiring NPC interaction completion

---

### Combining Conditions

Multiple conditions joined with `and`:

```
if [condition1] and [condition2] and [condition3] then [action]
```

All conditions must be true (AND logic).

---

## Actions

Actions executed when conditions are met.

### Level Up Action

Increases player level by 1.

**Syntax:**
```
level up
```

**Examples:**
```
if user has experience > 100 then level up
if user has item "gem1" then level up
```

**Behavior:**
- Increments `user.level`
- Shows "Level Up!" message at player position

---

### Talk Action

Triggers NPC interaction (typically implicit, not commonly used in rules).

**Syntax:**
```
talk-[npc_type]
```

**Types:** `talk-static`, `talk-dynamic`, `talk-state-machine`

**Examples:**
```
if user is at (10, 10) then talk-static
```

**Note:** Usually NPCs are interacted with via Enter/Space key, not rules.

---

### Command Action

Executes game command (future extensibility).

**Syntax:**
```
[command_name]
```

**Examples:**
```
if user has item "key" then unlock_door
```

**Note:** Currently limited command support, mainly `level up` is implemented.

---

## Operators

Comparison operators for numeric conditions.

**Operators:**
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal
- `<=` - Less than or equal
- `==` - Equal (default if omitted)
- `!=` - Not equal

**Usage:**
```
user has experience > 100
user has health < 50
user has experience >= 500
user has health <= 0
```

**Default:** If operator omitted in comparison, defaults to `==`.

---

## Data Types

### Numbers

Integers or floats:

```
100
50
3.14
0.5
```

**Usage:** Coordinates, health, experience, percentages, etc.

---

### Strings

Quoted text (single or double quotes):

```
"Hello, world!"
'This is a string'
"Item name with spaces"
```

**Escape sequences:**
- `\n` - Newline
- `\t` - Tab
- `\\` - Backslash
- `\"` - Double quote (in double-quoted strings)
- `\'` - Single quote (in single-quoted strings)

**Usage:** Unique names, messages, context, responses, etc.

---

### Booleans

Boolean literals:

```
true
false
```

**Usage:** Variable values, flags.

---

### Percentages

Number followed by `%`:

```
30%
50%
100%
```

**Usage:** Random placement probability.

---

### Identifiers

Alphanumeric with underscores/hyphens:

```
user
gem1
npc-static
monster-boss
unique_name
```

**Usage:** Entity names, keywords, variable names, quest names.

**Rules:**
- Start with letter or underscore
- Can contain letters, numbers, underscores, hyphens
- Case-sensitive for entity names
- Keywords are case-insensitive

---

## Game Mechanics

### Movement

- **Arrow Keys:** Move player one cell (up/down/left/right)
- **Shift + Arrow Keys:** Pan camera without moving player
- **Boundaries:** Cannot move outside world (0 to width-1, 0 to height-1)
- **Collisions:** Blocked by walls, stones, NPCs, undefeated monsters
- **Viewport:** Auto-centers on player (unless panning with Shift)

### Combat

- **Attack:** Press Enter or Space when adjacent to monster (same cell or distance <= 1)
- **Player Damage:** Default punch = 1 damage
- **Monster Counter-Attack:** 1 damage (static/dynamic), 2 damage (boss)
- **Health Bars:** Shown during combat for 3 seconds
- **Defeat:** Monster removed when health <= 0, experience awarded
- **Dynamic Monsters:** Chase player within 10 units, auto-attack when adjacent (3s cooldown)

### Inventory

- **Pickup:** Automatic when stepping on item/mythic with `can be picked up by the user`
- **Items:** Added to `user.inventory` array
- **Healing Items:** `item-heal` restores 25% max health on pickup
- **Display:** Inventory shown in "Inventory" dropdown menu

### Interactions

- **NPCs:** Press Enter/Space when adjacent (same cell or distance <= 1)
- **Static NPCs:** Show response immediately
- **Dynamic NPCs:** Open dialog with input field for LLM conversation
- **Items/Mythics:** Auto-interact when stepping on cell
- **Monsters:** Enter/Space to attack when adjacent

### Experience & Leveling

- **Experience:** Gained by defeating monsters
- **Level:** Increased by `level up` action in rules/quests
- **Display:** Shown in "Status" dropdown menu

### Save/Load

- **Save:** "Save" button downloads `game_save.json`
- **Load:** "Load" button opens file picker, restores game state
- **Format:** JSON with version, timestamp, and full game state

### UI Elements

- **Menu Bar:** Save, Load, Status, Inventory, Chat History, Quest-Status dropdowns
- **Dialog Panel:** Slides in from right for NPC conversations
- **Splash Screen:** Shown on game start (if `on_game_start:` configured)
- **Interaction Text:** Temporary messages shown at entity positions
- **Health Bars:** Shown during combat

### Rendering

- **Grid:** Cell-based world with emoji sprites
- **Zoom:** `+`/`-` keys to zoom in/out (0.5x to 3.0x)
- **Cell Size:** 40px base, scaled by zoom
- **Viewport:** Renders visible cells only for performance
- **Emojis:**
  - 🧙 - Player
  - 👹 - Static monster
  - 💀 - Dynamic/Boss monster
  - 👤 - NPC (default)
  - 💎 - Item
  - 💠 - Mythic
  - 🧱 - Wall/Stone
  - 🟩 - Grass
  - 🏠 - Default furniture

---

## Validation Rules

The compiler validates:

1. **Required Sections:** `init:` must be present
2. **Uniqueness:** All `unique_name` values must be unique across:
   - Mythics
   - Items
   - Monsters
   - NPCs
   - User
3. **Collisions:** Monsters and NPCs cannot overlap at same coordinate (items/mythics can)
4. **Semantics:**
   - User must have initial position
   - `npc-static` must have placement
   - Rules must reference valid entities
5. **Syntax:** Proper tokenization and parsing (reports line/column errors)

---

## Compilation Process

1. **Lexing:** Source code → Tokens (keywords, identifiers, operators, literals)
2. **Parsing:** Tokens → AST (Abstract Syntax Tree)
3. **Validation:** AST → Error checking (uniqueness, collisions, semantics)
4. **Code Generation:** AST → HTML/JavaScript game file
5. **Output:** Single HTML file with embedded CSS and JavaScript

---

## Example Complete Game

```
init:
    world: 100 x 100 grid
    furniture:
        grass at all
        wall at (0, 0) to (100, 0)
        wall at (0, 0) to (0, 100)
        wall at (100, 0) to (100, 100)
        wall at (0, 100) to (100, 100)
    mytics:
        mythic-static: unique_name="gem1", place at (20, 20), can be picked up by the user
        mythic-static: unique_name="gem2", place at (80, 80), can be picked up by the user
    items:
        item-heal: unique_name="potion", place at (50, 50), can be picked up by the user
    monsters:
        monster-static: unique_name="goblin", place at (50, 50), health 3, gives 50 experience
        monster-dynamic: unique_name="ninja", place at (30, 30), health 2, gives 25 experience
    npc:
        npc-static: unique_name="wizard" place at (10, 10) response "Hello! Find the gems!"
        npc-dynamic: unique_name="merchant" place at (90, 90) context "You are a helpful merchant." response "Welcome!"
    user: unique_name="player", context "hero", at (5, 5)
rules:
    if user is at (50, 50) then level up
quests:
    gem_quest:
        if user has item "gem1" and user has item "gem2" then level up
    talk_quest:
        if user talked to wizard then level up
end_game:
    if user has item "gem1" and user has item "gem2" then win the game
    if wizard responded then win the game
    win_the_game: show "Congratulations! You found both gems!"
on_game_start:
    display_title: "Dungeon Adventure"
    display_text: "Find the two gems to win!"
    display_text: "Talk to NPCs and defeat monsters"
    display_link: "GitHub", "https://github.com/example"
```

---

## Keywords Reference

**Section Keywords:**
- `init`, `rules`, `quests`, `end_game`, `on_game_start`

**Entity Keywords:**
- `world`, `furniture`, `mytics`, `items`, `monsters`, `user`, `npc`, `llm`

**Control Keywords:**
- `if`, `then`, `and`, `let`

**Action Keywords:**
- `level up`, `win`, `lose`, `die`, `show`

**Property Keywords:**
- `at`, `is`, `has`, `place`, `can`, `be`, `picked`, `up`, `by`, `the`, `gives`, `catch`

**Value Keywords:**
- `all`, `random`, `to`, `of`, `with`, `towards`

**Type Keywords:**
- `health`, `experience`, `damage`, `killable`, `hit`

**Display Keywords:**
- `display_title`, `display_text`, `display_link`

**Operators:**
- `=`, `==`, `!=`, `>`, `<`, `>=`, `<=`

**Literals:**
- `true`, `false`

---

## Notes

- **Case Sensitivity:** Keywords are case-insensitive, but entity names are case-sensitive
- **Whitespace:** Flexible, but newlines separate statements
- **Comments:** `#` starts single-line comment
- **String Quotes:** Single or double quotes allowed, must match
- **Coordinates:** Zero-indexed (0, 0) is top-left
- **Entity Names:** Must be unique across all entity types
- **Placement:** Random placement evaluated at game start
- **LLM:** Requires HTTP server (not `file://`) due to CORS
- **Browser:** Modern browser with JavaScript enabled required

---

*End of Reference*

