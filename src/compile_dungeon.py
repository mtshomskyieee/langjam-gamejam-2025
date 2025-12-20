#!/usr/bin/env python3
"""
Compiler for Dungeon Game DSL
Compiles a custom DSL into a playable HTML/JavaScript game.

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
"""

import re
import sys
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TokenType(Enum):
    # Keywords
    INIT = "init"
    RULES = "rules"
    QUESTS = "quests"
    END_GAME = "end_game"
    ON_GAME_START = "on_game_start"
    WORLD = "world"
    FURNITURE = "furniture"
    MYTHICS = "mytics"
    ITEMS = "items"
    MONSTERS = "monsters"
    USER = "user"
    NPC = "NPC"
    LET = "let"
    CATCH = "catch"
    IF = "if"
    THEN = "then"
    AND = "and"
    AT = "at"
    IS = "is"
    HAS = "has"
    SHOW = "show"
    WIN = "win"
    LOSE = "lose"
    DIE = "die"
    LEVEL_UP = "level up"
    MOVE = "move"
    TALK = "talk"
    ATTACK = "attack"
    USE = "use"
    SET = "set"
    TOUCH = "touch"
    PLACE = "place"
    CHECK_INVENTORY = "check_inventory"
    TOWARDS = "towards"
    WITH = "with"
    CAN = "can"
    BE = "be"
    PICKED = "picked"
    UP = "up"
    BY = "by"
    THE = "the"
    GIVES = "gives"
    EXPERIENCE = "experience"
    HEALTH = "health"
    DAMAGE = "damage"
    KILLABLE = "killable"
    HIT = "hit"
    RANDOM = "random"
    ALL = "all"
    TO = "to"
    OF = "of"
    
    # Types
    IDENTIFIER = "identifier"
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    PERCENTAGE = "percentage"
    
    # Operators
    EQUALS = "="
    COMMA = ","
    COLON = ":"
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    EQ = "=="
    NE = "!="
    
    # Special
    NEWLINE = "newline"
    COMMENT = "comment"
    EOF = "eof"


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Keywords mapping
        self.keywords = {
            'init': TokenType.INIT,
            'rules': TokenType.RULES,
            'quests': TokenType.QUESTS,
            'end_game': TokenType.END_GAME,
            'on_game_start': TokenType.ON_GAME_START,
            'world': TokenType.WORLD,
            'furniture': TokenType.FURNITURE,
            'mytics': TokenType.MYTHICS,
            'items': TokenType.ITEMS,
            'monsters': TokenType.MONSTERS,
            'user': TokenType.USER,
            'npc': TokenType.NPC,
            'let': TokenType.LET,
            'catch': TokenType.CATCH,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'and': TokenType.AND,
            'at': TokenType.AT,
            'is': TokenType.IS,
            'has': TokenType.HAS,
            'show': TokenType.SHOW,
            'win': TokenType.WIN,
            'lose': TokenType.LOSE,
            'die': TokenType.DIE,
            'level': TokenType.LEVEL_UP,
            'move': TokenType.MOVE,
            'talk': TokenType.TALK,
            'attack': TokenType.ATTACK,
            'use': TokenType.USE,
            'set': TokenType.SET,
            'touch': TokenType.TOUCH,
            'place': TokenType.PLACE,
            'check_inventory': TokenType.CHECK_INVENTORY,
            'towards': TokenType.TOWARDS,
            'with': TokenType.WITH,
            'can': TokenType.CAN,
            'be': TokenType.BE,
            'picked': TokenType.PICKED,
            'up': TokenType.UP,
            'by': TokenType.BY,
            'the': TokenType.THE,
            'gives': TokenType.GIVES,
            'experience': TokenType.EXPERIENCE,
            'health': TokenType.HEALTH,
            'damage': TokenType.DAMAGE,
            'killable': TokenType.KILLABLE,
            'hit': TokenType.HIT,
            'random': TokenType.RANDOM,
            'all': TokenType.ALL,
            'to': TokenType.TO,
            'of': TokenType.OF,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
        }
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.text):
            return None
        return self.text[pos]
    
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_string(self) -> str:
        quote = self.current_char()
        self.advance()  # Skip opening quote
        value = ""
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    value += '\n'
                elif self.current_char() == 't':
                    value += '\t'
                elif self.current_char() == '\\':
                    value += '\\'
                elif self.current_char() == '"':
                    value += '"'
                else:
                    value += self.current_char()
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        if self.current_char() == quote:
            self.advance()  # Skip closing quote
        return value
    
    def read_number(self) -> Tuple[float, bool]:
        """Returns (value, is_float)"""
        num_str = ""
        is_float = False
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    break
                is_float = True
            num_str += self.current_char()
            self.advance()
        return (float(num_str) if is_float else int(num_str), is_float)
    
    def read_identifier(self) -> str:
        ident = ""
        while self.current_char() and (self.current_char().isalnum() or self.current_char() in '_-'):
            ident += self.current_char()
            self.advance()
        return ident
    
    def read_comment(self):
        while self.current_char() and self.current_char() != '\n':
            self.advance()
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.text):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            line = self.line
            col = self.column
            
            # Comments
            if char == '#':
                self.read_comment()
                continue
            
            # Newline
            if char == '\n':
                self.advance()
                continue
            
            # Strings
            if char in '"\'':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, line, col))
                continue
            
            # Numbers
            if char.isdigit():
                value, _ = self.read_number()
                # Check for percentage
                if self.current_char() == '%':
                    self.advance()
                    self.tokens.append(Token(TokenType.PERCENTAGE, value, line, col))
                else:
                    self.tokens.append(Token(TokenType.NUMBER, value, line, col))
                continue
            
            # Operators
            if char == '=':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.EQ, "==", line, col))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUALS, "=", line, col))
                continue
            
            if char == '>':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.GTE, ">=", line, col))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.GT, ">", line, col))
                continue
            
            if char == '<':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.LTE, "<=", line, col))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.LT, "<", line, col))
                continue
            
            if char == '!':
                if self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.NE, "!=", line, col))
                else:
                    raise SyntaxError(f"Unexpected character '!' at line {line}, column {col}")
                continue
            
            if char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ",", line, col))
                continue
            
            if char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ":", line, col))
                continue
            
            if char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ";", line, col))
                continue
            
            if char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, "(", line, col))
                continue
            
            if char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ")", line, col))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                ident = self.read_identifier()
                # Check for multi-word keywords
                if ident == 'level' and self.current_char() == ' ':
                    next_pos = self.pos
                    while self.text[next_pos:next_pos+3] == ' up':
                        ident += ' up'
                        self.pos = next_pos + 3
                        break
                
                token_type = self.keywords.get(ident.lower(), TokenType.IDENTIFIER)
                if token_type == TokenType.BOOLEAN:
                    value = ident.lower() == 'true'
                    self.tokens.append(Token(TokenType.BOOLEAN, value, line, col))
                else:
                    self.tokens.append(Token(token_type, ident, line, col))
                continue
            
            # Unknown character
            raise SyntaxError(f"Unexpected character '{char}' at line {line}, column {col}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# AST Nodes
@dataclass
class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    variables: List['VariableDecl'] = field(default_factory=list)
    init_section: Optional['InitSection'] = None
    rules_section: Optional['RulesSection'] = None
    quests_section: Optional['QuestsSection'] = None
    end_game_section: Optional['EndGameSection'] = None
    on_game_start_section: Optional['OnGameStartSection'] = None


@dataclass
class VariableDecl(ASTNode):
    name: str
    value: Any


@dataclass
class InitSection(ASTNode):
    world: Optional['WorldDecl'] = None
    furniture: List['FurnitureItem'] = field(default_factory=list)
    mythics: List['MythicItem'] = field(default_factory=list)
    items: List['ItemDecl'] = field(default_factory=list)
    monsters: List['MonsterDecl'] = field(default_factory=list)
    user: Optional['UserDecl'] = None
    npcs: List['NPCDecl'] = field(default_factory=list)
    llm_endpoint: Optional[str] = None
    llm_token: Optional[str] = None


@dataclass
class WorldDecl(ASTNode):
    width: int = 100
    height: int = 100


@dataclass
class FurnitureItem(ASTNode):
    name: str
    placement: 'Placement'


@dataclass
class Placement(ASTNode):
    type: str  # 'all', 'coordinate', 'range', 'random'
    coord1: Optional[Tuple[int, int]] = None
    coord2: Optional[Tuple[int, int]] = None
    percentage: Optional[float] = None  # For random placement


@dataclass
class MythicItem(ASTNode):
    unique_name: str
    placement: Optional[Placement] = None
    can_pickup: bool = False
    catch_message: Optional[str] = None


@dataclass
class ItemDecl(ASTNode):
    item_type: str
    unique_name: str
    placement: Optional[Placement] = None
    can_pickup: bool = False
    effect: Optional[str] = None
    damage: Optional[int] = None
    catch_message: Optional[str] = None


@dataclass
class MonsterDecl(ASTNode):
    unique_name: str
    monster_type: str = 'monster-static'  # 'monster-static', 'monster-dynamic', or 'monster-boss'
    placement: Optional[Placement] = None
    health: Optional[int] = None
    killable_hits: Optional[int] = None  # Legacy support
    experience: Optional[int] = None


@dataclass
class UserDecl(ASTNode):
    unique_name: str
    context: Optional[str] = None
    position: Optional[Tuple[int, int]] = None


@dataclass
class NPCDecl(ASTNode):
    npc_type: str  # 'npc-static', 'npc-dynamic', 'npc-state-machine'
    unique_name: str
    placement: Optional[Placement] = None
    context: Optional[str] = None
    response: Optional[str] = None
    state_machine: Optional[str] = None
    emoji: Optional[str] = None
    agenda: Optional[str] = None
    conditions: List['NPCCondition'] = field(default_factory=list)
    catch_message: Optional[str] = None


@dataclass
class NPCCondition(ASTNode):
    condition_type: str  # 'item', 'experience', 'health'
    then_action: str  # 'response' or 'context'
    operator: Optional[str] = None
    value: Any = None
    action_value: str = None


@dataclass
class RulesSection(ASTNode):
    rules: List['Rule'] = field(default_factory=list)


@dataclass
class Rule(ASTNode):
    conditions: List['Condition'] = field(default_factory=list)
    action: 'Action' = None


@dataclass
class Condition(ASTNode):
    type: str  # 'position', 'has', 'comparison', 'talked_to', 'responded_to'
    entity: str
    operator: Optional[str] = None
    value: Any = None
    position: Optional[Tuple[int, int]] = None


@dataclass
class Action(ASTNode):
    type: str  # 'talk-dynamic', 'talk-static', 'talk-state-machine', 'level up', 'command'
    command: Optional[str] = None
    target: Optional[str] = None
    value: Optional[Any] = None


@dataclass
class QuestsSection(ASTNode):
    quests: List['Quest'] = field(default_factory=list)


@dataclass
class Quest(ASTNode):
    name: Optional[str] = None
    conditions: List[Condition] = field(default_factory=list)
    action: Action = None


@dataclass
class EndGameSection(ASTNode):
    conditions: List['EndCondition'] = field(default_factory=list)
    win_message: Optional[str] = None
    lose_message: Optional[str] = None


@dataclass
class OnGameStartSection(ASTNode):
    title: Optional[str] = None
    text_lines: List[str] = field(default_factory=list)
    links: List[Tuple[str, str]] = field(default_factory=list)  # List of (anchor_text, url) tuples


@dataclass
class EndCondition(ASTNode):
    condition: Condition
    result: Optional[str] = None  # 'win the game' or 'die and lose the game'


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[pos]
    
    def advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1
    
    def expect(self, token_type: TokenType, value: Any = None):
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}, column {token.column}")
        if value is not None and token.value != value:
            raise SyntaxError(f"Expected {value}, got {token.value} at line {token.line}, column {token.column}")
        self.advance()
        return token
    
    def parse(self) -> Program:
        program = Program()
        
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.LET:
                program.variables.append(self.parse_variable())
            elif self.current_token().type == TokenType.INIT:
                program.init_section = self.parse_init_section()
            elif self.current_token().type == TokenType.RULES:
                program.rules_section = self.parse_rules_section()
            elif self.current_token().type == TokenType.QUESTS:
                program.quests_section = self.parse_quests_section()
            elif self.current_token().type == TokenType.END_GAME:
                program.end_game_section = self.parse_end_game_section()
            elif self.current_token().type == TokenType.ON_GAME_START:
                program.on_game_start_section = self.parse_on_game_start_section()
            else:
                raise SyntaxError(f"Unexpected token {self.current_token().type} at line {self.current_token().line}")
        
        return program
    
    def parse_variable(self) -> VariableDecl:
        self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.EQUALS)
        value = self.parse_value()
        return VariableDecl(name, value)
    
    def parse_value(self) -> Any:
        token = self.current_token()
        if token.type == TokenType.NUMBER:
            self.advance()
            return token.value
        elif token.type == TokenType.STRING:
            self.advance()
            return token.value
        elif token.type == TokenType.BOOLEAN:
            self.advance()
            return token.value
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return token.value
        else:
            raise SyntaxError(f"Unexpected value type {token.type} at line {token.line}")
    
    def parse_init_section(self) -> InitSection:
        self.expect(TokenType.INIT)
        self.expect(TokenType.COLON)
        
        init = InitSection()
        
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.WORLD:
                init.world = self.parse_world()
            elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'llm':
                self.parse_llm_config(init)
            elif self.current_token().type == TokenType.FURNITURE:
                init.furniture.extend(self.parse_furniture())
            elif self.current_token().type == TokenType.MYTHICS:
                init.mythics.extend(self.parse_mythics())
            elif self.current_token().type == TokenType.ITEMS:
                init.items.extend(self.parse_items())
            elif self.current_token().type == TokenType.MONSTERS:
                init.monsters.extend(self.parse_monsters())
            elif self.current_token().type == TokenType.USER:
                init.user = self.parse_user()
            elif self.current_token().type == TokenType.NPC:
                init.npcs.extend(self.parse_npcs())
            else:
                break
        
        return init
    
    def parse_world(self) -> WorldDecl:
        self.expect(TokenType.WORLD)
        self.expect(TokenType.COLON)
        
        if self.current_token().type == TokenType.NUMBER:
            width = int(self.expect(TokenType.NUMBER).value)
            self.expect(TokenType.IDENTIFIER)  # 'x'
            height = int(self.expect(TokenType.NUMBER).value)
            self.expect(TokenType.IDENTIFIER)  # 'grid'
            return WorldDecl(width, height)
        else:
            self.expect(TokenType.IDENTIFIER)  # 'grid'
            return WorldDecl(100, 100)  # Default
    
    def parse_furniture(self) -> List[FurnitureItem]:
        self.expect(TokenType.FURNITURE)
        self.expect(TokenType.COLON)
        
        furniture = []
        while self.current_token().type == TokenType.IDENTIFIER:
            # Check if next token is AT - if not, we've hit a new section
            if self.peek_token().type != TokenType.AT:
                break
            name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.AT)
            placement = self.parse_placement()
            furniture.append(FurnitureItem(name, placement))
        
        return furniture
    
    def parse_placement(self) -> Placement:
        if self.current_token().type == TokenType.ALL:
            self.advance()
            return Placement('all')
        elif self.current_token().type == TokenType.RANDOM:
            self.advance()
            self.expect(TokenType.LPAREN)
            percentage = self.expect(TokenType.PERCENTAGE).value
            self.expect(TokenType.RPAREN)
            return Placement('random', None, None, percentage)
        elif self.current_token().type == TokenType.LPAREN:
            coord1 = self.parse_coordinate()
            if self.current_token().type == TokenType.TO:
                self.advance()
                coord2 = self.parse_coordinate()
                return Placement('range', coord1, coord2)
            else:
                return Placement('coordinate', coord1)
        else:
            raise SyntaxError(f"Unexpected placement at line {self.current_token().line}")
    
    def parse_coordinate(self) -> Tuple[int, int]:
        self.expect(TokenType.LPAREN)
        x = int(self.expect(TokenType.NUMBER).value)
        self.expect(TokenType.COMMA)
        y = int(self.expect(TokenType.NUMBER).value)
        self.expect(TokenType.RPAREN)
        return (x, y)
    
    def parse_mythics(self) -> List[MythicItem]:
        self.expect(TokenType.MYTHICS)
        self.expect(TokenType.COLON)
        
        mythics = []
        while self.current_token().type == TokenType.IDENTIFIER:
            # mythic-static:
            self.expect(TokenType.IDENTIFIER)  # 'mythic-static'
            self.expect(TokenType.COLON)
            
            unique_name = None
            placement = None
            can_pickup = False
            catch_message = None
            
            # Parse properties
            while self.current_token().type in [TokenType.IDENTIFIER, TokenType.STRING, TokenType.AT, TokenType.CAN, TokenType.CATCH, TokenType.COMMA, TokenType.PLACE]:
                # Skip commas
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
                    continue
                    
                if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'unique_name':
                    self.advance()
                    self.expect(TokenType.EQUALS)
                    unique_name = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.PLACE:
                    self.advance()
                    self.expect(TokenType.AT)
                    placement = self.parse_placement()
                elif self.current_token().type == TokenType.CAN:
                    # "can be picked up by the user"
                    self.advance()
                    self.expect(TokenType.BE)
                    self.expect(TokenType.PICKED)
                    self.expect(TokenType.UP)
                    self.expect(TokenType.BY)
                    self.expect(TokenType.THE)
                    # Accept either USER token or IDENTIFIER for 'user'
                    if self.current_token().type == TokenType.USER:
                        self.advance()
                    else:
                        self.expect(TokenType.IDENTIFIER)  # 'user'
                    can_pickup = True
                elif self.current_token().type == TokenType.CATCH:
                    self.advance()
                    catch_message = self.expect(TokenType.STRING).value
                else:
                    break
            
            if unique_name:
                mythics.append(MythicItem(unique_name, placement, can_pickup, catch_message))
        
        return mythics
    
    def parse_items(self) -> List[ItemDecl]:
        self.expect(TokenType.ITEMS)
        self.expect(TokenType.COLON)
        
        items = []
        while self.current_token().type == TokenType.IDENTIFIER:
            item_type = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            
            unique_name = None
            placement = None
            can_pickup = False
            effect = None
            damage = None
            catch_message = None
            
            # Parse properties
            while self.current_token().type in [TokenType.IDENTIFIER, TokenType.STRING, TokenType.AT, TokenType.CAN, TokenType.CATCH, TokenType.DAMAGE, TokenType.COMMA, TokenType.PLACE]:
                # Skip commas
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
                    continue
                    
                if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'unique_name':
                    self.advance()
                    self.expect(TokenType.EQUALS)
                    unique_name = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.PLACE:
                    self.advance()
                    self.expect(TokenType.AT)
                    placement = self.parse_placement()
                elif self.current_token().type == TokenType.CAN:
                    # "can be used to" or "can be picked up by the user"
                    self.advance()
                    self.expect(TokenType.BE)
                    if self.current_token().type == TokenType.USE:
                        self.advance()
                        self.expect(TokenType.TO)
                        # Parse effect description
                        effect_parts = []
                        while self.current_token().type not in [TokenType.COMMA, TokenType.CATCH, TokenType.EOF] and self.current_token().type != TokenType.IDENTIFIER:
                            if self.current_token().type == TokenType.STRING:
                                effect = self.expect(TokenType.STRING).value
                                break
                            elif self.current_token().type == TokenType.IDENTIFIER:
                                effect_parts.append(self.expect(TokenType.IDENTIFIER).value)
                            else:
                                self.advance()
                        if not effect:
                            effect = ' '.join(effect_parts)
                    elif self.current_token().type == TokenType.PICKED:
                        self.expect(TokenType.PICKED)
                        self.expect(TokenType.UP)
                        self.expect(TokenType.BY)
                        self.expect(TokenType.THE)
                        # Accept either USER token or IDENTIFIER for 'user'
                        if self.current_token().type == TokenType.USER:
                            self.advance()
                        else:
                            self.expect(TokenType.IDENTIFIER)  # 'user'
                        can_pickup = True
                elif self.current_token().type == TokenType.DAMAGE:
                    self.advance()
                    damage = int(self.expect(TokenType.NUMBER).value)
                elif self.current_token().type == TokenType.CATCH:
                    self.advance()
                    catch_message = self.expect(TokenType.STRING).value
                else:
                    break
            
            if unique_name:
                items.append(ItemDecl(item_type, unique_name, placement, can_pickup, effect, damage, catch_message))
        
        return items
    
    def parse_monsters(self) -> List[MonsterDecl]:
        self.expect(TokenType.MONSTERS)
        self.expect(TokenType.COLON)
        
        monsters = []
        while self.current_token().type == TokenType.IDENTIFIER:
            # monster-static:, monster-dynamic:, or monster-boss:
            monster_type_token = self.expect(TokenType.IDENTIFIER)
            monster_type = monster_type_token.value  # 'monster-static', 'monster-dynamic', or 'monster-boss'
            if monster_type not in ['monster-static', 'monster-dynamic', 'monster-boss']:
                raise SyntaxError(f"Expected 'monster-static', 'monster-dynamic', or 'monster-boss', got '{monster_type}' at line {monster_type_token.line}")
            self.expect(TokenType.COLON)
            
            unique_name = None
            placement = None
            health = None
            killable_hits = None
            experience = None
            
            # Parse properties
            while self.current_token().type in [TokenType.IDENTIFIER, TokenType.STRING, TokenType.AT, TokenType.HEALTH, TokenType.KILLABLE, TokenType.GIVES, TokenType.COMMA, TokenType.PLACE]:
                # Skip commas
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
                    continue
                    
                if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'unique_name':
                    self.advance()
                    self.expect(TokenType.EQUALS)
                    unique_name = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.PLACE:
                    self.advance()
                    self.expect(TokenType.AT)
                    placement = self.parse_placement()
                elif self.current_token().type == TokenType.HEALTH:
                    self.advance()
                    health = int(self.expect(TokenType.NUMBER).value)
                elif self.current_token().type == TokenType.KILLABLE:
                    self.advance()
                    killable_hits = int(self.expect(TokenType.NUMBER).value)
                    self.expect(TokenType.HIT)
                elif self.current_token().type == TokenType.GIVES:
                    self.advance()
                    experience = int(self.expect(TokenType.NUMBER).value)
                    self.expect(TokenType.EXPERIENCE)
                else:
                    break
            
            if unique_name:
                monsters.append(MonsterDecl(unique_name, monster_type, placement, health, killable_hits, experience))
        
        return monsters
    
    def parse_user(self) -> UserDecl:
        self.expect(TokenType.USER)
        self.expect(TokenType.COLON)
        
        unique_name = None
        context = None
        position = None
        
        # Parse properties
        while self.current_token().type in [TokenType.IDENTIFIER, TokenType.STRING, TokenType.AT, TokenType.COMMA]:
            # Skip commas
            if self.current_token().type == TokenType.COMMA:
                self.advance()
                continue
                
            if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'unique_name':
                self.advance()
                self.expect(TokenType.EQUALS)
                unique_name = self.expect(TokenType.STRING).value
            elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'context':
                self.advance()
                context = self.expect(TokenType.STRING).value
            elif self.current_token().type == TokenType.AT:
                self.advance()
                position = self.parse_coordinate()
            else:
                break
        
        return UserDecl(unique_name or "player", context, position)
    
    def parse_llm_config(self, init: InitSection):
        self.expect(TokenType.IDENTIFIER)  # 'llm'
        self.expect(TokenType.COLON)
        
        while self.current_token().type == TokenType.IDENTIFIER:
            if self.current_token().value == 'endpoint':
                self.advance()
                init.llm_endpoint = self.expect(TokenType.STRING).value
            elif self.current_token().value == 'token':
                self.advance()
                init.llm_token = self.expect(TokenType.STRING).value
            else:
                break
    
    def parse_npcs(self) -> List[NPCDecl]:
        self.expect(TokenType.NPC)
        self.expect(TokenType.COLON)
        
        npcs = []
        while self.current_token().type == TokenType.IDENTIFIER:
            npc_type = self.expect(TokenType.IDENTIFIER).value  # 'npc-static', 'npc-dynamic', etc.
            self.expect(TokenType.COLON)
            
            unique_name = None
            placement = None
            context = None
            response = None
            state_machine = None
            emoji = None
            agenda = None
            conditions = []
            catch_message = None
            
            # Parse properties
            while self.current_token().type in [TokenType.IDENTIFIER, TokenType.STRING, TokenType.IF, TokenType.CATCH, TokenType.PLACE, TokenType.AT]:
                if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'unique_name':
                    self.advance()
                    self.expect(TokenType.EQUALS)
                    unique_name = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.PLACE:
                    self.advance()
                    self.expect(TokenType.AT)
                    placement = self.parse_placement()
                elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'context':
                    self.advance()
                    context = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'response':
                    self.advance()
                    response = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'state_machine':
                    self.advance()
                    self.expect(TokenType.EQUALS)
                    state_machine = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'emoji':
                    self.advance()
                    self.expect(TokenType.EQUALS)
                    emoji = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'agenda':
                    self.advance()
                    agenda = self.expect(TokenType.STRING).value
                elif self.current_token().type == TokenType.IF:
                    conditions.append(self.parse_npc_condition())
                elif self.current_token().type == TokenType.CATCH:
                    self.advance()
                    catch_message = self.expect(TokenType.STRING).value
                else:
                    break
            
            if unique_name:
                npcs.append(NPCDecl(npc_type, unique_name, placement, context, response, state_machine, emoji, agenda, conditions, catch_message))
        
        return npcs
    
    def parse_npc_condition(self) -> NPCCondition:
        self.expect(TokenType.IF)
        self.expect(TokenType.IDENTIFIER)  # 'user'
        self.expect(TokenType.HAS)
        
        condition_type = self.expect(TokenType.IDENTIFIER).value  # 'item', 'experience', 'health'
        operator = None
        value = None
        
        if condition_type == 'item':
            value = self.expect(TokenType.STRING).value
        else:
            operator = self.expect(TokenType.GT).value if self.current_token().type == TokenType.GT else None
            if not operator:
                operator = self.expect(TokenType.LT).value if self.current_token().type == TokenType.LT else None
            if not operator:
                operator = self.expect(TokenType.GTE).value if self.current_token().type == TokenType.GTE else None
            if not operator:
                operator = self.expect(TokenType.LTE).value if self.current_token().type == TokenType.LTE else None
            if not operator:
                operator = self.expect(TokenType.EQ).value if self.current_token().type == TokenType.EQ else None
            if not operator:
                operator = "=="  # Default
            value = self.expect(TokenType.NUMBER).value
        
        self.expect(TokenType.THEN)
        action_type = self.expect(TokenType.IDENTIFIER).value  # 'response' or 'context'
        action_value = self.expect(TokenType.STRING).value
        
        return NPCCondition(condition_type, operator, value, action_type, action_value)
    
    def parse_rules_section(self) -> RulesSection:
        self.expect(TokenType.RULES)
        self.expect(TokenType.COLON)
        
        rules = []
        while self.current_token().type == TokenType.IF:
            rules.append(self.parse_rule())
        
        return RulesSection(rules)
    
    def parse_rule(self) -> Rule:
        conditions = []
        action = None
        
        self.expect(TokenType.IF)
        conditions.append(self.parse_condition())
        
        while self.current_token().type == TokenType.AND:
            self.advance()
            conditions.append(self.parse_condition())
        
        self.expect(TokenType.THEN)
        action = self.parse_action()
        
        return Rule(conditions, action)
    
    def parse_condition(self) -> Condition:
        # Accept either USER token or IDENTIFIER for entity name
        if self.current_token().type == TokenType.USER:
            self.advance()
            entity = 'user'
        else:
            entity = self.expect(TokenType.IDENTIFIER).value
        
        # Check for "responded" or "responds" first (before other condition types)
        # This handles "wizard responded" where wizard is the entity
        if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value in ['responded', 'responds']:
            # "wizard responded" or "wizard responds" -> Condition('responded_to', 'wizard', None, None)
            self.advance()  # consume 'responded' or 'responds'
            npc_name = entity  # The entity is the NPC name
            return Condition('responded_to', npc_name, None, None)
        
        if self.current_token().type == TokenType.IS:
            self.advance()
            self.expect(TokenType.AT)
            position = self.parse_coordinate()
            return Condition('position', entity, None, None, position)
        elif self.current_token().type == TokenType.HAS:
            self.advance()
            # Could be: has item, has experience > 100, has health < 50
            if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value in ['item', 'experience', 'health']:
                attr = self.expect(TokenType.IDENTIFIER).value
                if attr == 'item':
                    value = self.expect(TokenType.STRING).value
                    return Condition('has', entity, None, value)
                else:
                    operator = None
                    if self.current_token().type in [TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE, TokenType.EQ, TokenType.NE]:
                        operator = self.current_token().value
                        self.advance()
                    else:
                        operator = "=="
                    value = self.expect(TokenType.NUMBER).value
                    return Condition('comparison', entity, operator, value)
            else:
                # Simple has check
                value = self.parse_value()
                return Condition('has', entity, None, value)
        elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'talked':
            # "user talked to wizard" -> Condition('talked_to', 'user', None, 'wizard')
            self.advance()  # consume 'talked'
            self.expect(TokenType.TO)
            npc_name = self.expect(TokenType.IDENTIFIER).value
            return Condition('talked_to', entity, None, npc_name)
        else:
            raise SyntaxError(f"Unexpected condition at line {self.current_token().line}")
    
    def parse_action(self) -> Action:
        token = self.current_token()
        
        if token.type == TokenType.IDENTIFIER and token.value.startswith('talk-'):
            action_type = self.expect(TokenType.IDENTIFIER).value
            return Action('talk', None, None, action_type)
        elif token.type == TokenType.LEVEL_UP:
            self.advance()
            return Action('level up', None, None, None)
        else:
            # Command
            command = self.expect(TokenType.IDENTIFIER).value
            return Action('command', command, None, None)
    
    def parse_quests_section(self) -> QuestsSection:
        self.expect(TokenType.QUESTS)
        self.expect(TokenType.COLON)
        
        quests = []
        # Support both named quests (name: if ...) and unnamed quests (if ...)
        while self.current_token().type in [TokenType.IF, TokenType.IDENTIFIER]:
            # Check if this is a named quest (identifier followed by colon)
            quest_name = None
            if self.current_token().type == TokenType.IDENTIFIER:
                # Peek ahead to see if next token is COLON
                if self.peek_token().type == TokenType.COLON:
                    quest_name = self.current_token().value
                    self.advance()  # consume the identifier
                    self.advance()  # consume the colon
            
            quests.append(self.parse_quest(quest_name))
        
        return QuestsSection(quests)
    
    def parse_quest(self, name: Optional[str] = None) -> Quest:
        conditions = []
        action = None
        
        self.expect(TokenType.IF)
        conditions.append(self.parse_condition())
        
        while self.current_token().type == TokenType.AND:
            self.advance()
            conditions.append(self.parse_condition())
        
        self.expect(TokenType.THEN)
        action = self.parse_action()
        
        return Quest(name, conditions, action)
    
    def parse_end_game_section(self) -> EndGameSection:
        self.expect(TokenType.END_GAME)
        self.expect(TokenType.COLON)
        
        conditions = []
        win_message = None
        lose_message = None
        
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.IF:
                self.advance()  # Consume 'if'
                # Parse condition(s) - can have multiple with "and"
                condition_list = []
                condition_list.append(self.parse_condition())
                while self.current_token().type == TokenType.AND:
                    self.advance()
                    condition_list.append(self.parse_condition())
                
                result = None
                if self.current_token().type == TokenType.THEN:
                    self.advance()
                    if self.current_token().type == TokenType.WIN:
                        self.advance()
                        self.expect(TokenType.THE)
                        self.expect(TokenType.IDENTIFIER)  # 'game'
                        result = 'win the game'
                    elif self.current_token().type == TokenType.DIE:
                        self.advance()
                        self.expect(TokenType.AND)
                        self.expect(TokenType.LOSE)
                        self.expect(TokenType.THE)
                        self.expect(TokenType.IDENTIFIER)  # 'game'
                        result = 'die and lose the game'
                
                # Store all conditions together as a single EndCondition with a compound condition
                # We'll use a special marker to indicate this is a grouped condition
                # Create a compound condition that represents all conditions together
                if len(condition_list) == 1:
                    conditions.append(EndCondition(condition_list[0], result))
                else:
                    # For multiple conditions, we need to store them as a group
                    # We'll create a special condition type that represents "all of these"
                    # For now, store them all with the same result - the JS will check all
                    for cond in condition_list:
                        conditions.append(EndCondition(cond, result))
            elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'win_the_game':
                self.advance()
                self.expect(TokenType.COLON)
                self.expect(TokenType.SHOW)
                win_message = self.expect(TokenType.STRING).value
            elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'lose_the_game':
                self.advance()
                self.expect(TokenType.COLON)
                self.expect(TokenType.SHOW)
                lose_message = self.expect(TokenType.STRING).value
            else:
                break
        
        return EndGameSection(conditions, win_message, lose_message)
    
    def parse_on_game_start_section(self) -> OnGameStartSection:
        self.expect(TokenType.ON_GAME_START)
        self.expect(TokenType.COLON)
        
        title = None
        text_lines = []
        links = []
        
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'display_title':
                self.advance()  # consume 'display_title'
                self.expect(TokenType.COLON)
                # Title can be a string or unquoted text (collect tokens until next command or EOF)
                if self.current_token().type == TokenType.STRING:
                    title = self.expect(TokenType.STRING).value
                else:
                    # Collect tokens until we hit the next display_ command or end of section
                    title_parts = []
                    while (self.current_token().type != TokenType.EOF and 
                           not (self.current_token().type == TokenType.IDENTIFIER and 
                                self.current_token().value.startswith('display_'))):
                        token = self.current_token()
                        if token.type == TokenType.IDENTIFIER or token.type == TokenType.STRING:
                            title_parts.append(token.value)
                        elif token.type in [TokenType.NUMBER, TokenType.BOOLEAN]:
                            title_parts.append(str(token.value))
                        else:
                            # Include punctuation and other characters as-is
                            title_parts.append(str(token.value) if token.value else '')
                        self.advance()
                    title = ' '.join(title_parts).strip()
                    if not title:
                        title = None
            elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'display_text':
                self.advance()  # consume 'display_text'
                self.expect(TokenType.COLON)
                # Text must be a string
                text_lines.append(self.expect(TokenType.STRING).value)
            elif self.current_token().type == TokenType.IDENTIFIER and self.current_token().value == 'display_link':
                self.advance()  # consume 'display_link'
                self.expect(TokenType.COLON)
                # display_link: "anchor", "url"
                anchor_text = self.expect(TokenType.STRING).value
                self.expect(TokenType.COMMA)
                url = self.expect(TokenType.STRING).value
                links.append((anchor_text, url))
            else:
                break
        
        return OnGameStartSection(title, text_lines, links)


