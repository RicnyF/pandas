
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as mt

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
        yearly_data2 = self.data[self.data['rok'] == year2]
        if yearly_data1.empty or yearly_data2.empty:
            print("Špatně zadaný rok")
            return None
        yearly_data1 = yearly_data1.groupby('rok')['T-AVG'].mean()
        yearly_data2 = yearly_data2.groupby('rok')['T-AVG'].mean()
        if float(yearly_data1[year1]) > float(yearly_data2[year2]):
            return round(yearly_data1[year1], 2), round(yearly_data2[year2], 2), year1, round(
                abs(yearly_data1[year1] - yearly_data2[year2]), 2)
        return round(yearly_data1[year1], 2), round(yearly_data2[year2], 2), year2, round(
            abs(yearly_data1[year1] - yearly_data2[year2]), 2)

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
        mt.title(f'Maximální a minimální teplota pro {month[mesic - 1]} {rok}')
        mt.xlabel('Den')
        mt.ylabel('Teplota (°C)')
        mt.grid(True)
        mt.legend()
        mt.show()

    def plot_annual_temperature_averages(self, start_year, end_year):
        if start_year >= end_year:
            print("Druhý rok musí být novější")

        else:
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
        return max_month_temps[month]

    def seasons(self, year):
        yearly_data = self.data[self.data['rok'] == year]
        if yearly_data.empty:
            print("Špatně zadaný rok")
            return None
        jaro = yearly_data[(yearly_data['měsíc'] == 3) | (yearly_data['měsíc'] == 4) | (yearly_data['měsíc'] == 5)]
        jaro = jaro.groupby('měsíc')['T-AVG'].mean()
        jaro = sum(jaro) / len(jaro)
        leto = yearly_data[(yearly_data['měsíc'] == 6) | (yearly_data['měsíc'] == 7) | (yearly_data['měsíc'] == 8)]
        leto = leto.groupby('měsíc')['T-AVG'].mean()
        leto = sum(leto) / len(leto)
        podzim = yearly_data[(yearly_data['měsíc'] == 9) | (yearly_data['měsíc'] == 10) | (yearly_data['měsíc'] == 11)]
        podzim = podzim.groupby('měsíc')['T-AVG'].mean()
        podzim = sum(podzim) / len(podzim)
        zima = yearly_data[(yearly_data['měsíc'] == 12) | (yearly_data['měsíc'] == 1) | (yearly_data['měsíc'] == 2)]
        zima = zima.groupby('měsíc')['T-AVG'].mean()
        zima = sum(zima) / len(zima)
        return round(jaro, 2), round(leto, 2), round(podzim, 2), round(zima, 2)
