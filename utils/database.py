import os
import pandas as pd

os.makedirs("data", exist_ok=True)

def get_database_file(role):
    return f"data/{role.lower()}s.csv"

def create_user(name, age, address, password, role):
    file = get_database_file(role)
    df = pd.DataFrame([[name, age, address, password]], columns=["Nom", "Âge", "Adresse", "Mot de passe"])
    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)

def verify_user(name, password, role):
    file = get_database_file(role)
    if os.path.exists(file):
        df = pd.read_csv(file)
        return ((df["Nom"] == name) & (df["Mot de passe"] == password)).any()
    return False
