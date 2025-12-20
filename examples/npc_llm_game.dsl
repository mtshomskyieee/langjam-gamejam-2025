init:
    world: 20 x 20 grid
    furniture:
        grass at all
    llm:
        endpoint "http://localhost:1234/v1/chat/completions"
        token "anything"
    npc:
        npc-dynamic: unique_name="echo" place at (10, 10) context "You are Echo, a helpful assistant that repeats and responds to the user's messages."  response "This is the backup response if the LLM is not working. this project has a local_llm directory that you can use to host a local LLM and carry on a conversation with an LLM."
    user: unique_name="player", context "hero", at (5, 5)
quests:
end_game:

