import bcrypt

plain_password = "admin_password"  # Admin için belirlediğiniz şifre
hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print("Hashed Password:", hashed_password)
