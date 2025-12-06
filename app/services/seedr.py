from seedrcc import Token

from app.database import get_session
from app.database.repository import AccountRepository


async def on_token_refresh(new_token: Token, account_id: int, user_id: int) -> None:
    """Callback to update token in database when it's refreshed."""
    async with get_session() as new_session:
        account_repo = AccountRepository(new_session)
        await account_repo.update_token(account_id, user_id, new_token.to_base64())
        await new_session.commit()
