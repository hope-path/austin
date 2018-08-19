import os
URL = os.environ.get("mailgun_url")

API_KEY =  os.environ.get("mailgun_key")
FROM =  os.environ.get("mailgun_from")

ALERT_TIMEOUT = 5
COLLECTION = 'alerts'


