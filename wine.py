### SP assignment Wine

import requests as rq
import pandas as pd

df_red = pd.read_excel("./data/winequality-red.xlsx", header=1)
df_white = pd.read_excel("./data/winequality-white.xlsx", header=1)




#---------------------------------------
#Task 1 Analyze

df_red.info()
df_red.columns
df_red.head()
df_red.shape
df_red.describe()

df_white.info()
df_white.columns
df_white.head()
df_white.shape
df_white.describe()

#---------------------------------------

#---------------------------------------
#Task 2 Hypothize, expectations
# Red wine is stronger than white wine
# Red wine is more acidic than white wine (because you normally drink it with steak etc)


#---------------------------------------

#---------------------------------------
#Task 3 Data Wrangling

#Fejl i data
df_red.isna().sum()
df_white.isna().sum()

# 1. Create the identity label FIRST
df_red['wine_type'] = 'red'
df_white['wine_type'] = 'white'

# 2. Now combine them. Because they both have 'wine_type', 
# the new df_wine will have this column too!
df_wine = pd.concat([df_red, df_white], ignore_index=True)

# 3. Clean column names (replace spaces with underscores for easier coding)
df_wine.columns = [col.replace(' ', '_') for col in df_wine.columns]

# 4. Remove Duplicates
# Check how many duplicates exist
print(f"Duplicates found: {df_wine.duplicated().sum()}")

# Remove them
df_wine.drop_duplicates(inplace=True)

# How many duplicates left?
print(f"Duplicates found: {df_wine.duplicated().sum()}")

# 5. Create a new feature: 'quality_label' (Discretization)
# We categorize quality into: Low (3-4), Medium (5-6), High (7-9)
bins = [0, 4, 6, 10]
labels = ['Low', 'Medium', 'High']
df_wine['quality_label'] = pd.cut(df_wine['quality'], bins=bins, labels=labels)

# 6. Feature Engineering: Calculate 'bound_sulfur_dioxide'
df_wine['bound_sulfur_dioxide'] = df_wine['total_sulfur_dioxide'] - df_wine['free_sulfur_dioxide']

#---------------------------------------

#---------------------------------------
#Task 4 Data cleaning  (aggregate)

# 1. Confirm the balance of the two types
print("Distribution of Wine Types:")
print(df_wine['wine_type'].value_counts())


# 2. Compare the mean values of all features by wine type
# This helps you see the "chemical profile" of Red vs. White
print("\nAverage chemical properties by type:")
display(df_wine.groupby('wine_type').mean(numeric_only=True))

# 3. Specifically compare quality across the two types
print("\nQuality breakdown by type:")
print(df_wine.groupby('wine_type')['quality'].describe())

# 4. Check for correlations (optional but insightful)
# This shows which factors move together with quality
print("\nCorrelation with Quality (Overall):")
print(df_wine.corr(numeric_only=True)['quality'].sort_values(ascending=False))

#---------------------------------------


#---------------------------------------
#Task 5 - Vi laver her Data Enrichment

# I terminalen skriv: 
    # python -m pip install --upgrade pip
    # python -m pip install kagglehub

import kagglehub

# Download latest version
path = kagglehub.dataset_download("yasserh/wine-quality-dataset")
import os
print(os.listdir(path))
#After i've found my path i relocate the data to my winefolder and read
df_kaggle = pd.read_csv("./data/WineQT.csv")

#I check the differences between dataframes
print("DF1 columns:")
print(df_wine.columns)

print("\nDF2 columns:")
print(df_kaggle.columns)

