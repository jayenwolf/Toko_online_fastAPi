from passlib.context import CryptContext

# untuk mengatur PW mengacak menggunakan standar algoritma bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# fungsinya untuk mengacak pw (saat register)
def acak_password(password_asli: str):
    # untuk memotong pw dari max nya 72 byte agar tidak terjadi nya eror di bcrypt
    pw_batas = password_asli[:72]
    return pwd_context.hash(pw_batas)

# fungsi untuk mencocokkan pw saat login
def cek_pw(password_asli: str, passwrod_acak: str):
    return pwd_context.verify(password_asli, passwrod_acak)