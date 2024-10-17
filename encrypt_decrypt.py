def xor_encrypt_decrypt(text, key):
    encrypted_decrypted = []
    key_length = len(key)

    # Шифрование/дешифрование, используя символы ключа по циклу
    for i, char in enumerate(text):
        current_key_char = key[i % key_length]  # Циклично используем ключ
        key_char_code = ord(current_key_char)   # Преобразуем символ ключа в ASCII
        encrypted_decrypted_char = chr(ord(char) ^ key_char_code)  # XOR операции
        encrypted_decrypted.append(encrypted_decrypted_char)

    return ''.join(encrypted_decrypted)