import os
import requests
from typing import Any, Optional

class BrawlStarsAPIClient:
    key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjA2NzQ4OTA3LWUzOTMtNGFhMS1iMjczLTY5YWNlZmQ4YWZkZiIsImlhdCI6MTc0NTc2NzY1OCwic3ViIjoiZGV2ZWxvcGVyLzY2OWEzM2M5LWQwYTgtN2Q5NC0wZTdlLTVmNjk2M2JhYWFkYiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTc5LjQyLjQuMTIyIl0sInR5cGUiOiJjbGllbnQifV19.v0M_Quus5-jiJo_dJV0j2WTC747c9CLwx7iXUr4TIpheuQL6PDQDlJm7NJX9DhopTYgOAq9qO29CcrOUpLZhbA"
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("BRAWL_API_KEY")
        self.base_url = "https://api.brawlstars.com/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        })

    def _get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        if response.status_code == 403:
            raise PermissionError("403 - Verifique se sua API Key está correta e ativada.")
        elif response.status_code == 429:
            raise RuntimeError("429 - Rate limit atingido, aguarde e tente novamente.")
        elif response.status_code != 200:
            raise Exception(f"Erro inesperado {response.status_code}: {response.text}")
        return response.json()

    def get_player(self, player_tag: str) -> dict[str, Any]:
        tag = player_tag.strip("#").upper()
        return self._get(f"players/%23{tag}")

    def get_battlelog(self, player_tag: str) -> dict[str, Any]:
        tag = player_tag.strip("#").upper()
        return self._get(f"players/%23{tag}/battlelog")

    def get_top_players(self, limit: int = 200, country_code: str = "global") -> dict[str, Any]:
        return self._get(f"rankings/{country_code}/players", params={"limit": limit})

