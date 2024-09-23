import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", password="root", database="mydatabase"
)
mycursor = mydb.cursor()

mycursor.execute(
    """
    CREATE TABLE IF NOT EXISTS secrets (
        macaddress VARCHAR(255),
        ipaddress VARCHAR(255),
        secret BLOB PRIMARY KEY
    )
    """
)


def save_key(key, ipaddress, macaddress):
    query = """
    INSERT INTO secrets (secret, ipaddress, macaddress) VALUES (%s, %s, %s)
    """
    key_hex = key.hex()
    val = (key_hex.encode("utf-8"), ipaddress, macaddress)
    mycursor.execute(query, val)
    mydb.commit()


def get_key(ipaddress, macaddress):
    query = "SELECT secret FROM secrets WHERE ipaddress = %s AND macaddress = %s"
    val = (ipaddress, macaddress)
    mycursor.execute(query, val)
    result = mycursor.fetchone()
    if result:
        return bytes.fromhex(result[0])
    return None
