from typing import List
from pydantic import BaseModel

class Ingredient(BaseModel):
    ingredient: str
    justify: str

class IngredientsResponse(BaseModel):
    book: str
    ingredients: List[Ingredient]

class IngredientsRecipe(BaseModel):
    ingredient: str
    amount: str

class Recipe(BaseModel):
    title_recipe: str
    ingredients: List[IngredientsRecipe]
    preperation_time: str
    cook_time: str
    difficulty: str
    recipe: str
    instructions: str
    book: str
    justify: List[Ingredient]

class BookRecipes(BaseModel):
    recipes: List[Recipe]

class ResponseRecipe(BaseModel):
    title_recipe: str
    ingredients: str
    preperation_time: str
    cook_time: str
    difficulty: str
    recipe: str
    instructions: str
    justify: str

class Response(BaseModel):
    book: str
    recipes: List[ResponseRecipe]
