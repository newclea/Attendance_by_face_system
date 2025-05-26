import secrets
import hashlib

random_bytes = secrets.token_bytes(64)  # 生成64字节的随机数据
secret_key = hashlib.sha256(random_bytes).hexdigest()

print(secret_key)
