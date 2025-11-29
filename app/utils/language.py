"""Language service for loading and accessing translations."""

import functools
from pathlib import Path

import yaml


class LanguageService:
    """
    Loads all language YAML files from a directory and provides
    a way to get a translator object for a specific language.
    """

    def __init__(self, directory: str | Path):
        self._languages = {}
        self._load_languages(directory)

    def _load_languages(self, directory: str | Path):
        """Loads all .yml files from the given directory."""
        path = Path(directory)
        for file_path in path.glob("*.yml"):
            lang_code = file_path.stem
            with open(file_path, encoding="utf-8") as f:
                self._languages[lang_code] = yaml.safe_load(f)

    def get_translator(self, language: str = "en"):
        """
        Gets a Translator instance for the requested language.
        Defaults to English if the requested language is not found.
        """
        if language not in self._languages:
            language = "en"  # Fallback to English

        return Translator(
            strings=self._languages.get(language, {}),
            fallback_strings=self._languages.get("en", {}),
        )


class Translator:
    """
    Provides a simple interface to get translated strings, with a fallback.
    """

    def __init__(self, strings: dict, fallback_strings: dict):
        self._strings = strings
        self._fallback_strings = fallback_strings

    def get(self, key: str) -> str:
        """
        Gets a string for a given key.

        Tries the primary language first, then falls back to English,
        and finally to the key itself.
        """
        return self._strings.get(key) or self._fallback_strings.get(key, key)


@functools.lru_cache(maxsize=1)
def get_language_service() -> LanguageService:
    """Returns the singleton instance of the LanguageService."""
    i18n_dir = Path(__file__).parent.parent / "localization" / "i18n"
    language_service_instance = LanguageService(i18n_dir)

    return language_service_instance
