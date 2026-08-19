import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configuração estética global para os gráficos
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["font.size"] = 10

# ==============================================================================
# 0. CARREGAMENTO E PRÉ-PROCESSAMENTO DOS DADOS
# ==============================================================================
df = pd.read_csv("netflix_titles.csv")

# Converter 'date_added' para formato datetime e extrair o ano de adição
df["date_added_clean"] = pd.to_datetime(
    df["date_added"].str.strip(), format="%B %d, %Y", errors="coerce"
)
df["year_added"] = df["date_added_clean"].dt.year

# Tratar coluna 'duration' separando Filmes (minutos) e Séries (temporadas)
movies_mask = df["type"] == "Movie"
tv_mask = df["type"] == "TV Show"

df["duration_num"] = np.nan
df.loc[movies_mask, "duration_num"] = (
    df.loc[movies_mask, "duration"]
    .str.replace(" min", "", regex=False)
    .astype(float)
)
df.loc[tv_mask, "duration_num"] = (
    df.loc[tv_mask, "duration"]
    .str.replace(" Seasons", "", regex=False)
    .str.replace(" Season", "", regex=False)
    .astype(float)
)


# ==============================================================================
# 1. PROPORÇÃO ENTRE FILMES E SÉRIES DE TV
# ==============================================================================
type_counts = df["type"].value_counts()
print("--- Q1: Proporção Filmes vs. Séries ---")
print(type_counts)
print(
    f"Porcentagem de Filmes: {(type_counts['Movie'] / len(df)) * 100:.2f}%\n"
)

plt.figure(figsize=(6, 6))
plt.pie(
    type_counts,
    labels=type_counts.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=["#e50914", "#221f1f"],
    explode=(0.05, 0),
)
plt.title("Proporção de Filmes x Séries de TV no Catálogo")
plt.show()


# ==============================================================================
# 2. TOP 10 PAÍSES PRODUTORES
# ==============================================================================
# Múltiplos países são separados por vírgula na mesma célula
countries_series = (
    df["country"].dropna().str.split(", ").explode().str.strip()
)
top_countries = countries_series.value_counts().head(10)

print("--- Q2: Top 10 Países Produtores ---")
print(top_countries)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=top_countries.values, y=top_countries.index, hue=top_countries.index, palette="viridis", legend=False
)
plt.title("Top 10 Países com Mais Conteúdos no Catálogo")
plt.xlabel("Quantidade de Títulos")
plt.ylabel("País")
plt.show()


# ==============================================================================
# 3. EVOLUÇÃO TEMPORAL DE ADIÇÕES AO CATÁLOGO
# ==============================================================================
additions_per_year = (
    df["year_added"].value_counts().sort_index().loc[lambda x: x.index >= 2010]
)

print("--- Q3: Títulos Adicionados por Ano ---")
print(additions_per_year)

plt.figure(figsize=(10, 5))
sns.lineplot(
    x=additions_per_year.index.astype(int),
    y=additions_per_year.values,
    marker="o",
    color="#e50914",
    linewidth=2.5,
)
plt.title("Evolução Anual de Adição de Títulos (2010 - 2021)")
plt.xlabel("Ano de Adição")
plt.ylabel("Quantidade de Títulos Adicionados")
plt.xticks(additions_per_year.index.astype(int))
plt.show()


# ==============================================================================
# 4. TEMPO MÉDIO ENTRE LANÇAMENTO ORIGINAL E ENTRADA NA PLATAFORMA
# ==============================================================================
df["years_to_add"] = df["year_added"] - df["release_year"]
# Remover inconsistências onde a data de adição foi anterior ao lançamento
valid_diff = df[df["years_to_add"] >= 0]["years_to_add"]

mean_diff = np.mean(valid_diff)
median_diff = np.median(valid_diff)

print("--- Q4: Intervalo Lançamento vs. Entrada na Plataforma ---")
print(f"Tempo médio decorrido: {mean_diff:.2f} anos")
print(f"Mediana do tempo decorrido: {median_diff:.2f} anos")

plt.figure(figsize=(10, 5))
sns.histplot(valid_diff, bins=30, kde=True, color="darkslateblue")
plt.axvline(
    mean_diff,
    color="red",
    linestyle="--",
    label=f"Média ({mean_diff:.1f} anos)",
)
plt.axvline(
    median_diff,
    color="green",
    linestyle="-",
    label=f"Mediana ({median_diff:.1f} anos)",
)
plt.xlim(0, 40)
plt.title(
    "Distribuição do Tempo Decorrido entre Lançamento e Entrada na Plataforma"
)
plt.xlabel("Anos de Diferença")
plt.ylabel("Quantidade de Títulos")
plt.legend()
plt.show()


# ==============================================================================
# 5. GÊNEROS MAIS FREQUENTES POR TIPO DE CONTEÚDO
# ==============================================================================
df_genres = df.assign(
    genre=df["listed_in"].str.split(", ")
).explode("genre")
top_genres = (
    df_genres.groupby(["genre", "type"])
    .size()
    .unstack(fill_value=0)
    .assign(Total=lambda x: x.sum(axis=1))
    .sort_values(by="Total", ascending=False)
    .head(10)
)

