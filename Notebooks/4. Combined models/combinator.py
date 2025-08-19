import pandas as pd

def confidence_voting(paths, output_path="submission_confidence_voting.csv"):

    if len(paths) < 2:
        raise ValueError("At least two file paths must be provided.")

    # Load and merge all dataframes on 'isic_id'
    dfs = []
    for i, path in enumerate(paths):
        df = pd.read_csv(path).copy()
        df.rename(columns={'target': f'target_{i+1}'}, inplace=True)
        dfs.append(df)

    # Merge all on 'isic_id'
    merged = dfs[0]
    for df in dfs[1:]:
        merged = pd.merge(merged, df, on='isic_id')

    # Select the most confident prediction per row
    target_cols = [f'target_{i+1}' for i in range(len(paths))]
    merged['target'] = merged[target_cols].apply(
        lambda row: row.loc[row.sub(0.5).abs().idxmax()], axis=1
    )

    # Output result
    result = merged[['isic_id', 'target']]
    result.to_csv(output_path, index=False)
    print(f"Saved most confident prediction to: {output_path}")

# Aquí pones los paths de las submissions que quieras combinar
paths = [
]

confidence_voting(paths, output_path="")  # Aquí guardas