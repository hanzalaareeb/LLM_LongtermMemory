from sqlalchemy.orm import Session
from db import Memory, SessionLocal, User
from datetime import datetime

"""
Summary:
    - Store data into core memory.
    - Retrieve memory from the core memory.
"""

class MemoryManager: # parent class
    def __init__(self):
        self.db = SessionLocal()  

    def close_session(self):
        self.db.close()  

class MemoryLayer(MemoryManager): # child class (class MemoryLayer enherits "Memory" from MemoryManager() class)
    def __init__(self):
        super().__init__()  
        
        """ 
        extending features of parent class to child class 
        (concept of enharitance I know Teto don't know this and will probabily say it is ChatGPT generated)
        
        """

    def addInter(self, user, core_memory, user_info_memory, other_memory):
        new_interaction = Memory(
            user_id=user.id,
            core_memory=core_memory,
            user_info_memory=user_info_memory,
            other_memory=other_memory,
            timestamp=datetime.now()
            )
        self.db.add(new_interaction)
        self.db.commit()
        self.db.refresh(new_interaction)
        
        

    def get_user_memories(self, user_id):
        """Retrieves all memory records for a specific user."""
        return self.db.query(Memory).filter(Memory.user_id == user_id).all()
    
    def delete_user_memories(self, user_id):
        """Deletes all memory records for a specific user."""
        self.db.query(Memory).filter(Memory.user_id == user_id).delete()    
        self.db.commit()
        return True
    
    def get_memory_lists(self, user_id):
        """get back all memory records for a user_id"""
        db = SessionLocal()
        try:
            memories = db.query(Memory).filter(Memory.user_id == user_id).all()
            
            core_memories = [memory.core_memory for memory in memories]
            user_info_memories = [memory.user_info_memory for memory in memories]
            other_memories = [memory.other_memory for memory in memories]
            
            return core_memories, user_info_memories, other_memories
        finally:
            db.close()


if __name__ == "__main__":
    memory_layer = MemoryLayer()
    new_user = User(name="haz")
    memory_layer.db.add(new_user)
    memory_layer.db.commit()  
    memory_layer.addInter(new_user, "Hello, i feel sad today.", "i like ice cream", "i like birds")
    memories = memory_layer.get_user_memories(new_user.id)
    print(memory_layer.get_memory_lists(new_user.id))
    # for memory in memories:
        # print(f"user_name: {memory.user.name}, memory_id: {memory.id}, core_memory: {memory.core_memory}, user_info: {memory.user_info_memory}, other_memory: {memory.other_memory}, time: {memory.timestamp}")
        # delete_result = memory_layer.delete_user_memories(new_user.id)
        # print(f"Delete result: {delete_result}")
    memory_layer.close_session()
    
