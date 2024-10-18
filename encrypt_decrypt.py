def xor_encrypt_decrypt(text, key):
    encrypted_decrypted = []
    key_length = len(key)

    # Шифрование/дешифрование, используя символы ключа по циклу
    for i, char in enumerate(text):
        # Циклично используем ключ
        current_key_char = key[i % key_length]

        # Преобразуем символ ключа в ASCII
        key_char_code = ord(current_key_char)

        # XOR операции
        encrypted_decrypted_char = chr(ord(char) ^ key_char_code)
        encrypted_decrypted.append(encrypted_decrypted_char)

    return ''.join(encrypted_decrypted)
