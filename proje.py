import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import mode
from scipy.stats import ttest_ind, chi2_contingency, f_oneway

# List of country codes (196)
country_codes = [
    "ABW", "AFG", "AGO", "ALB", "ARE", "ARG", "ARM", "ATG", "AUS", "AUT",
    "AZE", "BDI", "BEL", "BEN", "BFA", "BGD", "BGR", "BHR", "BHS", "BIH",
    "BLR", "BLZ", "BOL", "BRA", "BRB", "BRN", "BTN", "BWA", "CAF", "CAN",
    "CHE", "CHL", "CHN", "CIV", "CMR", "COD", "COG", "COL", "COM", "CPV",
    "CRI", "CYP", "CZE", "DEU", "DJI", "DMA", "DNK", "DOM", "DZA", "ECU",
    "EGY", "ERI", "ESP", "EST", "ETH", "FIN", "FJI", "FRA", "FSM", "GAB",
    "GBR", "GEO", "GHA", "GIN", "GMB", "GNB", "GNQ", "GRC", "GRD", "GTM",
    "GUY", "HKG", "HND", "HRV", "HTI", "HUN", "IDN", "IND", "IRL", "IRN",
    "IRQ", "ISL", "ISR", "ITA", "JAM", "JOR", "JPN", "KAZ", "KEN", "KGZ",
    "KHM", "KIR", "KNA", "KOR", "KWT", "LAO", "LBN", "LBR", "LBY", "LCA",
    "LKA", "LSO", "LTU", "LUX", "LVA", "MAC", "MAR", "MDA", "MDG", "MDV",
    "MEX", "MHL", "MKD", "MLI", "MLT", "MMR", "MNE", "MNG", "MOZ", "MRT",
    "MUS", "MWI", "MYS", "NAM", "NER", "NGA", "NIC", "NLD", "NOR", "NPL",
    "NRU", "NZL", "OMN", "PAK", "PAN", "PER", "PHL", "PLW", "PNG", "POL",
    "PRI", "PRT", "PRY", "QAT", "ROU", "RUS", "RWA", "SAU", "SDN", "SEN",
    "SGP", "SLB", "SLE", "SLV", "SMR", "SOM", "SRB", "STP", "SUR", "SVK",
    "SVN", "SWE", "SWZ", "SYC", "SYR", "TCD", "TGO", "THA", "TJK", "TKM",
    "TLS", "TON", "TTO", "TUN", "TUR", "TUV", "TWN", "TZA", "UGA", "UKR",
    "URY", "USA", "UZB", "VCT", "VEN", "VNM", "VUT", "WBG", "WSM", "YEM",
    "ZAF", "ZMB", "ZWE", "SSD", "AND", "UVK"
]

base_url = 'https://www.imf.org/external/datamapper/api/v1/PCPIPCH/'

all_data = []

response = requests.get(base_url)

if response.status_code == 200:
    data = response.json()
    for country in country_codes:
            if 'values' in data and 'PCPIPCH' in data['values'] and country in data['values']['PCPIPCH']:
                cpi_data = data['values']['PCPIPCH'][country]
                df = pd.DataFrame(list(cpi_data.items()), columns=['Yıl', 'TÜFE'])
                df['Yıl'] = pd.to_numeric(df['Yıl'])
                df['Ülke'] = country
                all_data.append(df)
            else:
                print(f"{country} için TÜFE verisi bulunamadı.")
else:
    print("Veri alınamadı: {response.status_code}")

