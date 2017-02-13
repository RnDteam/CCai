# CCai
Hebrew Call Center for MVP 1

Our bot is based on entity extraction and intent recognition.
We're trying to find the entity the user talks about using a simple search of our synonyms list for each entity,
and same process for reaching the action.

Our purpose is to create a Call Center chatbot, which determines what is the user's need and directing him into a known conversation flow.
The conversation flow is based on our format which uses a simple format for creating a conversation(out for printing, and in for input).

Done:
-   Saving user's input for future. V
-   An option to go back when already in a flow. V
-   Printing a message when the bot didn't understand to input. V
-   Summary of input at the end of the conversation. V
-   Execute the action the user asked for. V

(python 3 required)
To view our chat -
    1) run hebChatbot\server.py
    2) run SimpleWebSocketServer\SimpleExampleServer.py
    3) view chatUI\index.html