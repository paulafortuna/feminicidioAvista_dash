import spacy
import pandas as pd

#nlp = spacy.load('pt_core_news_lg')

# read data
df = pd.read_csv('./data/annotated_data.tsv', sep='\t')

# crimes per year
df['arquivo_date'] = pd.to_datetime(df.arquivo_date, errors='coerce')
df_crimes = df[df['annotated_data'] == 'y']
df_crimes['dateyear'] = df_crimes['arquivo_date'].dt.year
res = pd.DataFrame(df_crimes.groupby(['dateyear']).size())
res['year'] = res.index
res.to_csv('./data/crimes_per_year.tsv',sep='\t',index=False)

# table news per year

for year in res['year']:
    df_crimes_sub = df_crimes[df_crimes['dateyear'] == year]
    df_crimes_sub[['news_site_title','search_newspaper']].to_csv('./data/table_crimes_year_' + str(year) +'.tsv',sep='\t',index=False)