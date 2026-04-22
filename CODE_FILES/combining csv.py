import pandas

df1 = pandas.read_csv("EDITED_CSV_FILES\Massey_XG.csv")
df2 = pandas.read_csv("EDITED_CSV_FILES\Perron-Frobenius.csv")
df3 = pandas.read_csv("EDITED_CSV_FILES\Massey_G.csv")
df4 = pandas.read_csv("EDITED_CSV_FILES\Actual_Points.csv", encoding="latin1")
merged_df = pandas.merge(df1, df2, on='Team', how='left')
merged_df = pandas.merge(merged_df, df3, on='Team', how='left')
merged_df = pandas.merge(merged_df, df4, on='Team', how='left')

print(merged_df)

merged_df.to_csv("EDITED_CSV_FILES\combined_ratings_3.csv", index=False)
