from datetime import datetime
class Task:
    def __init__(self, name, description, status="TODO", created_at=None):
        self.name = name
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now()


    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    def __str__(self):
        return f"{self.name}: {self.description} ({self.status})"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["description"], data["status"], datetime.fromisoformat(data["created_at"]))