#I replace punctuation
df_kaggle.columns = [col.replace(' ', '_') for col in df_kaggle.columns]
#I remove id-column (it's not important)
df_kaggle = df_kaggle.drop(columns=['Id'])
#The downloaded set is only for red_wines
df_kaggle['wine_type'] = 'red'
#I set the quality like my wine df
bins = [0, 4, 6, 10]
labels = ['Low', 'Medium', 'High']
df_kaggle['quality_label'] = pd.cut(df_kaggle['quality'], bins=bins, labels=labels)
#Im making the last row: bound sulfer dioxide:
df_kaggle['bound_sulfur_dioxide'] = df_kaggle['total_sulfur_dioxide'] - df_kaggle['free_sulfur_dioxide']
#Putting it all together:
df_all_wines = pd.concat([df_wine, df_kaggle], ignore_index=True)
#Check for duplicates: there are actually1064 - so only around 80 new wines out of 1143 added... 
duplicates = df_all_wines.duplicated().sum()
print("Number of duplicate rows:", duplicates)
#Removing duplicates:
df_all_wines = df_all_wines.drop_duplicates()
#---------------------------------------

#---------------------------------------
#Task 6 - Identificer dependent variable og indepedent variables of interest

# Dependent Variable: quality. Vi ønsker at forstå, hvad der definerer en god vin.
# Independent Variables of Interest:
    # alcohol: Typisk den stærkeste positive indikator for kvalitet.
    # volatile_acidity: Ofte en stærk negativ indikator (høj syre = lavere kvalitet/vineddike-smag).
    # wine_type: Fordi profilen for rød og hvid er markant forskellig.

    # density: Hænger ofte sammen med sukker og alkohol.
#---------------------------------------

### Data Exploration and analysis
#---------------------------------------
#---------------------------------------
#Task 7 - Normalfordeling og sammenligning

# Statistisk sammenligning af de tre datasæt
# Vi kigger på 'alcohol', da det er en god indikator for forskelle
stats_comparison = pd.DataFrame({'Red': df_red['alcohol'].describe(),'White': df_white['alcohol'].describe(),'All': df_all_wines['alcohol'].describe()})
print(stats_comparison)

# Skævhed
print(df_all_wines.skew(numeric_only=True).sort_values())

# Histogram
df_all_wines.hist(column='alcohol', by='wine_type', bins=20, figsize=(10, 4))

# Boxplot
# Vi laver ét for hver type af vin
df_all_wines[df_all_wines['wine_type'] == 'red'].plot(kind='box', y='residual_sugar', title='Red Wine Sugar')
df_all_wines[df_all_wines['wine_type'] == 'white'].plot(kind='box', y='residual_sugar', title='White Wine Sugar')

# Scatterplot
# Her tester vi f.eks. sammenhængen mellem alkohol og sukker
df_all_wines.plot.scatter(x='alcohol', y='residual_sugar', c='DarkBlue', title='Sugar vs Alcohol')
#---------------------------------------

#---------------------------------------
#Task 8 - Oprydning (Outlier removal)
#---------------------------------------

# Vi finder en grænseværdi (quantile). 
# Her vil vi gerne have at sugar_cutoff er den værdi som 99% af vinene ligger under. Altså vi fjerner ekstreme tilfælde
sugar_cutoff = df_all_wines['residual_sugar'].quantile(0.99)
print(f"99% af alle vine har under {sugar_cutoff} g/L sukker.")

# Vi laver et clean dataframe uden ekstreme outliers
df_clean = df_all_wines[df_all_wines['residual_sugar'] < sugar_cutoff]

# Tjekker om statistikken er forbedret 
print("Skævhed FØR fjernelse af outliers:")
print(df_all_wines['residual_sugar'].skew())

print("Skævhed EFTER fjernelse af outliers:")
print(df_clean['residual_sugar'].skew())

# Visuel sammenligning (Histogram)
# Vi plotter det nye 'rene' data for at se om det ligner en klokkekurve mere nu
df_clean.hist(column='residual_sugar', bins=20, figsize=(10, 4))

# Vi kan her se, at langt størstedelen af vine er "Tørre" og har derfor et Right Skew stadig, men det er langt mere læsbart.


