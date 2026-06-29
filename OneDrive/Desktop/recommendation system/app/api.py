import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

app = FastAPI(
    title="Fashion Recommendation System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Fashion Recommendation API Running"
    }


@app.get("/recommendations")
def get_recommendations():

    recommendations = (
        supabase    
        .table("recommendations")
        .select("*")
        .execute()
    )

    return recommendations.data


@app.get("/recommendations/details")
def get_recommendation_details():

    recommendations = (
        supabase
        .table("recommendations")
        .select("*")
        .execute()
        .data
    )

    result = []

    for rec in recommendations:

        product = (
            supabase
            .table("products")
            .select("*")
            .eq("id", rec["product_id"])
            .execute()
            .data
        )

        trend = (
            supabase
            .table("trend_data")
            .select("*")
            .eq("id", rec["trend_id"])
            .execute()
            .data
        )

        if product and trend:

            result.append({
                "trend": trend[0]["keyword"],
                "product_name":
                    product[0]["product_display_name"],
                "article_type":
                    product[0]["article_type"],
                "gender":
                    product[0]["gender"],
                "similarity_score":
                    rec["similarity_score"]
            })

    return result