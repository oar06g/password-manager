# FUNCTION FILE 
from PIL import Image
from cryptography.fernet import Fernet

def resize_image(path_image, w, h):
  img = Image.open(str(path_image))
  new_size = (w, h)
  resized_img = img.resize(new_size)
  resized_img.save("E:\\2024\\My Projects\\continues\\manage_pass\\images\\background.jpg")
# resize_image("E:\\2024\\My Projects\\continues\\manage_pass\\images\\background.jpg", 800, 600)

# Generate a key
# def generate_key():
#     key = Fernet.generate_key()
#     with open("secret.key", "wb") as key_file:
#         key_file.write(key)

# Encrypt a message
def encrypt(text: str, key: str):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(text.encode())
    return encrypted_message

# Decrypt a message
def decrypt(text: str, key: str):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(text).decode()
    return decrypted_message
