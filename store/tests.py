import uuid

def generate_uuid():
    # Generate a UUID using the uuid1 function
    uuid_str = str(uuid.uuid1())
    # Keep only the numeric characters from the UUID
    uuid_num = ''.join(c for c in uuid_str if c.isdigit())
    # Return the first 8 characters of the UUID
    return uuid_num[:8]

# Generate a UUID
uuid = generate_uuid()

print(uuid)  # Outputs a 8-character UUID composed of numbers only
