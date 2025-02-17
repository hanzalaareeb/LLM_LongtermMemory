from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from model import ConversationTurn, SessionLocal, User
import logging

# Create a session
session = SessionLocal()

def get_or_create_user(username):
    """Fetch a user from the database or create a new one."""
    user = session.query(User).filter(User.name == username).first()
    if not user:
        user = User(name=username)
        session.add(user)
        session.commit()
        print(f"Created new user: {username}")
    return user

def add_conversation_turn(user, message, answer, character="Bot"):
    """Add a conversation turn to the database."""
    conversation_turn = ConversationTurn(
        user_id=user.id,
        message_date_local=date.today(),
        message=message,
        # answered_at=datetime.now(),
        answer=answer,
        character=character
    )
    try:
        session.add(conversation_turn)
        session.commit()
        ConversationTurn.convert_to_string(conversation_turn)
    except Exception as e:
        session.rollback()
        print(f"Error saving conversation: {e}")
    finally:
        session.close()

def main():
    username = input("Enter your name: ").strip()
    user = get_or_create_user(username)

    while True:
        message = input(f"{user.name}: ").strip()
        if message.lower() == "quit":
            break  # Exit the loop

        answer = input("Bot: ").strip()
        try:
            add_conversation_turn(user, message, answer)
            logging.info("saved")
        except Exception as e:
            print(f"Error saving conversation: {e}")



if __name__ == "__main__":
    main()

# Close session
session.close()
