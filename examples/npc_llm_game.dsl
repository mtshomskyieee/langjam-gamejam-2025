init:
    world: 20 x 20 grid
    furniture:
        grass at all
    llm:
        endpoint "http://localhost:1234/v1/chat/completions"
        token "anything"
    npc:
        npc-dynamic: unique_name="echo" place at (10, 10) context "You are Echo, a helpful assistant that repeats and responds to the user's messages."
    user: unique_name="player", context "hero", at (5, 5)
quests:
end_game:

