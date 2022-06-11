import numpy as np
import pandas as pd


def clean_data(path, id_col = 0, is_test = False):
    df = pd.read_csv(path, index_col=id_col)
    cabins = df["Cabin"].tolist()
    decks = [np.NaN] * len(cabins)
    rows = [np.NaN] * len(cabins)
    sides = [np.NaN] * len(cabins)
    for i in range(len(cabins)):
        try:
            decks[i] = cabins[i][0:1]
            rows[i] = float(cabins[i][2:-2])
            sides[i] = cabins[i][-1:]
        except TypeError:
            continue
    df["Decks"] = decks
    df["Rows"] = rows
    df["Sides"] = sides
    deckValues = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'T': 7}
    sideValues = {'P': 0, 'S': 1}
    planets = {"Earth": 0, "Mars": 1, "Europa": 2}
    TorF = {True: 1, False: 0}
    destinations = {'TRAPPIST-1e': 0,'PSO J318.5-22': 1, '55 Cancri e': 2}
    names = df.Name.values.tolist()
    surnames = []
    for name in names:
        try:
            surname = name.split(" ")[-1].strip()
        except AttributeError:
            surname = np.NaN
        surnames.append(surname)
    surname_dict = {surnames[i] : i for i in range(len(surnames))}
    df["HomePlanet"] = df["HomePlanet"].replace(planets)
    for col in ["CryoSleep", "VIP"]:
        df[col] = df[col].replace(TorF)
    if not is_test:
       df["Transported"] = df["Transported"].replace(TorF) 
    df["Destination"] = df["Destination"].replace(destinations)
    df["Name"] = surnames
    df["Name"] = df["Name"].replace(surname_dict)
    df["Decks"] = df["Decks"].replace(deckValues)
    df["Sides"] = df["Sides"].replace(sideValues)
    new_cols = ['HomePlanet', 'CryoSleep', 'Cabin', 'Destination', 'Age',
            'VIP', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck',
            'Name', 'Decks', 'Rows', 'Sides', 'Transported'] if not is_test else ['HomePlanet', 'CryoSleep', 'Cabin', 'Destination', 'Age',
            'VIP', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck',
            'Name', 'Decks', 'Rows', 'Sides']
    df = df[new_cols]
    df = df.drop("Cabin", axis=1)

    return df