# Combine all data into a single DataFrame
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)

    # Plot for Turkey with standard deviation line
    plt.figure(figsize=(10, 6))
    turkey_data = combined_df[combined_df['Ülke'] == 'TUR']
    sns.lineplot(data=turkey_data, x='Yıl', y='TÜFE', color='blue', label='Türkiye TÜFE')
    plt.title('Türkiye Tüketici Fiyat Endeksi ve tahminleri')
    plt.xlabel('Yıl')
    plt.ylabel('TÜFE')

    # Calculate standard deviation of Turkey's CPI and plot it
    std_turkey_cpi = turkey_data['TÜFE'].std()
    plt.axhline(std_turkey_cpi, color='green', linestyle='--', label='Standart Sapma TÜFE')

    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    # Plot for Other Countries (average CPI)
    plt.figure(figsize=(10, 6))
    other_countries = combined_df[combined_df['Ülke'] != 'TUR']
    aggregated_cpi = other_countries.groupby('Yıl')['TÜFE'].mean().reset_index()
    sns.lineplot(data=aggregated_cpi, x='Yıl', y='TÜFE', color='orange')
    plt.title('Diğer Ülkeler için Ortalama Tüketici Fiyat Endeksi ve tahminleri')
    plt.xlabel('Yıl')
    plt.ylabel('Ortalama TÜFE')
    plt.xticks(rotation=45)
    plt.show()

    # Plot for Median CPI of all countries, with Turkey in a different color
    plt.figure(figsize=(10, 6))
    median_cpi = combined_df.groupby('Ülke')['TÜFE'].median().reset_index()

    # Define colors: set 'red' for Turkey and 'blue' for other countries
    colors = ['red' if country == 'TUR' else 'blue' for country in median_cpi['Ülke']]

    # Plotting the bar plot with customized colors
    sns.barplot(data=median_cpi, x='Ülke', y='TÜFE', palette=colors)
    plt.title('Tüm Ülkelerin Medyan Tüketici Fiyat Endeksi')
    plt.xlabel('Ülke')
    plt.ylabel('Medyan TÜFE')
    plt.xticks([], rotation=0)  # Hide x-tick labels to keep the plot cleaner
    plt.show()

    # Calculate the mean for Turkey's CPI specifically for the pie chart
    mean_turkey_cpi = turkey_data['TÜFE'].mean()
    average_world_cpi = other_countries['TÜFE'].mean()

    # Average CPI Pie Chart
    plt.figure(figsize=(6, 6))
    pie_data = pd.Series([mean_turkey_cpi, average_world_cpi], index=['Türkiye', 'Diğer Ülkeler'])
    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
    plt.title('Ortalama Tüketici Fiyat Endeksi')
    plt.show()

    # Mode CPI for each country in a bar plot with Turkey highlighted
    plt.figure(figsize=(12, 6))
    mode_cpi = combined_df.groupby('Ülke')['TÜFE'].apply(lambda x: mode(x) if len(x) > 0 else None).reset_index()
    colors = ['red' if x == 'TUR' else 'blue' for x in mode_cpi['Ülke']]
    sns.barplot(data=mode_cpi, x='Ülke', y='TÜFE', palette=colors)
    plt.title('Her Ülke İçin Tüketici Fiyat Endeksinin (Mod)')
    plt.xlabel('Ülke')
    plt.ylabel('Mod TÜFE')
    plt.xticks([], rotation=0)  # Hide x-tick labels
    plt.show()

    # T-test function
    def perform_t_test(data):
        turkey_cpi = data[data['Ülke'] == 'TUR']['TÜFE']
        other_countries_cpi = data[data['Ülke'] != 'TUR']['TÜFE']
        t_stat, p_value = ttest_ind(turkey_cpi, other_countries_cpi, equal_var=False)
        print(f"T-test: t-statistic = {t_stat:.4f}, p-value = {p_value:.4f}")
        if p_value < 0.05:
            print("Türkiye ile diğer ülkeler arasında anlamlı fark var.")
        else:
            print("Türkiye ile diğer ülkeler arasında anlamlı fark yok.")

    # Chi-squared test function
    def perform_chi_squared_test(data):
        contingency_table = pd.crosstab(data['Yıl'], data['Ülke'] == 'TUR')
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        print(f"Chi-squared test: chi2 = {chi2:.4f}, p-value = {p_value:.4f}")
        if p_value < 0.05:
            print("Yıllar ile ülke gruplandırması arasında anlamlı ilişki var.")
        else:
            print("Yıllar ile ülke gruplandırması arasında anlamlı ilişki yok.No significant association between years and country grouping.")

        
    # Call the new functions to display test results
    perform_t_test(combined_df)
    perform_chi_squared_test(combined_df)

else:
    print("Görselleştirme için veri bulunmamaktadır.")