print("--- Q5: Top 10 Gêneros por Tipo ---")
print(top_genres)

top_genres[["Movie", "TV Show"]].plot(
    kind="barh", stacked=True, color=["#e50914", "#333333"], figsize=(10, 6)
)
plt.title("Top 10 Gêneros Mais Frequentes (Divididos por Filmes e Séries)")
plt.xlabel("Quantidade de Títulos")
plt.ylabel("Gênero")
plt.gca().invert_yaxis()
plt.legend(["Filmes", "Séries"])
plt.show()


# ==============================================================================
# 6. DISTRIBUIÇÃO DAS CLASSIFICAÇÕES INDICATIVAS (RATING)
# ==============================================================================
# Filtrar possíveis entradas incorretas/ruídos na coluna rating (ex: durações)
valid_ratings = df[
    df["rating"].str.contains("min|Season", na=False) == False
]["rating"]
rating_counts = valid_ratings.value_counts()

print("--- Q6: Classificação Indicativa ---")
print(rating_counts)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=rating_counts.index, y=rating_counts.values, hue=rating_counts.index, palette="mako", legend=False
)
plt.title("Distribuição dos Títulos por Classificação Indicativa (Rating)")
plt.xlabel("Classificação Indicativa")
plt.ylabel("Quantidade de Títulos")
plt.xticks(rotation=45)
plt.show()


# ==============================================================================
# 7. DURAÇÃO MÉDIA DOS FILMES E SUA EVOLUÇÃO TEMPORAL
# ==============================================================================
movies_df = df[df["type"] == "Movie"].dropna(subset=["duration_num"])
avg_movie_duration = movies_df["duration_num"].mean()

print("--- Q7: Duração dos Filmes ---")
print(f"Duração média geral dos filmes: {avg_movie_duration:.2f} minutos")

# Tendência ao longo das décadas (a partir de 1960)
duration_by_year = (
    movies_df[movies_df["release_year"] >= 1960]
    .groupby("release_year")["duration_num"]
    .mean()
)

plt.figure(figsize=(11, 5))
sns.lineplot(
    x=duration_by_year.index,
    y=duration_by_year.values,
    color="darkred",
    linewidth=1.8,
)
plt.axhline(
    avg_movie_duration,
    color="gray",
    linestyle="--",
    label=f"Média Geral ({avg_movie_duration:.1f} min)",
)
plt.title("Evolução da Duração Média dos Filmes por Ano de Lançamento (1960-2021)")
plt.xlabel("Ano de Lançamento")
plt.ylabel("Duração Média (minutos)")
plt.legend()
plt.show()


# ==============================================================================
# 8. MÉDIA E DISTRIBUIÇÃO DE TEMPORADAS NAS SÉRIES DE TV
# ==============================================================================
tv_df = df[df["type"] == "TV Show"].dropna(subset=["duration_num"])
avg_seasons = tv_df["duration_num"].mean()
seasons_dist = tv_df["duration_num"].value_counts().sort_index()

print("--- Q8: Número de Temporadas de Séries ---")
print(f"Média de temporadas por série: {avg_seasons:.2f}")
print("\nDistribuição de temporadas:\n", seasons_dist.head(5))

plt.figure(figsize=(8, 5))
sns.countplot(data=tv_df, x="duration_num", hue="duration_num", palette="crest", legend=False)
plt.title("Distribuição do Número de Temporadas por Série de TV")
plt.xlabel("Número de Temporadas")
plt.ylabel("Quantidade de Séries")
plt.xlim(-0.5, 9.5)  # Foco visual até 10 temporadas
plt.show()


# ==============================================================================
# 9. DIRETORES COM MAIOR NÚMERO DE TÍTULOS
# ==============================================================================
directors = (
    df["director"].dropna().str.split(", ").explode().str.strip()
)
top_directors = directors.value_counts().head(10)

print("--- Q9: Top 10 Diretores ---")
print(top_directors)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=top_directors.values, y=top_directors.index, hue=top_directors.index, palette="magma", legend=False
)
plt.title("Top 10 Diretores com Mais Títulos no Catálogo")
plt.xlabel("Número de Títulos")
plt.ylabel("Diretor")
plt.show()


# ==============================================================================
# 10. COMBINAÇÕES MAIS COMUNS EM COPRODUÇÕES INTERNACIONAIS
# ==============================================================================
coproductions = df["country"].dropna()[df["country"].dropna().str.contains(",")]
top_coproductions = coproductions.value_counts().head(10)

print("--- Q10: Top 10 Coproduções Internacionais ---")
print(top_coproductions)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=top_coproductions.values,
    y=top_coproductions.index,
    hue=top_coproductions.index,
    palette="rocket",
    legend=False,
)
plt.title("Top 10 Parcerias/Coproduções Internacionais Mais Frequentes")
plt.xlabel("Quantidade de Títulos Produzidos em Parceria")
plt.ylabel("Parceria de Países")
plt.show()