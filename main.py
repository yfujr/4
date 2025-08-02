import random
import string

# Phonetic pools
vowels = 'aeiou'
consonants = ''.join(set(string.ascii_lowercase) - set(vowels))

# Set size and count
USERNAME_LENGTH = 5
COUNT = 100  # Number of usernames to generate

def generate_cvcvc():
    """Generates CVCVC or similar patterns to sound like one-syllable."""
    patterns = [
        'cvcvc', 'ccvvc', 'cvccv', 'vcvcv'
    ]
    pattern = random.choice(patterns)
    name = ''

    for char in pattern:
        if char == 'v':
            name += random.choice(vowels)
        else:
            name += random.choice(consonants)
    return name

# Main loop
usernames = set()
while len(usernames) < COUNT:
    uname = generate_cvcvc()
    if len(uname) == USERNAME_LENGTH:
        usernames.add(uname)

# Output to console and save
print("Generated Usernames:")
for u in usernames:
    print(f" - {u}")

# Save to file
with open("aesthetic_usernames.txt", "w") as f:
    for u in usernames:
        f.write(u + "\n")
