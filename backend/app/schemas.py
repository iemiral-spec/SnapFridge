"""API istek/cevap şekilleri (Pydantic)."""
from pydantic import BaseModel, Field


class RegisterIn(BaseModel):
    email: str = Field(min_length=3, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    password: str = Field(min_length=6, max_length=128)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    is_admin: bool


class RecognitionOut(BaseModel):
    sure: list[str]
    unsure: list[str]
    demo: bool = False  # True: sahte (mock) sağlayıcı, fotoğrafa gerçekten bakılmadı


class MatchIn(BaseModel):
    ingredients: list[str] = Field(min_length=1, max_length=100)


class RecipeIngredientOut(BaseModel):
    name: str
    measure: str = ""
    label: str = ""  # tarifte yazdığı gibi; boşsa name kullanılır


class RecipeSummary(BaseModel):
    id: int
    title: str
    image_url: str | None = None


class RecipeMatch(RecipeSummary):
    matched: list[str]
    missing: list[str]
    score: float


class RecipeDetail(RecipeSummary):
    instructions: str
    source: str
    ingredients: list[RecipeIngredientOut]


class RecipeIn(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    instructions: str = ""
    image_url: str | None = None
    ingredients: list[RecipeIngredientOut] = Field(min_length=1)