#---------------------------------------
#Task 9 - Visualisering og analyse

# Hvilken vintype har højere gennemsnitlig kvalitet?
# Bar-graf. Det ligner at kvaliteten er en lille smule bedre i hvidvin, men meget ens.
df_all_wines.groupby('wine_type')['quality'].mean().plot(kind='bar', title='Average Quality by Wine Type')

# Hvilken type har højere gennemsnitligt alkoholniveau?
# Hvidvin har et højere gennemsnitligt alkoholniveau. Den grønne streg i midten af boksen er højere oppe end rød.
df_all_wines.plot(kind='box', column='alcohol', by='wine_type', title='Alcohol Level by Wine Type')

# Hvilken type har højere gennemsnitlig mængde restsukker?
# Hvidvin har et højere gennemsnitligt mængde restsukker. Faktisk enormt stor forskel her.
df_all_wines.plot(kind='box', column='residual_sugar', by='wine_type', title='Residual Sugar by Wine Type')

# Påvirker alkohol og sukker kvaliteten?
# Alkohol vs Kvalitet = Det ligner at ml. 11-13% alkohol er der størst gennemsnitlig kvalitet
df_all_wines.plot.scatter(x='alcohol', y='quality', title='Alcohol vs Quality', alpha=0.5)
# Sukker vs Kvalitet = Det ligner at for meget sukker påvirker kvaliteten. I den lave ende af restsukker er der højest kval.
df_all_wines.plot.scatter(x='residual_sugar', y='quality', title='Sugar vs Quality', alpha=0.5)

#---------------------------------------

#---------------------------------------
#Task 10 - Binning pH

# Splitter data i 5 subsets (bins) baseret på pH
df_all_wines['pH_bin_5'] = pd.cut(df_all_wines['pH'], bins=5)

# Find gennemsnitlig density for hvert subset
print("Gennemsnitlig Density for 5 pH-subsets:")
density_5 = df_all_wines.groupby('pH_bin_5', observed=True)['density'].mean()
print(density_5)

# Splitter data i 10 subsets (bins) baseret på pH (samme som jeg gjorde lige før, bare 10)
df_all_wines['pH_bin_10'] = pd.cut(df_all_wines['pH'], bins=10)

print("Gennemsnitlig Density for 10 pH-subsets:")
density_10 = df_all_wines.groupby('pH_bin_10', observed=True)['density'].mean()
print(density_10)

# Visualisering for at se mønstret (valgfrit men hjælper på analysen)
density_10.plot(kind='bar', title='Density vs pH Bins (10 subsets)')
#---------------------------------------

#---------------------------------------
#Task 11 - Discussion

# Svært at skrive meget her, men konklusionen på vores diskussion var, at det havde været fedt at have pris el. oprindelsesland
# i datasættet. Så kunne man konkludere yderligere for vinproducenter og lign. hvad forbrugermønstrene er osv.
# Det ville også gøre at man kunne se sammenhæng ml. kvalitet og salg, så distributører kunne købe flere vin ind med høj kvalitet.
#---------------------------------------

#---------------------------------------
# Task 12 - Korrelationsmatrix og Heatmap
import seaborn as sns
import matplotlib.pyplot as plt

# Beregner korrelation 
# Vi fjerner 'quality_label' da den ikke er numerisk, og fokuserer på de vigtigste
cols_to_show = ['alcohol', 'density', 'volatile_acidity', 'residual_sugar', 'ph', 'total_sulfur_dioxide', 'chlorides', 'quality']

# Vi sikrer os at vi kun tager de kolonner der rent faktisk findes i vores dataframe
existing_cols = [c for c in cols_to_show if c in df_all_wines.columns]
corr_matrix = df_all_wines[existing_cols].corr()

# Laver Heatmap
plt.figure(figsize=(10, 8))
plot = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plot.set_title('Correlation Heatmap (Simplified)')
plt.show()

