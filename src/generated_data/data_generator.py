import random
import csv

# SIMULARE DE CONSUM
def simuleaza_carburant(distance, pct_city, avg_speed_city, avg_speed_hwy, ac_on, persons, tire_pressure, temp):

    # consum de baza
    base_city = 10.3
    base_hwy  = 7.8

    # efect AC
    if ac_on == 1:
        base_city += 0.6
        base_hwy  += 0.3

    #adaos persoane
    extra_mass = (persons - 1) * 90  # ~90 kg per pasager
    base_city += extra_mass * 0.003
    base_hwy  += extra_mass * 0.0015

    #adaos presiune pneuri
    if tire_pressure < 2.0:
        base_city += 0.5
        base_hwy  += 0.3

    #adaos temperatura scazuta
    if temp < 5:
        base_city += 0.4
        base_hwy  += 0.2

    #calcul procent urban/extraurban
    city_fraction = pct_city / 100
    hwy_fraction  = 1 - city_fraction

    l_per_100 = base_city * city_fraction + base_hwy * hwy_fraction

    noise = random.uniform(-0.3, 0.3)

    return (distance * l_per_100 / 100) + noise

#GENERATORUL DE DATE
def genereaza(n=2500):
    rows = []

    for _ in range(n):
        distance = round(random.uniform(10, 700), 1)
        pct_city = round(random.uniform(5, 100), 1)
        avg_speed_city = round(random.uniform(18, 50), 1)
        avg_speed_hwy  = round(random.uniform(85, 130), 1)
        ac_on = random.choice([0, 1])
        persons = random.choice([1, 2, 3, 4, 5])
        tire_pressure = random.choice([1.8, 2.0, 2.2, 2.25])
        temp = round(random.uniform(-10, 40), 1)

        fuel = simuleaza_carburant(
            distance, pct_city, avg_speed_city, avg_speed_hwy,
            ac_on, persons, tire_pressure, temp
        )

        rows.append([
            distance,
            pct_city,
            avg_speed_city,
            avg_speed_hwy,
            ac_on,
            persons,
            tire_pressure,
            temp,
            round(fuel, 2)
        ])

    with open("generated_trips4.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "distance_km",
            "city_share_pct",
            "avg_speed_city",
            "avg_speed_hwy",
            "ac_on",
            "persons_in_car",
            "tire_pressure_bar",
            "outside_temp_c",
            "fuel_used_l"
        ])
        writer.writerows(rows)

    print("a aparut generated_trips.csv")

if __name__ == "__main__":
    genereaza(2500)
