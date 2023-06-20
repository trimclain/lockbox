#!/usr/bin/env python3

import random
import string

CHARS = string.ascii_letters + string.digits*4

def generate_password(stringLength=random.randint(10,20)):
    return ''.join(random.choice(CHARS) for i in range(stringLength))

if __name__ == "__main__":
    print(generate_password())

