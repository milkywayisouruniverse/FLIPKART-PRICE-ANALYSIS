import pandas as pd
from sqlalchemy import create_engine

# Paste your Neon connection string below
engine = create_engine(
    "postgresql://neondb_owner:npg_D2zYOQu3ImSb@ep-noisy-smoke-ao3q3vbh-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

df = pd.read_csv(
    "data/flipkart_com-ecommerce_sample.csv"
)

df.to_sql(
    "flipkart_products",
    engine,
    if_exists="replace",
    index=False
)

print("Upload complete!")