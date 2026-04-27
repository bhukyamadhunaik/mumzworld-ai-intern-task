from pydantic import BaseModel, Field
from typing import List

class ProductRecommendation(BaseModel):
    product_id: str = Field(..., description="The ID of the recommended product from the catalog.")
    product_name_en: str = Field(..., description="The name of the product in English.")
    product_name_ar: str = Field(..., description="The name of the product translated to Arabic.")
    reasoning_en: str = Field(..., description="Why this product is a great fit for the user's request (in English).")
    reasoning_ar: str = Field(..., description="Why this product is a great fit for the user's request, naturally translated to Arabic.")

class GiftFinderResponse(BaseModel):
    recommendations: List[ProductRecommendation] = Field(
        ..., 
        description="A curated shortlist of 2 to 4 recommended products based on the user's query."
    )
    summary_message_en: str = Field(
        ..., 
        description="A friendly summary message addressing the user in English."
    )
    summary_message_ar: str = Field(
        ..., 
        description="A friendly summary message addressing the user in Arabic."
    )
