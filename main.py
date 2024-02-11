# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as mt

# Načtení dat z Excel souboru
data_path = 'data/klementinum.xlsx'  # Upravte cestu k vašemu souboru
data_sheet_name = 'data'
temperature_data = pd.read_excel(data_path, sheet_name=data_sheet_name)


# Definice třídy pro analýzu teplot
class TemperatureAnalytics:
    def __init__(self, data):
        self.data = data

    def get_average_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            print("Špatně zadaný rok")
            return None

        return round(yearly_data['T-AVG'].mean(), 2)

    def get_max_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            return None, None
        max_temp = yearly_data['TMA'].max()
        date_of_max_temp = yearly_data[yearly_data['TMA'] == max_temp][['rok', 'měsíc', 'den']].iloc[0]
        return max_temp, date_of_max_temp

    def get_min_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            return None, None
        min_temp = yearly_data['TMI'].min()
        date_of_min_temp = yearly_data[yearly_data['TMI'] == min_temp][['rok', 'měsíc', 'den']].iloc[0]
        return min_temp, date_of_min_temp

    def get_monthly_averages(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            print("Špatně zadaný rok")
            return None

        return yearly_data.groupby('měsíc')['T-AVG'].mean()

    def analyze_temperature_trends(self, start_year, end_year):
        trend_data = self.data[(self.data['rok'] >= start_year) & (self.data['rok'] <= end_year)]
        annual_average_temperatures = trend_data.groupby('rok')['T-AVG'].mean()
        return annual_average_temperatures

    def plot_annual_temperature_averages(self, start_year, end_year):
        filtered_data = self.data[(self.data['rok'] >= start_year) & (self.data['rok'] <= end_year)]

        annual_avg_temps = filtered_data.groupby('rok')['T-AVG'].mean()
        mt.figure(figsize=(10, 6))
        mt.plot(annual_avg_temps.index, annual_avg_temps.values, marker='o', linestyle='-', color='b')
        mt.title(f'Průměrné roční teploty mezi lety {start_year} a {end_year}')
        mt.xlabel('Rok')
        mt.ylabel('Průměrná teplota (°C]')
        mt.grid(True)
        mt.show()

    def detect_temperature_anomalies(self):
        max_month_temps = self.data.groupby('měsíc')['TMA'].mean()
        anomalies = self.data[self.data['TMA'] > max_month_temps[self.data['měsíc']].values]

        return anomalies


def main():
    # Vytvoření instance třídy a provedení analýzy
    temperature_analytics = TemperatureAnalytics(temperature_data)
    month = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen', 'září', 'říjen', 'listopad',
             'prosinec']
    anomalies= temperature_analytics.detect_temperature_anomalies()
    print(anomalies)

""" while (True):
     print("Interaktivní menu pro analýzu teplot")
     print("1 - Zobrazit průměrnou teplotu pro zadaný rok\n"
           "2 - Zobrazit minimální a maximální teplotu pro zadaný rok\n"
           "3 - Zobrazit měsíční průměry pro zadaný rok\n"
           "4 - Analyzovat teplotní trendy\n"
           "5 - Analyzovat sezónní změny\n"
           "6 - Detekovat teplotní anomálii\n"
           "7 - Vykreslit průměrné roční teploty\n"
           "8 - Vykreslit denní teplotní trendy\n"
           "9 - Vykreslit minimální a maximální teploty pro konkrétní den\n"
           "0 - Konec")

     user_input = input("Zvolte akci:")

     if user_input == "1":
         while (True):
             year_input = int(input("Zadejte rok (1775-2022):"))
             average_temp = temperature_analytics.get_average_temperature(year_input)

             if average_temp is not None:
                 print(f"Průměrná teplota v roce {year_input}: {average_temp}°C")
                 break

     elif user_input == "2":
         while(True):
             year_input = int(input("Zadejte rok (1775-2022):"))
             max_temp, date_max = temperature_analytics.get_max_temperature(year_input)
             min_temp, date_min = temperature_analytics.get_min_temperature(year_input)
             if max_temp is not None:
                 print(
                     f"Maximální teplota v roce {year_input}: {max_temp}°C, datum: {date_max['den']}.{date_max['měsíc']}.{date_max['rok']}")
                 print(
                     f"Minimální teplota v roce {year_input}: {min_temp}°C, datum: {date_min['den']}.{date_min['měsíc']}.{date_min['rok']}")
                 break
             else:
                 print("Špatně zadaný rok")

     elif user_input == "3":
         year_input = int(input("Zadejte rok (1775-2022):"))
         monthly = temperature_analytics.get_monthly_averages(year_input)
         if monthly is not None:
             print(f"Teploty pro rok {year_input}\n"
                   "----------------------------\n")
             for index, temp in monthly.items():
                 print(f"{month[index - 1].capitalize()} {round(temp, 2)} °C")

     elif user_input == "7":
         while(True):
             year_start = int(input("Zadejte rok (1775-2022):"))
             year_end = int(input("Zadejte druhý rok (1775-2022):"))
             if year_start >=1775 and year_end >=1775 and year_start <=2022 and year_end <=2022:
                 temperature_analytics.plot_annual_temperature_averages(year_start, year_end)
                 break
             print("Špatně zadané roky")

     elif user_input == "0":
         print("Program bude ukončen")
         break

     else:
         print("Špatně zadaný vstup\n")

     """

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
