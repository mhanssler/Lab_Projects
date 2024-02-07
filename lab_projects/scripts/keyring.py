import keyring
keyring.set_password("GNU/Linux", "morgan", "Battlefield$$$321")
print(keyring.get_password("GNU/Linux", "morgan"))

