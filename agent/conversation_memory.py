conversation_memory = []


def save_conversation(
    user_query,
    ai_answer
):

    conversation_memory.append(
        {
            "user_query":
            user_query,

            "ai_answer":
            ai_answer
        }
    )

    if len(
        conversation_memory
    ) > 5:

        conversation_memory.pop(0)


def get_recent_conversations():

    return conversation_memory