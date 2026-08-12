from langchain_core.chat_history import InMemoryChatMessageHistory

_histories: dict[str, InMemoryChatMessageHistory] = {}


def get_history(user_id: str) -> InMemoryChatMessageHistory:
    if user_id not in _histories:
        _histories[user_id] = InMemoryChatMessageHistory()
    return _histories[user_id]


def clear_history(user_id: str) -> None:
    _histories.pop(user_id, None)