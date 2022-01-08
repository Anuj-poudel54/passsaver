

chars = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """*50

def enc(text):
    enc_text = ""
    for i in range(len(text)):
        char_index = chars.find(text[i])
        new_char_index = char_index - 4
        new_char = chars[new_char_index]
        enc_text = enc_text + new_char
    return enc_text


def dec(text):

    dec_text = ""
    for i in range(len(text)):
        char_index = chars.find(text[i])
        new_char_index = char_index + 4
        new_char = chars[new_char_index]
        dec_text = dec_text + new_char
    return dec_text


if __name__ == '__main__':
    str = "Hello how AAAre y23!*@)_#our @21342342"
    enc_str = enc(str)
    dec_str = dec(enc_str)
    if str == dec_str:
        print("Working fine")
        print(f"'{str}'")
        print(f"'{dec_str}'")
    else:
        print("Not working")
        print(f"'{str}'")
        print(f"'{dec_str}'")
