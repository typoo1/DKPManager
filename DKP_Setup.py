import sqlite3

connection = sqlite3.connect("DKP.db")

crsr = connection.cursor()

# crsr.execute("""DROP TABLE Player""")
# crsr.execute("""DROP TABLE Characters""")
# crsr.execute("""DROP TABLE Role""")
# crsr.execute("""DROP TABLE Item""")
# crsr.execute("""DROP TABLE IF EXISTS Transactions""")

# sql_command = """CREATE TABLE Role(
#  role VARCHAR(30) PRIMARY KEY NOT NULL,
#  dkp_multi FLOAT NOT NULL)"""
#
# crsr.execute(sql_command)
#
# sql_command = """CREATE TABLE Item(
#  item_id INTEGER PRIMARY KEY NOT NULL,
#  description VARCHAR(255),
#  ilevel INTEGER NOT NULL)"""
#
# crsr.execute(sql_command)
#
# sql_command = """CREATE TABLE Characters(
#  character_id INTEGER PRIMARY KEY NOT NULL,
#  class VARCHAR(30) NOT NULL,
#  level INTEGER NOT NULL,
#  role VARCHAR(30) NOT NULL,
#  character_name VARCHAR(30) NOT NULL UNIQUE,
#  player_id INTEGER,
#  FOREIGN KEY(player_id) REFERENCES Player(player_id),
#  FOREIGN KEY(role) REFERENCES Role(role))"""
#
# crsr.execute(sql_command)

# sql_command = """CREATE TABLE Player(
#  player_id INTEGER PRIMARY KEY NOT NULL,
#  DKP INTEGER NOT NULL,
#  player_name VARCHAR(30) NOT NULL)"""
#
# crsr.execute(sql_command)
# 
# sql_command = """CREATE TABLE Transactions(
#  transaction_id INTEGER PRIMARY KEY NOT NULL,
#  buyer_id INTEGER NOT NULL,
#  seller_id INTEGER NOT NULL,
#  cost INTEGER NOT NULL,
#  date DATETIME NOT NULL,
#  item_id INTEGER NOT NULL,
#  FOREIGN KEY(buyer_id) REFERENCES Player(player_id),
#  FOREIGN KEY(seller_id) REFERENCES Player(player_id),
#  FOREIGN KEY(item_id) REFERENCES Item(item_id))"""
# 
# crsr.execute(sql_command)

connection.commit()

connection.close()

