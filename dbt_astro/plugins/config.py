from env_variables import ACCESS_TOKEN

MONZO_API_BASE = "https://api.monzo.com"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