class Validator:
    def __init__(self, program: Program):
        self.program = program
        self.errors = []
    
    def validate(self):
        if not self.program.init_section:
            self.errors.append("Missing required 'init:' section")
            return
        
        self.validate_uniqueness()
        self.validate_collisions()
        self.validate_semantics()
    
    def validate_uniqueness(self):
        unique_names = set()
        
        # Check mythics
        for mythic in self.program.init_section.mythics:
            if mythic.unique_name in unique_names:
                self.errors.append(f"Duplicate unique_name: {mythic.unique_name}")
            unique_names.add(mythic.unique_name)
        
        # Check items
        for item in self.program.init_section.items:
            if item.unique_name in unique_names:
                self.errors.append(f"Duplicate unique_name: {item.unique_name}")
            unique_names.add(item.unique_name)
        
        # Check monsters
        for monster in self.program.init_section.monsters:
            if monster.unique_name in unique_names:
                self.errors.append(f"Duplicate unique_name: {monster.unique_name}")
            unique_names.add(monster.unique_name)
        
        # Check NPCs
        for npc in self.program.init_section.npcs:
            if npc.unique_name in unique_names:
                self.errors.append(f"Duplicate unique_name: {npc.unique_name}")
            unique_names.add(npc.unique_name)
        
        # Check user
        if self.program.init_section.user:
            if self.program.init_section.user.unique_name in unique_names:
                self.errors.append(f"Duplicate unique_name: {self.program.init_section.user.unique_name}")
    
    def validate_collisions(self):
        # Track entity positions
        entity_positions = {}  # (x, y) -> list of entity names
        
        # Check fixed placements (not random)
        for mythic in self.program.init_section.mythics:
            if mythic.placement and mythic.placement.type == 'coordinate':
                pos = mythic.placement.coord1
                if pos not in entity_positions:
                    entity_positions[pos] = []
                entity_positions[pos].append(f"mythic:{mythic.unique_name}")
        
        for item in self.program.init_section.items:
            if item.placement and item.placement.type == 'coordinate':
                pos = item.placement.coord1
                if pos not in entity_positions:
                    entity_positions[pos] = []
                entity_positions[pos].append(f"item:{item.unique_name}")
        
        for monster in self.program.init_section.monsters:
            if monster.placement and monster.placement.type == 'coordinate':
                pos = monster.placement.coord1
                if pos not in entity_positions:
                    entity_positions[pos] = []
                entity_positions[pos].append(f"monster:{monster.unique_name}")
        
        for npc in self.program.init_section.npcs:
            if npc.placement and npc.placement.type == 'coordinate':
                pos = npc.placement.coord1
                if pos not in entity_positions:
                    entity_positions[pos] = []
                entity_positions[pos].append(f"npc:{npc.unique_name}")
        
        # Check for collisions (items, monsters, NPCs shouldn't overlap)
        for pos, entities in entity_positions.items():
            if len(entities) > 1:
                # Allow items/mythics on same cell, but warn about monsters/NPCs
                non_pickup = [e for e in entities if not e.startswith('item:') and not e.startswith('mythic:')]
                if len(non_pickup) > 1:
                    self.errors.append(f"Collision at {pos}: {', '.join(entities)}")
    
    def validate_semantics(self):
        # Basic semantic checks
        if self.program.init_section.user and not self.program.init_section.user.position:
            self.errors.append("User must have an initial position")
        
        # Check that npc-static NPCs have placement
        for npc in self.program.init_section.npcs:
            if npc.npc_type == 'npc-static' and not npc.placement:
                self.errors.append(f"npc-static '{npc.unique_name}' must have a placement specified")
        
        # Check that rules reference valid entities
        if self.program.rules_section:
            for rule in self.program.rules_section.rules:
                for condition in rule.conditions:
                    if condition.entity != 'user':
                        # Check if entity exists
                        found = False
                        for mythic in self.program.init_section.mythics:
                            if mythic.unique_name == condition.entity:
                                found = True
                                break
                        if not found:
                            for item in self.program.init_section.items:
                                if item.unique_name == condition.entity:
                                    found = True
                                    break
                        if not found:
                            for monster in self.program.init_section.monsters:
                                if monster.unique_name == condition.entity:
                                    found = True
                                    break
                        if not found:
                            for npc in self.program.init_section.npcs:
                                if npc.unique_name == condition.entity:
                                    found = True
                                    break
                        if not found:
                            self.errors.append(f"Unknown entity referenced in rule: {condition.entity}")


