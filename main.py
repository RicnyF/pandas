# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd


from temperature_analytics import TemperatureAnalytics


# Načtení dat z Excel souboru
data_path = 'data/klementinum.xlsx'  # Upravte cestu k vašemu souboru
data_sheet_name = 'data'
temperature_data = pd.read_excel(data_path, sheet_name=data_sheet_name)
month = ['leden', 'únor', 'březen', 'duben', 'květen', 'červen', 'červenec', 'srpen', 'září', 'říjen', 'listopad',
         'prosinec']


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
            while (True):
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
                year1_temp, year2_temp, comparsion, diff = temperature_analytics.compare_years(year1, year2)
                if year1_temp is not None:
                    print(
                        f"Rok {year1} měl průměrnou teplotu {year1_temp} °C a rok {year2} měl průměrnou teplotu {year2_temp}°C. Rok {comparsion} má větší průměrnou teplotu o {diff}°C. ")
                    break

        elif user_input == "5":
            while (True):
                year_input = int(input("Zadejte rok (1775-2022):"))
                jaro, leto, podzim, zima = temperature_analytics.seasons(year_input)
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
                    print(f"Pruměrná teplota v měsíci {month[month_input - 1]} je {monthly} °C")
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
                if (mesic >= 1 and mesic <= 12) and (rok >= 1775 and rok <= 2022):
                    temperature_analytics.plot_max_and_min_temp(mesic, rok)
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
