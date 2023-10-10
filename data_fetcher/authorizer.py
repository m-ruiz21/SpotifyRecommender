import tekore as tk
from dotenv import dotenv_values, load_dotenv
from tekore._client import Spotify

def authorize() -> Spotify:
    loaded = load_dotenv(dotenv_path=".env")
    if not loaded:
        raise ValueError("No .env file found")

    env_values = dotenv_values()
    client_id: str | None = env_values["SPOTIFY_CLIENT_ID"] 
    secret_key: str | None = env_values["SPOTIFY_CLIENT_SECRET"]
    
    if client_id is None or secret_key is None:
        raise ValueError("SPOTIFY_CLIENT_ID or SPOTIFY_SECRET_KEY not found in environment variables")

    token: tk.RefreshingToken = tk.request_client_token(client_id, secret_key)
    return tk.Spotify(token)
