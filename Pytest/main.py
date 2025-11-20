def get_weather(temp):
    if temp > 20:
        return "hot"
    else:
        return "cold"
    
def add(a,b):
    return a + b

def divide(a,b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username,email):
        if username in self.users:
            raise ValueError("User already exists.")
        self.users[username] = email
        return True

    def get_user(self, username):
        return self.users.get(username)
    
class Database:
    """Simulates a basic user database."""
    def __init__(self):
        self.data = {}

    def add_user(self, user_id, name):
        if user_id in self.data: 
            raise ValueError("User already exists")
        self.data[user_id] = name

    def get_user(self, user_id):
        return self.data.get(user_id, None)
    
    def delete_user(self, user_id):
        if user_id in self.data:
            del self.data[user_id]
        

def is_prime(n):
    if n <= 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True