import pandas as pd
import os

df = pd.read_csv("styles.csv", on_bad_lines="skip")

existing_images = {
    int(file.split(".")[0])
    for file in os.listdir("images")
    if file.endswith(".jpg")
}

df = df[df["id"].isin(existing_images)]

df = df.dropna(subset=["productDisplayName"])

print("Original Rows:", len(pd.read_csv("styles.csv", on_bad_lines="skip")))
print("Cleaned Rows:", len(df))

df.to_csv("cleaned_styles.csv", index=False)

print("Saved cleaned_styles.csv")