# Finder topscorerne i konsollen
corrs_with_quality = corr_matrix['quality'].sort_values(ascending=False)
print("\nSammenhæng med kvalitet:")
print(corrs_with_quality)

# Alkoholen er den vigtigste faktor for vinens kvalitet
# Sukker er den vigtigste faktor for density 
#---------------------------------------

#---------------------------------------
# Task 13 - Feature Selection (Oprydning)

# Definerer hvilke kolonner vi vil beholde
# Vi beholder de vigtigste kemiske træk og selvfølgelig kvaliteten
cols_to_keep = ['alcohol', 'volatile_acidity', 'chlorides', 'pH', 'free_sulfur_dioxide', 'quality']

# Laver det endelige, rene datasæt
df_final = df_all_wines[cols_to_keep].copy()

# Bekræfter resultatet
print("Endelige attributter valgt til analyse:")
print(df_final.columns.tolist())

# Det endelige, nye, simple heatmap (Altså jeg har beholdt de vigtigste columns)
plt.figure(figsize=(8, 6))
sns.heatmap(df_final.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Final Cleaned Correlation Matrix')
plt.show()
#---------------------------------------

#---------------------------------------
# Task 14 - Scaling og Normalisering

from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# Vi vælger en kolonne med tydelige outliers til testen, f.eks. 'alcohol'
data_to_scale = df_final[['alcohol']]

# Min-Max Scaling (Normalisering)
minmax = MinMaxScaler()
df_final['alcohol_minmax'] = minmax.fit_transform(data_to_scale)

# Standardization (Z-score scaling)
std_scaler = StandardScaler()
df_final['alcohol_std'] = std_scaler.fit_transform(data_to_scale)

# Robust Scaling (God mod outliers)
robust = RobustScaler()
df_final['alcohol_robust'] = robust.fit_transform(data_to_scale)

# 4. Sammenlign effekten
print("Statistik efter forskellige scalers:")
print(df_final[['alcohol', 'alcohol_minmax', 'alcohol_std', 'alcohol_robust']].describe())

# Visuel sammenligning med boxplots
df_final[['alcohol_minmax', 'alcohol_std', 'alcohol_robust']].plot(kind='box', figsize=(10,6), title='Comparison of Scalers')


#---------------------------------------
# Task 15 - Statistisk Hypotesetest

from scipy import stats

# Opdeler kvalitetsscorerne i to grupper
red_quality = df_all_wines[df_all_wines['wine_type'] == 'red']['quality']
white_quality = df_all_wines[df_all_wines['wine_type'] == 'white']['quality']

# Udfører en uafhængig t-test
t_stat, p_value = stats.ttest_ind(red_quality, white_quality)

# Beregner gennemsnit og standardafvigelse
print(f"Gennemsnitlig kvalitet (Rød): {red_quality.mean():.4f}")
print(f"Gennemsnitlig kvalitet (Hvid): {white_quality.mean():.4f}")
print(f"T-statistik: {t_stat:.4f}")
print(f"P-værdi: {p_value:.4e}")
#---------------------------------------
#---------------------------------------
#Task 16 - Final summary 

"Mine hypoteser i task 2 blev begge udfordret af dataanalysen. Jeg forventede, at rødvin ville være både stærkere og mere syreholdig. 
"Analysen viste dog det modsatte: hvidvinene i dette datasæt havde generelt et højere alkoholindhold og en lavere pH-værdi (hvilket betyder højere syreindhold).
"Dette understreger vigtigheden af Exploratory Data Analysis (EDA); vores mavefornemmelse om et produkt stemmer ikke altid overens med de kemiske realiteter. 
"For en forretning betyder det, at man ikke kan markedsføre rødvin udelukkende på at være 'kraftigere', da data viser, at hvidvin ofte besidder de samme eller stærkere kemiske egenskaber."
#---------------------------------------
#---------------------------------------
#Task
#---------------------------------------