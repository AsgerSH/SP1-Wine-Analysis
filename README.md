# Wine Quality Analysis – Business Intelligence Project

## Project Overview
Dette projekt analyserer kemiske egenskaber ved rød- og hvidvin for at forstå, hvad der driver den oplevede kvalitet. Formålet var at gennemgå hele data science-processen: fra rå data-integration og rensning til statistisk hypotesetestning og forretningsindsigt.

## Data Sources
Analysen er baseret på to datasæt (rød og hvid), der er aggregeret til ét samlet korpus. Datasættet indeholder 12 numeriske variabler, herunder:
* Fixed & Volatile Acidity
* Residual Sugar
* Chlorides
* Sulfur Dioxide levels
* Density, pH & Alcohol
* **Quality Score** (Target variabel)

## Initial Hypotheses (Task 2)
Inden analysen startede, blev følgende hypoteser opstillet baseret på almindelige antagelser:
1.  **Styrke:** Rødvin er "stærkere" (højere alkoholindhold) end hvidvin.
2.  **Syre:** Rødvin er mere syreholdig end hvidvin (baseret på antagelsen om, at rødvin ofte parres med tung mad som steak).

## Data Preparation & Cleaning
For at sikre valide resultater blev følgende trin udført:
* **Aggregering:** Sammenfletning af rød- og hvidvins-data.
* **Outlier Management:** Identificering af outliers via skewness-målinger (f.eks. i `residual_sugar`), som blev filtreret for at undgå skævvridning af gennemsnit.
* **Feature Engineering:** Oprettelse af `quality_label` og beregning af `bound_sulfur_dioxide`.
* **Binning:** Opdeling af data i subsets (bins) baseret på pH for at undersøge trends i `density`.

## Exploratory Data Analysis (EDA)
De vigtigste fund fra den visuelle analyse:
* **Modbevisning af hypoteser:** Data viste overraskende, at hvidvin i dette datasæt generelt har en højere alkoholprocent og en lavere pH (hvilket betyder **højere** syreindhold) end rødvin.
* **Korrelationsanalyse:** Ved brug af et varmekort (Heatmap) blev det identificeret, at **Alcohol** har den stærkeste positive sammenhæng med kvalitet, mens **Volatile Acidity** har den stærkeste negative sammenhæng.
* **Multikollinearitet:** `Density` viste sig at være ekstremt korreleret med både sukker og alkohol, hvilket gjorde den redundant for videre modellering.

## Statistical Testing (Task 15)
For at validere forskellen mellem vintyperne blev der udført en **T-test**:
* **Resultat:** P-værdien var signifikant lav, hvilket betød, at vi kunne forkaste nulhypotesen ($H_0$).
* **Konklusion:** Der er en statistisk signifikant forskel på kvaliteten af de to vintyper, hvor hvidvinene i dette specifikke datasæt scorede marginalt højere i gennemsnit.

## Scaling & Normalization (Task 14)
Tre metoder blev sammenlignet for at håndtere variablernes forskellige skalaer:
1.  **Min-Max Scaling:** Nyttig til at få alt mellem 0 og 1, men sårbar over for outliers.
2.  **Standardization (Z-score):** God til normalfordelte data.
3.  **Robust Scaling:** Den mest effektive metode for dette datasæt, da den bruger median og IQR, hvilket sikrer, at outliers (f.eks. ekstreme sukker-niveauer) ikke ødelægger skalaen for resten af dataene.

## Business Insights & Conclusions
Baseret på dataene kan følgende anbefalinger gives til vinproducenter og distributører:
* **Kvalitetskontrol:** Producenter bør fokusere på at kontrollere **volatile acidity**, da selv små stigninger her korrelerer med et markant fald i kvalitetsscoren.
* **Markedsføring:** Distributører kan udfordre myten om, at rødvin er "kraftigere" end hvidvin, da data viser, at hvidvin ofte besidder højere alkohol- og syreniveauer.
* **Optimering:** Ved at fjerne redundante variabler som `density` og `total_sulfur_dioxide`, kan man skabe simplere og mere præcise modeller til at forudsige vinkvalitet før salg.

## Technologies Used
* **Python** (Pandas, NumPy)
* **Visualisering:** Matplotlib, Seaborn
* **Statistik:** SciPy (Stats)
* **Preprocessing:** Scikit-learn (Scalers)

**Author:** Asger Storgaard Høffner
