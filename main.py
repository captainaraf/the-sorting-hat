import pandas as pd
import numpy as np
import colorama
import pyfiglet
from colorama import Fore
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

colorama.init(autoreset=True)

print(Fore.YELLOW + pyfiglet.figlet_format("Sorting Hat", font="slant"))

csv_file = "dataset.csv"
df = pd.read_csv(csv_file)

df["Quidditch_Fan"] = df["Quidditch_Fan"].str.lower()

le_subject = LabelEncoder()
le_quidditch = LabelEncoder()
le_house = LabelEncoder()

df["Favorite_Subject"] = le_subject.fit_transform(df["Favorite_Subject"])
df["Quidditch_Fan"] = le_quidditch.fit_transform(df["Quidditch_Fan"])
df["House"] = le_house.fit_transform(df["House"])

X = df.drop(columns=["Name", "House"])
y = df["House"]

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)


def sorting_hat():
    print(Fore.CYAN + "\n🎩 The Sorting Hat is ready to sort you!\n")

    bravery = int(input(Fore.YELLOW + "🔴 On a scale of 1-10, how brave are you? "))
    loyalty = int(input(Fore.YELLOW + "🟡 How loyal are you (1-10)? "))
    wisdom = int(input(Fore.YELLOW + "🔵 How wise are you (1-10)? "))
    ambition = int(input(Fore.YELLOW + "🟢 How ambitious are you (1-10)? "))

    print("\n📚 Choose your favorite subject:")
    subjects = le_subject.classes_
    for i, sub in enumerate(subjects):
        print(f"{i}: {sub}")
    favorite_subject = int(
        input("Enter the number corresponding to your favorite subject: ")
    )

    while True:
        quidditch = input("\n🏆 Do you like Quidditch? (Yes/No): ").strip().lower()
        if quidditch in ["yes", "no"]:
            quidditch = le_quidditch.transform([quidditch])[0]
            break
        else:
            print(Fore.RED + "❌ Invalid input! Please type 'Yes' or 'No'. Try again.")

    user_data = pd.DataFrame(
        [[bravery, loyalty, wisdom, ambition, favorite_subject, quidditch]],
        columns=[
            "Bravery",
            "Loyalty",
            "Wisdom",
            "Ambition",
            "Favorite_Subject",
            "Quidditch_Fan",
        ],
    )
    predicted_house_index = model.predict(user_data)[0]
    predicted_house = le_house.inverse_transform([predicted_house_index])[0]

    house_colors = {
        "Gryffindor": Fore.RED,
        "Slytherin": Fore.GREEN,
        "Ravenclaw": Fore.BLUE,
        "Hufflepuff": Fore.YELLOW,
    }

    print(house_colors[predicted_house] + f"\n🎩 You belong to {predicted_house}!\n")


sorting_hat()