class CodeGenerator:
    def __init__(self, program: Program):
        self.program = program
    
    def generate(self) -> str:
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dungeon Game</title>
    <style>
        {self.generate_css()}
    </style>
</head>
<body>
    {self.generate_html()}
    <script>
        {self.generate_javascript()}
    </script>
</body>
</html>"""
        return html
    
    def generate_css(self) -> str:
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: #1a1a1a;
            color: #fff;
            overflow: hidden;
        }
        
        #menu-bar {
            background: #2a2a2a;
            padding: 10px;
            display: flex;
            gap: 10px;
            border-bottom: 2px solid #444;
        }
        
        .menu-button {
            background: #444;
            color: #fff;
            border: 1px solid #666;
            padding: 8px 16px;
            cursor: pointer;
            border-radius: 4px;
        }
        
        .menu-button:hover {
            background: #555;
        }
        
        .dropdown {
            position: relative;
            display: inline-block;
        }
        
        .dropdown-content {
            display: none;
            position: absolute;
            background: #333;
            min-width: 200px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            z-index: 1000;
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #555;
            border-radius: 4px;
            top: 100%;
            left: 0;
            margin-top: 5px;
        }
        
        .dropdown-content.show {
            display: block;
        }
        
        .dropdown-content div {
            padding: 10px;
            border-bottom: 1px solid #444;
        }
        
        #game-container {
            position: relative;
            width: 100vw;
            height: calc(100vh - 50px);
            overflow: hidden;
        }
        
        #game-canvas {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            image-rendering: pixelated;
        }
        
        #dialog-panel {
            position: fixed;
            right: -400px;
            top: 60px;
            width: 350px;
            height: calc(100vh - 60px);
            background: #2a2a2a;
            border-left: 2px solid #444;
            transition: right 0.3s;
            padding: 20px;
            overflow-y: auto;
        }
        
        #dialog-panel.show {
            right: 0;
        }
        
        #dialog-content {
            margin-bottom: 20px;
        }
        
        #dialog-input {
            width: 100%;
            padding: 10px;
            background: #333;
            color: #fff;
            border: 1px solid #555;
            border-radius: 4px;
        }
        
        #dialog-close {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #444;
            color: #fff;
            border: 1px solid #666;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 16px;
            z-index: 10;
        }
        
        #dialog-close:hover {
            background: #555;
        }
        
        .interaction-text {
            position: absolute;
            background: rgba(0,0,0,0.8);
            color: #fff;
            padding: 5px 10px;
            border-radius: 4px;
            pointer-events: none;
            z-index: 100;
            font-size: 12px;
        }
        
        .popup-text {
            position: absolute;
            background: rgba(255,255,0,0.9);
            color: #000;
            padding: 5px 10px;
            border-radius: 4px;
            pointer-events: none;
            z-index: 101;
            font-size: 12px;
            animation: fadeOut 3s forwards;
        }
        
        @keyframes fadeOut {
            0% { opacity: 1; }
            70% { opacity: 1; }
            100% { opacity: 0; }
        }
        
        #splash-screen {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        #splash-screen.show {
            display: flex;
        }
        
        #splash-content {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            max-width: 600px;
            width: 90%;
            text-align: center;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        #splash-title {
            font-size: 2.5em;
            margin: 0 0 20px 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            color: #ffd700;
        }
        
        #splash-text {
            font-size: 1.2em;
            line-height: 1.8;
            margin: 20px 0;
            color: #ffffff;
        }
        
        #splash-text p {
            margin: 10px 0;
        }
        
        #splash-close {
            margin-top: 30px;
            padding: 15px 40px;
            font-size: 1.2em;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        #splash-close:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
        }
        
        #splash-close:active {
            transform: translateY(0);
        }
        """
    
    def generate_html(self) -> str:
        return """
    <div id="menu-bar">
        <button class="menu-button" onclick="game.saveGame()">Save</button>
        <button class="menu-button" onclick="document.getElementById('load-input').click()">
            Load
            <input type="file" id="load-input" accept=".json" style="display:none" onchange="game.loadGame(event)">
        </button>
        <div class="dropdown">
            <button class="menu-button" onclick="toggleDropdown('status-dropdown')">Status</button>
            <div id="status-dropdown" class="dropdown-content">
                <div id="status-content"></div>
            </div>
        </div>
        <div class="dropdown">
            <button class="menu-button" onclick="toggleDropdown('inventory-dropdown')">Inventory</button>
            <div id="inventory-dropdown" class="dropdown-content">
                <div id="inventory-content"></div>
            </div>
        </div>
        <div class="dropdown">
            <button class="menu-button" onclick="toggleDropdown('chat-dropdown')">Chat History</button>
            <div id="chat-dropdown" class="dropdown-content">
                <div id="chat-content"></div>
            </div>
        </div>
        <div class="dropdown">
            <button class="menu-button" onclick="toggleDropdown('quest-dropdown')">Quest-Status</button>
            <div id="quest-dropdown" class="dropdown-content">
                <div id="quest-content"></div>
            </div>
        </div>
    </div>
    <div id="game-container">
        <canvas id="game-canvas"></canvas>
    </div>
    <div id="dialog-panel">
        <button id="dialog-close" onclick="game.closeDialog()">× Close</button>
        <div id="dialog-content"></div>
        <input type="text" id="dialog-input" placeholder="Type message..." style="display:none" onkeypress="handleDialogInput(event)">
    </div>
    <div id="splash-screen">
        <div id="splash-content">
            <h1 id="splash-title"></h1>
            <div id="splash-text"></div>
            <button id="splash-close" onclick="game.closeSplashScreen()">Start Game</button>
        </div>
    </div>
    <script>
        function toggleDropdown(id) {
            const dropdown = document.getElementById(id);
            dropdown.classList.toggle('show');
        }
        
        function handleDialogInput(event) {
            if (event.key === 'Enter') {
                const input = document.getElementById('dialog-input');
                const message = input.value;
                if (message.trim()) {
                    game.handleDialogInput(message);
                    input.value = '';
                }
            }
        }
        
        // Close dropdowns when clicking outside
        window.onclick = function(event) {
            if (!event.target.matches('.menu-button')) {
                const dropdowns = document.getElementsByClassName('dropdown-content');
                for (let dropdown of dropdowns) {
                    if (dropdown.classList.contains('show')) {
                        dropdown.classList.remove('show');
                    }
                }
            }
        }
    </script>
        """
    
    def generate_javascript(self) -> str:
        js_parts = []
        
        # Game state initialization
        js_parts.append(self.generate_game_state())
        
        # Game engine
        js_parts.append(self.generate_game_engine())
        
        return "\n".join(js_parts)
    
    def generate_game_state(self) -> str:
        init = self.program.init_section
        world = init.world or WorldDecl(100, 100)
        
        state = {
            'world': {
                'width': world.width,
                'height': world.height
            },
            'user': {
                'unique_name': init.user.unique_name if init.user else 'player',
                'position': list(init.user.position) if init.user and init.user.position else [50, 50],
                'health': 100,
                'experience': 0,
                'level': 1,
                'inventory': [],
                'context': init.user.context if init.user else None,
                'talked_to_npcs': [],
                'showHealthBar': False
            },
            'terrain': {},
            'furniture': [],
            'mythics': [],
            'items': [],
            'monsters': [],
            'npcs': [],
            'variables': {},
            'quests': [],
            'rules': [],
            'end_game': {},
            'on_game_start': {}
        }
        
        # Add furniture
        for furniture in init.furniture:
            state['furniture'].append({
                'name': furniture.name,
                'placement': self.placement_to_dict(furniture.placement)
            })
        
        # Add mythics
        for mythic in init.mythics:
            mythic_data = {
                'unique_name': mythic.unique_name,
                'can_pickup': mythic.can_pickup,
                'picked_up': False,
                'catch_message': mythic.catch_message or "Not now"
            }
            if mythic.placement:
                if mythic.placement.type == 'coordinate':
                    mythic_data['position'] = list(mythic.placement.coord1)
                elif mythic.placement.type == 'random':
                    # Will be placed randomly during initialization
                    mythic_data['placement'] = {'type': 'random', 'percentage': getattr(mythic.placement, 'percentage', 50)}
            state['mythics'].append(mythic_data)
        
        # Add items
        for item in init.items:
            item_data = {
                'unique_name': item.unique_name,
                'item_type': item.item_type,
                'can_pickup': item.can_pickup,
                'picked_up': False,
                'effect': item.effect,
                'damage': item.damage or 1,
                'catch_message': item.catch_message or "Not now"
            }
            if item.placement:
                if item.placement.type == 'coordinate':
                    item_data['position'] = list(item.placement.coord1)
                elif item.placement.type == 'random':
                    item_data['placement'] = {'type': 'random', 'percentage': getattr(item.placement, 'percentage', 50)}
            state['items'].append(item_data)
        
        # Add monsters
        for monster in init.monsters:
            monster_data = {
                'unique_name': monster.unique_name,
                'monster_type': monster.monster_type,
                'health': monster.health or monster.killable_hits or 1,
                'max_health': monster.health or monster.killable_hits or 1,
                'experience': monster.experience or 0,
                'defeated': False
            }
            if monster.placement:
                if monster.placement.type == 'coordinate':
                    monster_data['position'] = list(monster.placement.coord1)
                elif monster.placement.type == 'random':
                    monster_data['placement'] = {'type': 'random', 'percentage': getattr(monster.placement, 'percentage', 50)}
            state['monsters'].append(monster_data)
        
        # Add NPCs
        for npc in init.npcs:
            npc_data = {
                'unique_name': npc.unique_name,
                'npc_type': npc.npc_type,
                'context': npc.context,
                'response': npc.response,
                'state_machine': npc.state_machine or 'idle',
                'emoji': npc.emoji or '👤',
                'agenda': npc.agenda,
                'conditions': [self.npc_condition_to_dict(c) for c in npc.conditions],
                'catch_message': npc.catch_message or "Not now",
                'conversation_history': [],
                'has_responded': False
            }
            # Set NPC position from placement
            if npc.placement:
                if npc.placement.type == 'coordinate':
                    npc_data['position'] = list(npc.placement.coord1)
                elif npc.placement.type == 'random':
                    # Random placement will be handled during initialization
                    npc_data['placement'] = {'type': 'random', 'percentage': getattr(npc.placement, 'percentage', 50)}
            else:
                # Only allow no placement for non-static NPCs (dynamic NPCs might be placed later)
                if npc.npc_type == 'npc-static':
                    npc_data['position'] = [10, 10]  # Fallback, but validator should catch this
            state['npcs'].append(npc_data)
        
        # Add variables
        for var in self.program.variables:
            state['variables'][var.name] = var.value
        
        # Add quests
        if self.program.quests_section:
            for i, quest in enumerate(self.program.quests_section.quests):
                # Use quest name if provided, otherwise use quest_{i}
                quest_id = quest.name if quest.name else f'quest_{i}'
                state['quests'].append({
                    'id': quest_id,
                    'conditions': [self.condition_to_dict(c) for c in quest.conditions],
                    'action': self.action_to_dict(quest.action),
                    'status': 'active',
                    'completed': False
                })
        
        # Add rules
        if self.program.rules_section:
            for i, rule in enumerate(self.program.rules_section.rules):
                state['rules'].append({
                    'id': f'rule_{i}',
                    'conditions': [self.condition_to_dict(c) for c in rule.conditions],
                    'action': self.action_to_dict(rule.action),
                    'triggered': False
                })
        
        # Add end game
        if self.program.end_game_section:
            state['end_game'] = {
                'conditions': [self.end_condition_to_dict(ec) for ec in self.program.end_game_section.conditions],
                'win_message': self.program.end_game_section.win_message,
                'lose_message': self.program.end_game_section.lose_message
            }
        
        # Add on game start (splash screen)
        if self.program.on_game_start_section:
            state['on_game_start'] = {
                'title': self.program.on_game_start_section.title,
                'text_lines': self.program.on_game_start_section.text_lines,
                'links': [list(link) for link in self.program.on_game_start_section.links]  # Convert tuples to lists for JSON
            }
        
        return f"const INITIAL_GAME_STATE = {json.dumps(state, indent=2)};"
    
    def placement_to_dict(self, placement: Placement) -> dict:
        if placement.type == 'all':
            return {'type': 'all'}
        elif placement.type == 'coordinate':
            return {'type': 'coordinate', 'coord': list(placement.coord1)}
        elif placement.type == 'range':
            return {'type': 'range', 'coord1': list(placement.coord1), 'coord2': list(placement.coord2)}
        elif placement.type == 'random':
            percentage = placement.percentage if placement.percentage is not None else 50
            return {'type': 'random', 'percentage': percentage}
        return {}
    
    def condition_to_dict(self, condition: Condition) -> dict:
        result = {
            'type': condition.type,
            'entity': condition.entity
        }
        if condition.position:
            result['position'] = list(condition.position)
        if condition.operator:
            result['operator'] = condition.operator
        if condition.value is not None:
            result['value'] = condition.value
        return result
    
    def action_to_dict(self, action: Action) -> dict:
        return {
            'type': action.type,
            'command': action.command,
            'target': action.target,
            'value': action.value
        }
    
    def npc_condition_to_dict(self, condition: NPCCondition) -> dict:
        return {
            'condition_type': condition.condition_type,
            'operator': condition.operator,
            'value': condition.value,
            'then_action': condition.then_action,
            'action_value': condition.action_value
        }
    
    def end_condition_to_dict(self, end_condition: EndCondition) -> dict:
        return {
            'condition': self.condition_to_dict(end_condition.condition),
            'result': end_condition.result
        }
    
    def generate_game_engine(self) -> str:
        # This is a large JavaScript file - I'll generate the core game engine
        # Due to length, I'll create a comprehensive but focused engine
        init = self.program.init_section
        llm_endpoint = json.dumps(init.llm_endpoint) if init and init.llm_endpoint else 'null'
        llm_token = json.dumps(init.llm_token) if init and init.llm_token else 'null'
        engine_code = """
        // Game Engine
        class DungeonGame {
            constructor() {
                this.state = JSON.parse(JSON.stringify(INITIAL_GAME_STATE));
                this.canvas = document.getElementById('game-canvas');
                this.ctx = this.canvas.getContext('2d');
                this.cellSize = 40;
                this.zoom = 1.0;
                this.viewportX = 0;
                this.viewportY = 0;
                this.panning = false;
                this.currentDialogNPC = null;
                this.interactionTexts = [];
                this.popupTexts = [];
                this.llmEndpoint = LLM_ENDPOINT_PLACEHOLDER;
                this.llmToken = LLM_TOKEN_PLACEHOLDER;
                this.npcInteractionHistory = {};
                this.lastDialogOpenTime = 0;
                
                this.init();
                this.setupEventListeners();
                this.gameLoop();
            }
            
            init() {
                this.resizeCanvas();
                this.placeRandomEntities();
                this.centerOnUser();  // Center viewport on user at game start
                this.updateUI();
                this.showSplashScreen();
            }
            
            resizeCanvas() {
                const container = document.getElementById('game-container');
                this.canvas.width = container.clientWidth;
                this.canvas.height = container.clientHeight;
            }
            
            placeRandomEntities() {
                // Place random mythics
                for (let mythic of this.state.mythics) {
                    if (mythic.placement && mythic.placement.type === 'random') {
                        if (Math.random() * 100 < mythic.placement.percentage) {
                            mythic.position = [
                                Math.floor(Math.random() * this.state.world.width),
                                Math.floor(Math.random() * this.state.world.height)
                            ];
                        }
                    }
                }
                
                // Place random items
                for (let item of this.state.items) {
                    if (item.placement && item.placement.type === 'random') {
                        if (Math.random() * 100 < item.placement.percentage) {
                            item.position = [
                                Math.floor(Math.random() * this.state.world.width),
                                Math.floor(Math.random() * this.state.world.height)
                            ];
                        }
                    }
                }
                
                // Place random monsters
                for (let monster of this.state.monsters) {
                    if (monster.placement && monster.placement.type === 'random') {
                        if (Math.random() * 100 < monster.placement.percentage) {
                            monster.position = [
                                Math.floor(Math.random() * this.state.world.width),
                                Math.floor(Math.random() * this.state.world.height)
                            ];
                        }
                    }
                }
            }
            
            setupEventListeners() {
                // Movement
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'ArrowUp' && !e.shiftKey) {
                        this.moveUser(0, -1);
                    } else if (e.key === 'ArrowDown' && !e.shiftKey) {
                        this.moveUser(0, 1);
                    } else if (e.key === 'ArrowLeft' && !e.shiftKey) {
                        this.moveUser(-1, 0);
                    } else if (e.key === 'ArrowRight' && !e.shiftKey) {
                        this.moveUser(1, 0);
                    } else if (e.key === 'Enter' || e.key === ' ') {
                        this.handleEnterKey();
                    } else if (e.key === 'Escape') {
                        this.closeDialog();
                    } else if (e.key === '+' || e.key === '=') {
                        this.zoomIn();
                    } else if (e.key === '-') {
                        this.zoomOut();
                    }
                });
                
                // Panning
                let shiftPressed = false;
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Shift') shiftPressed = true;
                    if (shiftPressed && e.key.startsWith('Arrow')) {
                        this.panning = true;
                        if (e.key === 'ArrowUp') this.viewportY -= 5;
                        if (e.key === 'ArrowDown') this.viewportY += 5;
                        if (e.key === 'ArrowLeft') this.viewportX -= 5;
                        if (e.key === 'ArrowRight') this.viewportX += 5;
                    }
                });
                document.addEventListener('keyup', (e) => {
                    if (e.key === 'Shift') {
                        shiftPressed = false;
                        this.panning = false;
                        this.centerOnUser();
                    }
                });
            }
            
            moveUser(dx, dy) {
                const newX = this.state.user.position[0] + dx;
                const newY = this.state.user.position[1] + dy;
                
                // Check boundaries (allow 0 to width-1 and 0 to height-1)
                if (newX < 0 || newX >= this.state.world.width ||
                    newY < 0 || newY >= this.state.world.height) {
                    return;
                }
                
                // Check collisions
                if (!this.canMoveTo(newX, newY)) {
                    return;
                }
                
                this.state.user.position[0] = newX;
                this.state.user.position[1] = newY;
                
                // Check for item/mythic pickup
                this.checkPickups();
                
                // Check for interactions
                this.checkInteractions();
                
                // Update viewport
                if (!this.panning) {
                    this.centerOnUser();
                }
                
                // Evaluate rules and quests
                this.evaluateRules();
                this.evaluateQuests();
                this.checkEndGame();
                
                this.updateUI();
            }
            
            canMoveTo(x, y) {
                // Check furniture (walls, stone are impassible)
                for (let furniture of this.state.furniture) {
                    if (furniture.placement.type === 'coordinate') {
                        const pos = furniture.placement.coord;
                        if (pos[0] === x && pos[1] === y) {
                            // Check if furniture blocks movement (walls, stone do)
                            if (furniture.name === 'wall' || furniture.name === 'stone') {
                                return false;
                            }
                        }
                    } else if (furniture.placement.type === 'range') {
                        const coord1 = furniture.placement.coord1;
                        const coord2 = furniture.placement.coord2;
                        const minX = Math.min(coord1[0], coord2[0]);
                        const maxX = Math.max(coord1[0], coord2[0]);
                        const minY = Math.min(coord1[1], coord2[1]);
                        const maxY = Math.max(coord1[1], coord2[1]);
                        if (x >= minX && x <= maxX && y >= minY && y <= maxY) {
                            // Check if furniture blocks movement (walls, stone do)
                            if (furniture.name === 'wall' || furniture.name === 'stone') {
                                return false;
                            }
                        }
                    }
                }
                
                // Check NPCs
                for (let npc of this.state.npcs) {
                    if (npc.position && npc.position[0] === x && npc.position[1] === y) {
                        return false; // Can't walk through NPCs
                    }
                }
                
                // Check monsters
                for (let monster of this.state.monsters) {
                    if (!monster.defeated && monster.position && 
                        monster.position[0] === x && monster.position[1] === y) {
                        return false; // Can't walk through monsters
                    }
                }
                
                return true;
            }
            
            checkPickups() {
                const userPos = this.state.user.position;
                let pickedUpSomething = false;
                
                // Check mythics
                for (let mythic of this.state.mythics) {
                    if (!mythic.picked_up && mythic.position &&
                        mythic.position[0] === userPos[0] && mythic.position[1] === userPos[1]) {
                        if (mythic.can_pickup) {
                            this.state.user.inventory.push(mythic.unique_name);
                            mythic.picked_up = true;
                            pickedUpSomething = true;
                            this.showInteractionText(userPos[0], userPos[1], `Picked up ${mythic.unique_name}`);
                        } else {
                            this.showInteractionText(userPos[0], userPos[1], mythic.catch_message);
                        }
                    }
                }
                
                // Check items
                for (let item of this.state.items) {
                    if (!item.picked_up && item.position &&
                        item.position[0] === userPos[0] && item.position[1] === userPos[1]) {
                        if (item.can_pickup) {
                            this.state.user.inventory.push(item.unique_name);
                            item.picked_up = true;
                            pickedUpSomething = true;
                            
                            // Heal 25% if it's a healing item
                            if (item.item_type === 'item-heal') {
                                const maxHealth = 100;
                                const healAmount = Math.floor(maxHealth * 0.25); // 25% of max health
                                const oldHealth = this.state.user.health;
                                this.state.user.health = Math.min(maxHealth, this.state.user.health + healAmount);
                                const actualHeal = this.state.user.health - oldHealth;
                                
                                if (actualHeal > 0) {
                                    this.showInteractionText(userPos[0], userPos[1], `Picked up ${item.unique_name}! Healed ${actualHeal} health!`);
                                } else {
                                    this.showInteractionText(userPos[0], userPos[1], `Picked up ${item.unique_name}! (Already at full health)`);
                                }
                            } else {
                                this.showInteractionText(userPos[0], userPos[1], `Picked up ${item.unique_name}`);
                            }
                        } else {
                            this.showInteractionText(userPos[0], userPos[1], item.catch_message);
                        }
                    }
                }
                
                // If we picked something up, check end game conditions
                if (pickedUpSomething) {
                    this.checkEndGame();
                }
            }
            
            checkInteractions() {
                const userPos = this.state.user.position;
                
                // Check NPCs at same position
                for (let npc of this.state.npcs) {
                    if (npc.position && npc.position[0] === userPos[0] && npc.position[1] === userPos[1]) {
                        // Auto-trigger interaction based on rules
                        // For now, just mark as available for interaction
                    }
                }
            }
            
            handleEnterKey() {
                const userPos = this.state.user.position;
                
                // Check for monsters at same position or adjacent (combat)
                for (let monster of this.state.monsters) {
                    if (!monster.defeated && monster.position) {
                        const dx = Math.abs(monster.position[0] - userPos[0]);
                        const dy = Math.abs(monster.position[1] - userPos[1]);
                        // Attack if on same cell or adjacent (distance <= 1)
                        if (dx <= 1 && dy <= 1 && (dx + dy) <= 1) {
                            this.attackMonster(monster);
                            return;
                        }
                    }
                }
                
                // Check for NPCs at same position or adjacent
                // Don't interact if dialog is already open
                const panel = document.getElementById('dialog-panel');
                if (panel && panel.classList.contains('show')) {
                    return; // Dialog already open, don't trigger new interaction
                }
                
                for (let npc of this.state.npcs) {
                    if (npc.position) {
                        const dx = Math.abs(npc.position[0] - userPos[0]);
                        const dy = Math.abs(npc.position[1] - userPos[1]);
                        // Interact if on same cell or adjacent (distance <= 1)
                        if (dx <= 1 && dy <= 1 && (dx + dy) <= 1) {
                            this.interactWithNPC(npc);
                            return;
                        }
                    }
                }
            }
            
            attackMonster(monster) {
                // Default punch attack does 1 damage
                let damage = 1;
                let weaponUsed = 'punch';
                
                // Check if user has items that can be used as weapons
                // For now, use default punch attack
                // TODO: Support "attack <monster> with <item>" command
                
                // Show health bars for combat
                monster.showHealthBar = true;
                this.state.user.showHealthBar = true;
                
                // Set timeout to hide health bars after 3 seconds
                if (monster.healthBarTimeout) {
                    clearTimeout(monster.healthBarTimeout);
                }
                if (this.state.user.healthBarTimeout) {
                    clearTimeout(this.state.user.healthBarTimeout);
                }
                monster.healthBarTimeout = setTimeout(() => {
                    monster.showHealthBar = false;
                }, 3000);
                this.state.user.healthBarTimeout = setTimeout(() => {
                    this.state.user.showHealthBar = false;
                }, 3000);
                
                // Apply damage
                monster.health -= damage;
                
                // Check if monster is defeated
                if (monster.health <= 0) {
                    monster.defeated = true;
                    const expGained = monster.experience || 0;
                    this.state.user.experience += expGained;
                    
                    this.showInteractionText(
                        monster.position[0],
                        monster.position[1],
                        `You defeated ${monster.unique_name}! Gained ${expGained} experience!`
                    );
                    
                    // Remove monster from blocking position
                    monster.position = null;
                    monster.showHealthBar = false;
                    if (monster.healthBarTimeout) {
                        clearTimeout(monster.healthBarTimeout);
                    }
                } else {
                    // Monster counter-attacks (2 damage for boss, 1 for others)
                    const counterDamage = monster.monster_type === 'monster-boss' ? 2 : 1;
                    this.state.user.health -= counterDamage;
                    
                    // Check if user is defeated
                    if (this.state.user.health <= 0) {
                        this.checkEndGame(); // This will trigger lose condition if health <= 0
                    }
                }
                
                this.updateUI();
                this.checkEndGame();
            }
            
            interactWithNPC(npc) {
                const panel = document.getElementById('dialog-panel');
                
                // If dialog is already open for this NPC, don't reopen it
                if (this.currentDialogNPC && this.currentDialogNPC.unique_name === npc.unique_name && panel.classList.contains('show')) {
                    return;
                }
                
                // Track that user talked to this NPC
                if (!this.state.user.talked_to_npcs.includes(npc.unique_name)) {
                    this.state.user.talked_to_npcs.push(npc.unique_name);
                    // Evaluate quests after talking to NPC (in case a quest requires talking to NPC)
                    this.evaluateQuests();
                }
                
                this.currentDialogNPC = npc;
                panel.classList.add('show');
                this.lastDialogOpenTime = Date.now();
                
                if (npc.npc_type === 'npc-static') {
                    this.showStaticNPCDialog(npc);
                } else if (npc.npc_type === 'npc-dynamic') {
                    this.showDynamicNPCDialog(npc);
                } else if (npc.npc_type === 'npc-state-machine') {
                    this.showStateMachineNPCDialog(npc);
                }
            }
            
            showStaticNPCDialog(npc) {
                const content = document.getElementById('dialog-content');
                const input = document.getElementById('dialog-input');
                input.style.display = 'none';
                
                // Check conditions
                let response = npc.response;
                for (let condition of npc.conditions) {
                    if (this.checkNPCCondition(condition)) {
                        if (condition.then_action === 'response') {
                            response = condition.action_value;
                            break;
                        }
                    }
                }
                
                // If response contains "|", randomly select one phrase
                if (response && response.includes('|')) {
                    const phrases = response.split('|').map(p => p.trim()).filter(p => p.length > 0);
                    if (phrases.length > 0) {
                        response = phrases[Math.floor(Math.random() * phrases.length)];
                    }
                }
                
                content.innerHTML = `<h3>${npc.unique_name}</h3><p>${response}</p>`;
            }
            
            showDynamicNPCDialog(npc) {
                const content = document.getElementById('dialog-content');
                const input = document.getElementById('dialog-input');
                input.style.display = 'block';
                input.focus();
                
                if (!this.npcInteractionHistory[npc.unique_name]) {
                    this.npcInteractionHistory[npc.unique_name] = [];
                }
                
                let contextText = npc.context || '';
                if (npc.agenda) {
                    contextText += '\\nAgenda: ' + npc.agenda;
                }
                
                // Show static response as initial message if available
                let initialMessage = '';
                if (npc.response) {
                    initialMessage = `<p><strong>${npc.unique_name}:</strong> ${npc.response}</p>`;
                }
                
                content.innerHTML = `<h3>${npc.unique_name}</h3><div id="conversation">${initialMessage}</div>`;
            }
            
            showStateMachineNPCDialog(npc) {
                const content = document.getElementById('dialog-content');
                const input = document.getElementById('dialog-input');
                input.style.display = 'none';
                
                // Simple state machine - use state to determine response
                let response = npc.response || 'Hello!';
                if (npc.state_machine === 'idle') {
                    response = 'I am idle.';
                }
                
                content.innerHTML = `<h3>${npc.unique_name}</h3><p>${response}</p>`;
            }
            
            handleDialogInput(message) {
                if (!this.currentDialogNPC || this.currentDialogNPC.npc_type !== 'npc-dynamic') {
                    return;
                }
                
                const npc = this.currentDialogNPC;
                const conversationDiv = document.getElementById('conversation');
                
                // Add user message
                conversationDiv.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
                
                // Send to LLM (if configured)
                if (this.llmEndpoint && this.llmToken) {
                    this.sendToLLM(npc, message, conversationDiv);
                } else {
                    // Use static response as fallback if available
                    let fallbackResponse = npc.response || "I'm having trouble thinking right now. Can we talk later?";
                    conversationDiv.innerHTML += `<p><strong>${npc.unique_name}:</strong> ${fallbackResponse}</p>`;
                    // Mark that NPC has responded (even if LLM not configured)
                    npc.has_responded = true;
                    // Evaluate quests and check end game after NPC responds
                    this.evaluateQuests();
                    this.checkEndGame();
                }
            }
            
            async sendToLLM(npc, message, conversationDiv) {
                try {
                    const history = this.npcInteractionHistory[npc.unique_name] || [];
                    history.push({role: 'user', content: message});
                    
                    // Check if endpoint is localhost and we're running from file://
                    const isLocalhost = this.llmEndpoint && (this.llmEndpoint.includes('localhost') || this.llmEndpoint.includes('127.0.0.1'));
                    const isFileProtocol = window.location.protocol === 'file:';
                    
                    if (isLocalhost && isFileProtocol) {
                        // Use static response as fallback if available
                        if (npc.response) {
                            conversationDiv.innerHTML += `<p><strong>${npc.unique_name}:</strong> ${npc.response}</p>`;
                            npc.has_responded = true;
                            this.evaluateQuests();
                            this.checkEndGame();
                        } else {
                            conversationDiv.innerHTML += `<p><strong>${npc.unique_name}:</strong> <em>Note: To use localhost LLM, please serve this HTML file from a local web server (e.g., python -m http.server) instead of opening it directly. CORS policy blocks file:// requests to localhost.</em></p>`;
                        }
                        return;
                    }
                    
                    const fetchOptions = {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${this.llmToken}`
                        },
                        body: JSON.stringify({
                            messages: [
                                {role: 'system', content: npc.context || '' + (npc.agenda ? '\\nAgenda: ' + npc.agenda : '')},
                                ...history.slice(-10) // Last 10 messages
                            ]
                        })
                    };
                    
                    // For localhost endpoints, explicitly set mode
                    if (isLocalhost) {
                        fetchOptions.mode = 'cors';
                    }
                    
                    const response = await fetch(this.llmEndpoint, fetchOptions);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    const llmResponse = data.choices?.[0]?.message?.content || "I'm having trouble thinking right now.";
                    
                    history.push({role: 'assistant', content: llmResponse});
                    conversationDiv.innerHTML += `<p><strong>${npc.unique_name}:</strong> ${llmResponse}</p>`;
                    
                    // Mark that NPC has responded
                    npc.has_responded = true;
                    // Evaluate quests and check end game after NPC responds
                    this.evaluateQuests();
                    this.checkEndGame();
                } catch (error) {
                    console.error('LLM request error:', error);
                    
                    // Use static response as fallback if available
                    if (npc.response) {
                        conversationDiv.innerHTML += `<p><strong>${npc.unique_name}:</strong> ${npc.response}</p>`;
                        npc.has_responded = true;
                        this.evaluateQuests();
                        this.checkEndGame();
                        return;
                    }
                    
                    // Otherwise show error message
                    let errorMsg = "I'm having trouble thinking right now. Can we talk later?";
                    
                    const errorStr = error.toString();
                    if (errorStr.includes('CORS') || errorStr.includes('preflight')) {
                        errorMsg = `CORS Error: The LLM server at ${this.llmEndpoint} needs to allow CORS from ${window.location.origin}. The server must respond to OPTIONS requests with these headers: Access-Control-Allow-Origin: ${window.location.origin}, Access-Control-Allow-Methods: POST, Access-Control-Allow-Headers: Content-Type, Authorization. Please configure your LLM server to allow CORS.`;
                    } else if (errorStr.includes('Failed to fetch') || errorStr.includes('ERR_FAILED')) {
                        errorMsg = `Connection Error: Could not connect to LLM server at ${this.llmEndpoint}. Please ensure: 1) The server is running, 2) The URL is correct, 3) The server allows CORS from ${window.location.origin}`;
                    } else if (error.message) {
                        errorMsg = `Error: ${error.message}`;
                    }
                    
                    conversationDiv.innerHTML += `<p><strong>${npc.unique_name}:</strong> <em style="color: #ff6b6b;">${errorMsg}</em></p>`;
                    
                    // Mark that NPC has responded (even on error)
                    npc.has_responded = true;
                    // Evaluate quests and check end game after NPC responds
                    this.evaluateQuests();
                    this.checkEndGame();
                }
            }
            
            checkNPCCondition(condition) {
                if (condition.condition_type === 'item') {
                    return this.state.user.inventory.includes(condition.value);
                } else if (condition.condition_type === 'experience') {
                    return this.compareValues(this.state.user.experience, condition.operator, condition.value);
                } else if (condition.condition_type === 'health') {
                    return this.compareValues(this.state.user.health, condition.operator, condition.value);
                }
                return false;
            }
            
            closeDialog() {
                // Prevent closing if dialog was just opened (within last 200ms)
                // This prevents accidental closes from key repeat or rapid key presses
                const timeSinceOpen = Date.now() - this.lastDialogOpenTime;
                if (timeSinceOpen < 200) {
                    return;
                }
                
                const panel = document.getElementById('dialog-panel');
                if (panel) {
                    panel.classList.remove('show');
                }
                this.currentDialogNPC = null;
                this.lastDialogOpenTime = 0;
                // Clear dialog content to ensure clean state
                const content = document.getElementById('dialog-content');
                if (content) {
                    content.innerHTML = '';
                }
                const input = document.getElementById('dialog-input');
                if (input) {
                    input.style.display = 'none';
                    input.value = '';
                }
            }
            
            compareValues(a, op, b) {
                switch(op) {
                    case '>': return a > b;
                    case '<': return a < b;
                    case '>=': return a >= b;
                    case '<=': return a <= b;
                    case '==': return a == b;
                    case '!=': return a != b;
                    default: return a == b;
                }
            }
            
            evaluateRules() {
                for (let rule of this.state.rules) {
                    if (this.checkConditions(rule.conditions)) {
                        this.executeAction(rule.action);
                    }
                }
            }
            
            evaluateQuests() {
                for (let quest of this.state.quests) {
                    if (!quest.completed && this.checkConditions(quest.conditions)) {
                        this.executeAction(quest.action);
                        quest.completed = true;
                        quest.status = 'completed';
                        // Check end game after quest completion (in case quest and end_game share conditions)
                        this.checkEndGame();
                    }
                }
            }
            
            checkConditions(conditions) {
                for (let condition of conditions) {
                    if (!this.checkCondition(condition)) {
                        return false;
                    }
                }
                return true;
            }
            
            checkCondition(condition) {
                if (condition.type === 'position') {
                    const entity = this.getEntity(condition.entity);
                    if (!entity || !entity.position) return false;
                    return entity.position[0] === condition.position[0] &&
                           entity.position[1] === condition.position[1];
                } else if (condition.type === 'has') {
                    if (condition.entity === 'user') {
                        if (typeof condition.value === 'string') {
                            return this.state.user.inventory.includes(condition.value);
                        }
                    }
                } else if (condition.type === 'talked_to') {
                    if (condition.entity === 'user') {
                        return this.state.user.talked_to_npcs.includes(condition.value);
                    }
                } else if (condition.type === 'responded_to') {
                    // Check if the NPC (condition.entity is the NPC name) has responded
                    const npc = this.getEntity(condition.entity);
                    return npc && npc.has_responded === true;
                } else if (condition.type === 'comparison') {
                    const entity = this.getEntity(condition.entity);
                    if (!entity) return false;
                    const attr = condition.value; // This should be the attribute name
                    const value = entity[attr] || 0;
                    return this.compareValues(value, condition.operator, condition.value);
                }
                return false;
            }
            
            getEntity(name) {
                if (name === 'user') return this.state.user;
                for (let npc of this.state.npcs) {
                    if (npc.unique_name === name) return npc;
                }
                for (let monster of this.state.monsters) {
                    if (monster.unique_name === name) return monster;
                }
                for (let item of this.state.items) {
                    if (item.unique_name === name) return item;
                }
                for (let mythic of this.state.mythics) {
                    if (mythic.unique_name === name) return mythic;
                }
                return null;
            }
            
            executeAction(action) {
                if (action.type === 'level up') {
                    this.state.user.level += 1;
                    this.showInteractionText(
                        this.state.user.position[0],
                        this.state.user.position[1],
                        'Level Up!'
                    );
                } else if (action.type === 'talk') {
                    // Talk action - handled by interactions
                }
            }
            
            checkEndGame() {
                // Check if user is dead (health <= 0)
                if (this.state.user.health <= 0) {
                    // Check for lose condition
                    if (this.state.end_game && this.state.end_game.conditions) {
                        for (let endCondition of this.state.end_game.conditions) {
                            if (endCondition.result === 'die and lose the game') {
                                this.endGame(false);
                                return;
                            }
                        }
                    }
                    // Default lose message if no specific condition
                    this.endGame(false);
                    return;
                }
                
                if (!this.state.end_game || !this.state.end_game.conditions) return;
                
                // Group conditions by result type
                const winConditions = [];
                const loseConditions = [];
                
                for (let endCondition of this.state.end_game.conditions) {
                    if (endCondition.result === 'win the game') {
                        winConditions.push(endCondition.condition);
                    } else if (endCondition.result === 'die and lose the game') {
                        loseConditions.push(endCondition.condition);
                    }
                }
                
                // Check win conditions (ALL must be true - this handles AND conditions)
                if (winConditions.length > 0) {
                    let allWinConditionsMet = true;
                    for (let condition of winConditions) {
                        if (!this.checkCondition(condition)) {
                            allWinConditionsMet = false;
                            break;
                        }
                    }
                    if (allWinConditionsMet) {
                        this.endGame(true);
                        return;
                    }
                }
                
                // Check lose conditions (all must be true)
                if (loseConditions.length > 0) {
                    let allLoseConditionsMet = true;
                    for (let condition of loseConditions) {
                        if (!this.checkCondition(condition)) {
                            allLoseConditionsMet = false;
                            break;
                        }
                    }
                    if (allLoseConditionsMet) {
                        this.endGame(false);
                        return;
                    }
                }
            }
            
            endGame(won) {
                const message = won ? 
                    (this.state.end_game.win_message || 'You won!') :
                    (this.state.end_game.lose_message || 'You lost!');
                alert(message);
            }
            
            centerOnUser() {
                // Ensure viewport stays within bounds
                this.viewportX = Math.max(0, Math.min(this.state.user.position[0], this.state.world.width - 1));
                this.viewportY = Math.max(0, Math.min(this.state.user.position[1], this.state.world.height - 1));
            }
            
            zoomIn() {
                this.zoom = Math.min(this.zoom * 1.2, 3.0);
            }
            
            zoomOut() {
                this.zoom = Math.max(this.zoom / 1.2, 0.5);
            }
            
            showInteractionText(x, y, text) {
                const textObj = {
                    x: x,
                    y: y,
                    text: text,
                    time: Date.now()
                };
                this.interactionTexts.push(textObj);
                setTimeout(() => {
                    const index = this.interactionTexts.indexOf(textObj);
                    if (index > -1) this.interactionTexts.splice(index, 1);
                }, 2000);
            }
            
            updateUI() {
                // Update status
                const statusContent = document.getElementById('status-content');
                statusContent.innerHTML = `
                    <div>Health: ${this.state.user.health}</div>
                    <div>Experience: ${this.state.user.experience}</div>
                    <div>Level: ${this.state.user.level}</div>
                    <div>Position: (${this.state.user.position[0]}, ${this.state.user.position[1]})</div>
                `;
                
                // Update inventory
                const inventoryContent = document.getElementById('inventory-content');
                if (this.state.user.inventory.length === 0) {
                    inventoryContent.innerHTML = '<div>Inventory is empty</div>';
                } else {
                    inventoryContent.innerHTML = this.state.user.inventory.map(item => 
                        `<div>${item}</div>`
                    ).join('');
                }
                
                // Update quests
                const questContent = document.getElementById('quest-content');
                if (this.state.quests.length === 0) {
                    questContent.innerHTML = '<div>No quests</div>';
                } else {
                    questContent.innerHTML = this.state.quests.map(quest => 
                        `<div><strong>Quest ${quest.id}</strong>: ${quest.status}</div>`
                    ).join('<hr>');
                }
            }
            
            render() {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                
                const cellSize = this.cellSize * this.zoom;
                const centerX = this.canvas.width / 2;
                const centerY = this.canvas.height / 2;
                
                // Calculate visible grid
                const viewWidth = Math.ceil(this.canvas.width / cellSize) + 2;
                const viewHeight = Math.ceil(this.canvas.height / cellSize) + 2;
                const startX = Math.max(0, Math.floor(this.viewportX - viewWidth / 2));
                const startY = Math.max(0, Math.floor(this.viewportY - viewHeight / 2));
                const endX = Math.min(this.state.world.width, startX + viewWidth);
                const endY = Math.min(this.state.world.height, startY + viewHeight);
                
                // Draw terrain (grass by default)
                this.ctx.fillStyle = '#4a7c59';
                for (let y = startY; y < endY; y++) {
                    for (let x = startX; x < endX; x++) {
                        const screenX = centerX + (x - this.viewportX) * cellSize;
                        const screenY = centerY + (y - this.viewportY) * cellSize;
                        this.ctx.fillRect(screenX, screenY, cellSize, cellSize);
                    }
                }
                
                // Draw furniture
                for (let furniture of this.state.furniture) {
                    let positions = [];
                    if (furniture.placement.type === 'coordinate') {
                        positions = [furniture.placement.coord];
                    } else if (furniture.placement.type === 'range') {
                        const coord1 = furniture.placement.coord1;
                        const coord2 = furniture.placement.coord2;
                        const minX = Math.min(coord1[0], coord2[0]);
                        const maxX = Math.max(coord1[0], coord2[0]);
                        const minY = Math.min(coord1[1], coord2[1]);
                        const maxY = Math.max(coord1[1], coord2[1]);
                        for (let fx = minX; fx <= maxX; fx++) {
                            for (let fy = minY; fy <= maxY; fy++) {
                                positions.push([fx, fy]);
                            }
                        }
                    }
                    
                    // Choose emoji based on furniture name
                    let emoji = '🏠'; // default
                    if (furniture.name === 'wall' || furniture.name === 'stone') {
                        emoji = '🧱';
                    } else if (furniture.name === 'grass') {
                        emoji = '🟩';
                    }
                    
                    for (let pos of positions) {
                        const screenX = centerX + (pos[0] - this.viewportX) * cellSize;
                        const screenY = centerY + (pos[1] - this.viewportY) * cellSize;
                        if (screenX >= -cellSize && screenX <= this.canvas.width + cellSize &&
                            screenY >= -cellSize && screenY <= this.canvas.height + cellSize) {
                            this.ctx.font = `${cellSize * 0.8}px Arial`;
                            this.ctx.fillText(emoji, screenX, screenY + cellSize * 0.8);
                        }
                    }
                }
                
                // Draw items
                for (let item of this.state.items) {
                    if (!item.picked_up && item.position) {
                        const screenX = centerX + (item.position[0] - this.viewportX) * cellSize;
                        const screenY = centerY + (item.position[1] - this.viewportY) * cellSize;
                        if (screenX >= -cellSize && screenX <= this.canvas.width + cellSize &&
                            screenY >= -cellSize && screenY <= this.canvas.height + cellSize) {
                            this.ctx.font = `${cellSize * 0.8}px Arial`;
                            this.ctx.fillText('💎', screenX, screenY + cellSize * 0.8);
                        }
                    }
                }
                
                // Draw mythics
                for (let mythic of this.state.mythics) {
                    if (!mythic.picked_up && mythic.position) {
                        const screenX = centerX + (mythic.position[0] - this.viewportX) * cellSize;
                        const screenY = centerY + (mythic.position[1] - this.viewportY) * cellSize;
                        if (screenX >= -cellSize && screenX <= this.canvas.width + cellSize &&
                            screenY >= -cellSize && screenY <= this.canvas.height + cellSize) {
                            this.ctx.font = `${cellSize * 0.8}px Arial`;
                            this.ctx.fillText('💠', screenX, screenY + cellSize * 0.8);
                        }
                    }
                }
                
                // Draw monsters
                for (let monster of this.state.monsters) {
                    if (!monster.defeated && monster.position) {
                        const screenX = centerX + (monster.position[0] - this.viewportX) * cellSize;
                        const screenY = centerY + (monster.position[1] - this.viewportY) * cellSize;
                        if (screenX >= -cellSize && screenX <= this.canvas.width + cellSize &&
                            screenY >= -cellSize && screenY <= this.canvas.height + cellSize) {
                            // Boss monsters are 4x bigger
                            const isBoss = monster.monster_type === 'monster-boss';
                            const fontSize = isBoss ? cellSize * 3.2 : cellSize * 0.8; // 4x bigger = 3.2x font size (0.8 * 4)
                            this.ctx.font = `${fontSize}px Arial`;
                            
                            // Use skull emoji for dynamic/boss monsters, ogre emoji for static monsters
                            const emoji = (monster.monster_type === 'monster-dynamic' || monster.monster_type === 'monster-boss') ? '💀' : '👹';
                            const yOffset = isBoss ? cellSize * 3.2 : cellSize * 0.8;
                            this.ctx.fillText(emoji, screenX, screenY + yOffset);
                            
                            // Draw health bar if monster is in combat
                            if (monster.showHealthBar) {
                                const barY = isBoss ? screenY - 40 : screenY - 10;
                                const barSize = isBoss ? cellSize * 4 : cellSize;
                                this.drawHealthBar(screenX, barY, monster.health, monster.max_health, barSize);
                            }
                        }
                    }
                }
                
                // Draw NPCs
                for (let npc of this.state.npcs) {
                    if (npc.position) {
                        const screenX = centerX + (npc.position[0] - this.viewportX) * cellSize;
                        const screenY = centerY + (npc.position[1] - this.viewportY) * cellSize;
                        if (screenX >= -cellSize && screenX <= this.canvas.width + cellSize &&
                            screenY >= -cellSize && screenY <= this.canvas.height + cellSize) {
                            this.ctx.font = `${cellSize * 0.8}px Arial`;
                            this.ctx.fillText(npc.emoji, screenX, screenY + cellSize * 0.8);
                        }
                    }
                }
                
                // Draw user
                const userScreenX = centerX + (this.state.user.position[0] - this.viewportX) * cellSize;
                const userScreenY = centerY + (this.state.user.position[1] - this.viewportY) * cellSize;
                this.ctx.font = `${cellSize * 0.8}px Arial`;
                this.ctx.fillText('🧙', userScreenX, userScreenY + cellSize * 0.8);
                
                // Draw health bar if user is in combat
                if (this.state.user.showHealthBar) {
                    this.drawHealthBar(userScreenX, userScreenY - 10, this.state.user.health, 100, cellSize);
                }
                
                // Draw interaction texts
                for (let textObj of this.interactionTexts) {
                    const screenX = centerX + (textObj.x - this.viewportX) * cellSize;
                    const screenY = centerY + (textObj.y - this.viewportY) * cellSize - 20;
                    this.ctx.fillStyle = '#fff';
                    this.ctx.font = '12px Arial';
                    this.ctx.fillText(textObj.text, screenX, screenY);
                    this.ctx.fillStyle = '#000';
                }
            }
            
            drawHealthBar(x, y, currentHealth, maxHealth, cellSize) {
                const barWidth = cellSize * 0.8;
                const barHeight = 6;
                const healthPercent = Math.max(0, Math.min(1, currentHealth / maxHealth));
                
                // Draw background (red/dark)
                this.ctx.fillStyle = '#333';
                this.ctx.fillRect(x - barWidth / 2, y, barWidth, barHeight);
                
                // Draw health (green to red gradient)
                if (healthPercent > 0.5) {
                    this.ctx.fillStyle = '#0f0'; // Green
                } else if (healthPercent > 0.25) {
                    this.ctx.fillStyle = '#ff0'; // Yellow
                } else {
                    this.ctx.fillStyle = '#f00'; // Red
                }
                this.ctx.fillRect(x - barWidth / 2, y, barWidth * healthPercent, barHeight);
                
                // Draw border
                this.ctx.strokeStyle = '#fff';
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(x - barWidth / 2, y, barWidth, barHeight);
            }
            
            gameLoop() {
                this.updateDynamicMonsters();
                this.render();
                requestAnimationFrame(() => this.gameLoop());
            }
            
            updateDynamicMonsters() {
                // Update dynamic monsters to chase the hero if within 10 units
                const heroPos = this.state.user.position;
                const currentTime = Date.now();
                
                for (let monster of this.state.monsters) {
                    if ((monster.monster_type === 'monster-dynamic' || monster.monster_type === 'monster-boss') && !monster.defeated && monster.position) {
                        const dx = heroPos[0] - monster.position[0];
                        const dy = heroPos[1] - monster.position[1];
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        // Check if monster is adjacent to player (distance <= 1 for adjacent cells)
                        const isAdjacent = Math.abs(dx) <= 1 && Math.abs(dy) <= 1 && (Math.abs(dx) + Math.abs(dy)) <= 1;
                        
                        // Attack player if adjacent and cooldown has passed (3 seconds = 3000ms)
                        if (isAdjacent) {
                            // Initialize lastAttackTime if not set
                            if (!monster.lastAttackTime) {
                                monster.lastAttackTime = 0;
                            }
                            
                            // Attack if 3 seconds (3000ms) have passed since last attack
                            if (currentTime - monster.lastAttackTime >= 3000) {
                                monster.lastAttackTime = currentTime;
                                
                                // Show health bars for combat
                                monster.showHealthBar = true;
                                this.state.user.showHealthBar = true;
                                
                                // Set timeout to hide health bars after 3 seconds
                                if (monster.healthBarTimeout) {
                                    clearTimeout(monster.healthBarTimeout);
                                }
                                if (this.state.user.healthBarTimeout) {
                                    clearTimeout(this.state.user.healthBarTimeout);
                                }
                                monster.healthBarTimeout = setTimeout(() => {
                                    monster.showHealthBar = false;
                                }, 3000);
                                this.state.user.healthBarTimeout = setTimeout(() => {
                                    this.state.user.showHealthBar = false;
                                }, 3000);
                                
                                // Deal damage to player (2 for boss, 1 for dynamic)
                                const damage = monster.monster_type === 'monster-boss' ? 2 : 1;
                                this.state.user.health -= damage;
                                
                                // Check if user is defeated
                                if (this.state.user.health <= 0) {
                                    this.checkEndGame(); // This will trigger lose condition if health <= 0
                                }
                                
                                this.updateUI();
                            }
                        }
                        // If hero is within 10 units but not adjacent, move towards hero slowly
                        else if (distance <= 10 && distance > 0) {
                            // Calculate direction (normalized)
                            const dirX = dx / distance;
                            const dirY = dy / distance;
                            
                            // Move slowly (0.1 units per frame, but we'll move in discrete steps)
                            // Use a counter to slow down movement
                            if (!monster.moveCounter) {
                                monster.moveCounter = 0;
                            }
                            monster.moveCounter++;
                            
                            // Move every 10 frames (adjust for speed)
                            if (monster.moveCounter >= 10) {
                                monster.moveCounter = 0;
                                
                                // Calculate new position (move 1 unit towards hero)
                                let newX = monster.position[0];
                                let newY = monster.position[1];
                                
                                // Move in the direction of the hero (discrete movement)
                                if (Math.abs(dirX) > Math.abs(dirY)) {
                                    newX += dirX > 0 ? 1 : -1;
                                } else {
                                    newY += dirY > 0 ? 1 : -1;
                                }
                                
                                // Check if the new position is valid (not blocked)
                                if (this.canMonsterMoveTo(newX, newY)) {
                                    monster.position[0] = newX;
                                    monster.position[1] = newY;
                                }
                            }
                        }
                    }
                }
            }
            
            canMonsterMoveTo(x, y) {
                // Check boundaries
                if (x < 0 || x >= this.state.world.width ||
                    y < 0 || y >= this.state.world.height) {
                    return false;
                }
                
                // Check furniture (walls, stone are impassible)
                for (let furniture of this.state.furniture) {
                    if (furniture.placement.type === 'coordinate') {
                        const pos = furniture.placement.coord;
                        if (pos[0] === x && pos[1] === y) {
                            if (furniture.name === 'wall' || furniture.name === 'stone') {
                                return false;
                            }
                        }
                    } else if (furniture.placement.type === 'range') {
                        const coord1 = furniture.placement.coord1;
                        const coord2 = furniture.placement.coord2;
                        const minX = Math.min(coord1[0], coord2[0]);
                        const maxX = Math.max(coord1[0], coord2[0]);
                        const minY = Math.min(coord1[1], coord2[1]);
                        const maxY = Math.max(coord1[1], coord2[1]);
                        if (x >= minX && x <= maxX && y >= minY && y <= maxY) {
                            if (furniture.name === 'wall' || furniture.name === 'stone') {
                                return false;
                            }
                        }
                    }
                }
                
                // Don't check collisions with other monsters/NPCs for now (monsters can overlap)
                // But don't move into the hero's position
                if (this.state.user.position[0] === x && this.state.user.position[1] === y) {
                    return false;
                }
                
                return true;
            }
            
            saveGame() {
                const saveData = {
                    version: '1.0',
                    timestamp: new Date().toISOString(),
                    game_state: this.state
                };
                const blob = new Blob([JSON.stringify(saveData, null, 2)], {type: 'application/json'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'game_save.json';
                a.click();
                URL.revokeObjectURL(url);
            }
            
            loadGame(event) {
                const file = event.target.files[0];
                if (!file) return;
                
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const saveData = JSON.parse(e.target.result);
                        this.state = saveData.game_state;
                        this.updateUI();
                        alert('Game loaded successfully');
                    } catch (error) {
                        alert('Failed to load game: ' + error.message);
                    }
                };
                reader.readAsText(file);
            }
            
            showSplashScreen() {
                if (!this.state.on_game_start || !this.state.on_game_start.title) {
                    return; // No splash screen configured
                }
                
                const splashScreen = document.getElementById('splash-screen');
                const splashTitle = document.getElementById('splash-title');
                const splashText = document.getElementById('splash-text');
                
                if (splashScreen && splashTitle && splashText) {
                    splashTitle.textContent = this.state.on_game_start.title;
                    
                    // Clear existing text
                    splashText.innerHTML = '';
                    
                    // Add each text line as a paragraph
                    if (this.state.on_game_start.text_lines && this.state.on_game_start.text_lines.length > 0) {
                        this.state.on_game_start.text_lines.forEach(text => {
                            const p = document.createElement('p');
                            p.textContent = text;
                            splashText.appendChild(p);
                        });
                    }
                    
                    // Add links
                    if (this.state.on_game_start.links && this.state.on_game_start.links.length > 0) {
                        const linksDiv = document.createElement('div');
                        linksDiv.style.marginTop = '20px';
                        linksDiv.style.display = 'flex';
                        linksDiv.style.flexWrap = 'wrap';
                        linksDiv.style.gap = '15px';
                        linksDiv.style.justifyContent = 'center';
                        
                        this.state.on_game_start.links.forEach(link => {
                            const [anchorText, url] = link;
                            const a = document.createElement('a');
                            a.href = url;
                            a.textContent = anchorText;
                            a.target = '_blank';
                            a.rel = 'noopener noreferrer';
                            a.style.color = '#ffd700';
                            a.style.textDecoration = 'none';
                            a.style.padding = '8px 16px';
                            a.style.border = '2px solid #ffd700';
                            a.style.borderRadius = '5px';
                            a.style.transition = 'all 0.3s';
                            a.style.display = 'inline-block';
                            a.onmouseenter = function() {
                                this.style.background = '#ffd700';
                                this.style.color = '#1e3c72';
                            };
                            a.onmouseleave = function() {
                                this.style.background = 'transparent';
                                this.style.color = '#ffd700';
                            };
                            linksDiv.appendChild(a);
                        });
                        
                        splashText.appendChild(linksDiv);
                    }
                    
                    splashScreen.classList.add('show');
                }
            }
            
            closeSplashScreen() {
                const splashScreen = document.getElementById('splash-screen');
                if (splashScreen) {
                    splashScreen.classList.remove('show');
                }
            }
        }
        
        // Initialize game
        let game;
        window.addEventListener('load', () => {
            game = new DungeonGame();
        });
        """
        return engine_code.replace('LLM_ENDPOINT_PLACEHOLDER', llm_endpoint).replace('LLM_TOKEN_PLACEHOLDER', llm_token)


def main():
    if len(sys.argv) < 2:
        print("Usage: python compile_dungeon.py <input_file> [output_file]")
        print("  input_file:  DSL source file to compile")
        print("  output_file: Output HTML file (default: game.html)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "game.html"
    
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Lex
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        program = parser.parse()
        
        # Validate
        validator = Validator(program)
        validator.validate()
        
        if validator.errors:
            print("Compilation errors found:")
            for error in validator.errors:
                print(f"  ERROR: {error}")
            sys.exit(1)
        
        # Generate code
        generator = CodeGenerator(program)
        html_output = generator.generate()
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"Successfully compiled {input_file} to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
