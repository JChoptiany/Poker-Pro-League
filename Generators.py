import random


def generate_password() -> str:
        adjectives = ['pretty', 'awesome', 'pink', 'colorful', 'strong', 'smart', 'beautiful', 'tall', 'stunning', 'hot', 'cute', 'gorgeous', 'nice', 'good', 'famous', 'wonderful', 'handsome']
        nouns = ['salmon', 'octopus', 'snail', 'dog', 'cat', 'elephant', 'turtle', 'raccoon', 'chihuahua', 'train', 'car', 'helicopter', 'plane', 'flower', 'cucumber', 'eggplant', 'broccoli', 'carrot', 'parrot']

        adjectiveIndex = random.randint(0, len(adjectives)-1)
        nounIndex = random.randint(0, len(nouns)-1)

        password = adjectives[adjectiveIndex].title() + nouns[nounIndex].title() + str(random.randint(1000,9999))

        return password

def generate_nickname(first_name: str, last_name: str, date_of_birth: str) -> str:       
        sum_of_date_digits = sum(int(char) for char in date_of_birth if char.isdigit())
        number = int(int(str(sum_of_date_digits) + date_of_birth[2:4]) * random.random() * 10)

        nickname = first_name[0] + last_name + str(number)
        
        return nickname
