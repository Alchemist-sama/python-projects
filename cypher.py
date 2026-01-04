alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))
def encrypt(original_text, shift_amount):
    cypher_text =""
    for letter in original_text:
        position = alphabet.index(letter)
        new_position = (position + shift_amount)%26
        new_letter = alphabet[new_position]
        cypher_text += new_letter
        print(f"The encoded text is {cypher_text}")
def decrypt(original_text, shift_amount):
    plain_text =""
    for letter in original_text:
        position = alphabet.index(letter)
        new_position = (position - shift_amount)%26
        new_letter = alphabet[new_position]
        plain_text += new_letter
        print(f"the decoded text is {plain_text}")
if direction == "decode":
    decrypt(original_text=text, shift_amount=shift) 
elif direction == "encode":           
    encrypt(original_text=text, shift_amount=shift)