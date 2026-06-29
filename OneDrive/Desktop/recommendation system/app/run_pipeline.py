import subprocess

print("=" * 50)
print("CLEANUP")
print("=" * 50)

subprocess.run(
    ["python", "app/cleanup.py"],
    check=True
)

print("=" * 50)
print("STEP 1 : SAVING TRENDS")
print("=" * 50)

subprocess.run(
    ["python", "app/save_trends.py"],
    check=True
)

print("=" * 50)
print("STEP 2 : GENERATING TREND EMBEDDINGS")
print("=" * 50)

subprocess.run(
    ["python", "app/generate_trend_embeddings.py"],
    check=True
)

print("=" * 50)
print("STEP 3 : GENERATING RECOMMENDATIONS")
print("=" * 50)

subprocess.run(
    ["python", "app/recommender.py"],
    check=True
)

print("=" * 50)
print("PIPELINE COMPLETED")
print("=" * 50)