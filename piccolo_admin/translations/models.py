import typing as t

from pydantic import BaseModel, Field


class TranslationListItem(BaseModel):
    language_name: str = Field(description="e.g. 'English'")
    language_code: str = Field(description="e.g. 'en'")


class TranslationListResponse(BaseModel):
    translations: t.List[TranslationListItem]
    default_language_code: str = Field(description="e.g. 'en'")


class Translation(BaseModel):
    """
    :param language_name:
        A human readable representation of the language. For example 'English'.
    :param language_code:
        The IETF language tag. For English it is 'en'. However, it also allows
        us to specify dialects like 'en-US' for American English, or 'en-GB'
        for British English, should we need it in the future.
    """

    language_name: str
    language_code: str
    translations: t.Dict[str, str]
