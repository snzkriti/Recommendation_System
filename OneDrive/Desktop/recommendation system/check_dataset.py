import pandas as pd
import os

df = pd.read_csv("styles.csv", on_bad_lines="skip")

print("Rows:", len(df))
print("Images:", len(os.listdir("images")))