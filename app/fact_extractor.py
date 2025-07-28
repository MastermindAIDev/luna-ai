import re


def extract_facts(user_input, existing_facts):
    facts = []
    memory_text = "\n".join(existing_facts)
    cleaned_input = user_input.strip()

    # Name
    if re.match(r"^\s*my name is\b", cleaned_input, re.IGNORECASE):
        name_match = re.search(r"my name is (\w+)",
                               cleaned_input, re.IGNORECASE)
        if name_match:
            fact = f"User's name is {name_match.group(1).capitalize()}."
            if fact not in memory_text:
                facts.append(fact)

    # Age
    if re.match(r"^\s*(i am|i'm|my age is)\b", cleaned_input, re.IGNORECASE):
        age_match = re.search(
            r"(i am|i'm|my age is)\s+(\d{1,3})", cleaned_input, re.IGNORECASE)
        if age_match:
            fact = f"User is {age_match.group(2)} years old."
            if fact not in memory_text:
                facts.append(fact)

    # Occupation
    if re.match(r"^\s*(i work as|my job is|i am a|i'm a)\b", cleaned_input, re.IGNORECASE):
        occ_match = re.search(
            r"(i work as|my job is|i am a|i'm a)\s+(.+?)(\.|$)", cleaned_input, re.IGNORECASE)
        if occ_match:
            occupation = occ_match.group(2).strip()
            fact = f"User works as {occupation}."
            if fact not in memory_text:
                facts.append(fact)

    # Hobby
    if re.match(r"^\s*(i like|i enjoy|my hobby is|my hobbies are)\b", cleaned_input, re.IGNORECASE):
        hobby_match = re.search(
            r"(i like|i enjoy|my hobby is|my hobbies are)\s+(.+?)(\.|$)", cleaned_input, re.IGNORECASE)
        if hobby_match:
            hobby = hobby_match.group(2).strip()
            fact = f"User enjoys {hobby}."
            if fact not in memory_text:
                facts.append(fact)

    # Location
    if re.match(r"^\s*(i live in|i'm from|i am from)\b", cleaned_input, re.IGNORECASE):
        location_match = re.search(
            r"(i live in|i'm from|i am from)\s+(.+?)(\.|$)", cleaned_input, re.IGNORECASE)
        if location_match:
            location = location_match.group(2).strip()
            fact = f"User lives in {location}."
            if fact not in memory_text:
                facts.append(fact)

    # Favorite color
    if re.match(r"^\s*(my favorite color is|i like the color)\b", cleaned_input, re.IGNORECASE):
        color_match = re.search(
            r"(my favorite color is|i like the color)\s+(\w+)", cleaned_input, re.IGNORECASE)
        if color_match:
            color = color_match.group(2).strip()
            fact = f"User's favorite color is {color}."
            if fact not in memory_text:
                facts.append(fact)

    # Pet
    if re.search(r"\b(i have a|my pet is a)\b", cleaned_input, re.IGNORECASE):
        pet_match = re.search(
            r"(i have a|my pet is a)\s+(\w+)", cleaned_input, re.IGNORECASE)
        if pet_match:
            pet = pet_match.group(2).strip()
            fact = f"User has a {pet}."
            if fact not in memory_text:
                facts.append(fact)

    # Favorite food
    if re.match(r"^\s*(my favorite food is|i love eating|i like eating|i enjoy eating)\b", cleaned_input, re.IGNORECASE):
        food_match = re.search(
            r"(my favorite food is|i love eating|i like eating|i enjoy eating)\s+(.+?)(\.|$)",
            cleaned_input, re.IGNORECASE
        )
        if food_match:
            food = food_match.group(2).strip()
            fact = f"User's favorite food is {food}."
            if fact not in memory_text:
                facts.append(fact)

    # Birthday
    if re.search(r"\b(my birthday is|i was born on)\b", cleaned_input, re.IGNORECASE):
        birthday_match = re.search(
            r"(my birthday is|i was born on)\s+([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?)(\.|$)",
            cleaned_input, re.IGNORECASE
        )
        if birthday_match:
            birthday = birthday_match.group(2).strip()
            fact = f"User's birthday is {birthday}."
            if fact not in memory_text:
                facts.append(fact)

    return facts
