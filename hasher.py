 
from werkzeug.security import generate_password_hash

input = "admin"
hashed = generate_password_hash(input)
print(hashed)