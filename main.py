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
month = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen', 'září', 'říjen', 'listopad',
             'prosinec']

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
        return round(max_temp, 2), date_of_max_temp

    def get_min_temperature(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            return None, None
        min_temp = yearly_data['TMI'].min()
        date_of_min_temp = yearly_data[yearly_data['TMI'] == min_temp][['rok', 'měsíc', 'den']].iloc[0]
        return round(min_temp, 2), date_of_min_temp

    def get_monthly_averages(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            print("Špatně zadaný rok")
            return None

        return round(yearly_data.groupby('měsíc')['T-AVG'].mean(), 2)

    def compare_years(self, year1, year2):
        yearly_data1 = self.data[self.data['rok'] == year1]
        yearly_data2 = self.data[self.data['rok'] ==year2]
        if yearly_data1.empty or yearly_data2.empty:
            print("Špatně zadaný rok")
            return None
        yearly_data1= yearly_data1.groupby('rok')['T-AVG'].mean()
        yearly_data2= yearly_data2.groupby('rok')['T-AVG'].mean()
        if float(yearly_data1[year1]) > float(yearly_data2[year2]):
            return round(yearly_data1[year1],2),round(yearly_data2[year2],2), year1, round(abs(yearly_data1[year1]-yearly_data2[year2]),2)
        return round(yearly_data1[year1],2),round(yearly_data2[year2],2),year2, round(abs(yearly_data1[year1]-yearly_data2[year2]),2)

    def analyze_temperature_trends(self, start_year, end_year):
        trend_data = self.data[(self.data['rok'] >= start_year) & (self.data['rok'] <= end_year)]
        annual_average_temperatures = trend_data.groupby('rok')['T-AVG'].mean()
        return round(annual_average_temperatures, 2)

    def plot_max_and_min_temp(self, mesic, rok):
        filtered_data = self.data[
            ((self.data['rok'] == rok) & (self.data['měsíc'] == mesic))]
        min_temp = filtered_data.groupby('den')['TMI'].mean()
        max_temp = filtered_data.groupby('den')['TMA'].mean()

        mt.figure(figsize=(10, 6))
        mt.plot(min_temp.index, min_temp.values, marker='o', linestyle='-', color='g', label='Minimum Temperature')

        # Plotting maximum temperatures
        mt.plot(max_temp.index, max_temp.values, marker='o', linestyle='-', color='r', label='Maximum Temperature')
        mt.title(f'Maximální a minimální teplota pro {month[mesic-1]} {rok}')
        mt.xlabel('Den')
        mt.ylabel('Teplota (°C)')
        mt.grid(True)
        mt.legend()
        mt.show()

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

    def average_monthly(self, month):
        max_month_temps = round(self.data.groupby('měsíc')['T-AVG'].mean(), 2)
        if max_month_temps.empty:
            print("Špatně zadaný měsíc")
            return None
        return max_month_temps[month]

    def seasons(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            print("Špatně zadaný rok")
            return None
        jaro = yearly_data[(yearly_data['měsíc']== 3) | (yearly_data['měsíc']== 4) | (yearly_data['měsíc']== 5)]
        jaro= jaro.groupby('měsíc')['T-AVG'].mean()
        jaro = sum(jaro)/len(jaro)
        leto = yearly_data[(yearly_data['měsíc']== 6) | (yearly_data['měsíc']== 7) | (yearly_data['měsíc']== 8)]
        leto = leto.groupby('měsíc')['T-AVG'].mean()
        leto = sum(leto) / len(leto)
        podzim = yearly_data[(yearly_data['měsíc'] == 9) | (yearly_data['měsíc'] == 10) | (yearly_data['měsíc'] == 11)]
        podzim = podzim.groupby('měsíc')['T-AVG'].mean()
        podzim = sum(podzim) / len(podzim)
        zima = yearly_data[(yearly_data['měsíc'] == 12) | (yearly_data['měsíc'] == 1) | (yearly_data['měsíc'] == 2)]
        zima = zima.groupby('měsíc')['T-AVG'].mean()
        zima = sum(zima) / len(zima)
        return round(jaro,2) ,round(leto,2), round(podzim,2) , round(zima,2)
def main():
    # Vytvoření instance třídy a provedení analýzy
    temperature_analytics = TemperatureAnalytics(temperature_data)


    while (True):
        print("Interaktivní menu pro analýzu teplot")
        print("1 - Zobrazit průměrnou teplotu pro zadaný rok\n"
              "2 - Zobrazit minimální a maximální teplotu pro zadaný rok\n"
              "3 - Zobrazit měsíční průměry pro zadaný rok\n"
              "4 - Porovnat průmernou teplotu roků\n"
              "5 - Analyzovat sezónní teplotu\n"
              "6 - Průmerná teplota měsíce\n"
              "7 - Vykreslit průměrné roční teploty\n"
              "8 - Vykreslit minimální a maximální teploty pro konkretni měsíc roku \n"
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
            while (True):
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
            while(True):
                year_input = int(input("Zadejte rok (1775-2022):"))
                monthly = temperature_analytics.get_monthly_averages(year_input)
                if monthly is not None:
                    print(f"Teploty pro rok {year_input}")
                    for index, temp in monthly.items():
                        print(f"{month[index - 1].capitalize()} {temp} °C")
                    break
        
        elif user_input == "4":
            while (True):
                year1 = int(input("Zadejte rok (1775-2022):"))
                year2 = int(input("Zadejte druhý rok (1775-2022):"))
                year1_temp,year2_temp, comparsion, diff = temperature_analytics.compare_years(year1,year2)
                if year1_temp is not None:
                    print(f"Rok {year1} měl průměrnou teplotu {year1_temp} °C a rok {year2} měl průměrnou teplotu {year2_temp}°C. Rok {comparsion} má větší průměrnou teplotu o {diff}°C. ")
                    break

        elif user_input == "5":
            while(True):
                year_input = int(input("Zadejte rok (1775-2022):"))
                jaro,leto,podzim,zima = temperature_analytics.seasons(year_input)
                if jaro is not None:
                    print(f"Průmerné sezónní teploty pro rok {year_input}.")
                    print(f"Jaro {jaro} °C \n"
                          f"Leto {leto} °C \n"
                          f"Podzim {podzim} °C\n"
                          f"Zima {zima} °C")
                    break
        
        
        elif user_input == "6":
            while (True):
                month_input = int(input("Zadejte číslo měsíce (1-12):"))
                monthly = temperature_analytics.average_monthly(month_input)
                if month is not None:
                    print(f"Pruměrná teplota v měsíci {month[month_input-1]} je {monthly} °C")
                    break
                print("Špatně zadané roky")

        elif user_input == "7":
            while (True):
                year_start = int(input("Zadejte rok (1775-2022):"))
                year_end = int(input("Zadejte druhý rok (1775-2022):"))
                if year_start >= 1775 and year_end >= 1775 and year_start <= 2022 and year_end <= 2022:
                    temperature_analytics.plot_annual_temperature_averages(year_start, year_end)
                    break
                print("Špatně zadané roky")
        elif user_input == "8":
            while (True):
                rok = int(input("Rok (1775-2022):"))
                mesic = int(input("Zadejte mesic (1,12):"))
                if (mesic >= 1 and mesic <= 12 )and( rok >= 1775 and rok <= 2022):
                    temperature_analytics.plot_max_and_min_temp(mesic,rok)
                    break
                print("Špatně zadané roky")
        elif user_input == "0":
            print("Program bude ukončen")
            break

        else:
            print("Špatně zadaný vstup\n")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
