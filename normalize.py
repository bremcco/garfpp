import pandas as pd

# Load your CSV (assuming it's in a file called 'data.csv')
df = pd.read_csv('arco28020.csv')

# Normalize each column by 'total'
columns_to_normalize = ['attachment1', 'attachment2', 'diffusion1', 'diffusion2']
for col in columns_to_normalize:
    df[col + '_norm'] = df[col] / df['total']

# View the resulting DataFrame
print(df.head())

# Optional: Save to a new CSV
df.to_csv('arco28020.csv', index=False)