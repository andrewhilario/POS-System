from uuid import uuid4

uuid = uuid4()
truncate_uuid = str(uuid)[:4]
truncate_uuid = truncate_uuid.upper()

print("CODE"+truncate_uuid)