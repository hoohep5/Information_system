import base64
import socket
from cryptography.fernet import Fernet
from threading import Thread
import HashTable


ht = HashTable.HashTable(20)
ht = ht.load_from_file('HashUsers.txt')


class User:
    def __init__(self, key):
        login = 0
        ip = 0
        password = 0

