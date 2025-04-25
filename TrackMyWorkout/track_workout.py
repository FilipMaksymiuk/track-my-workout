#Program Pomaga w śledzeniu swojego progresu
#Biblioteki potrzebne do poprawnego działania programu
#
import pandas as pd
import os
import datetime
from tabulate import tabulate


DATA_FILE = "treningi.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    if 'Week' not in df.columns:
        df['Week'] = df['Date'].apply(lambda x: x.isocalendar()[1] if pd.notna(x) else None)
else:
    df = pd.DataFrame(columns=["Date", "Exercise", "Series", "Reps", "Weight", "Week"])

def list_exercises():
    if df.empty:
        print("Brak zapisanych ćwiczeń.")
        return []
    return df["Exercise"].unique().tolist()

def add_new_entry():
    today = datetime.date.today()
    week_num = today.isocalendar()[1]  # Pobranie numeru tygodnia (ISO calendar)

    print("\nDostępne ćwiczenia:")
    current_exercises = list_exercises()
    for i, ex in enumerate(current_exercises):
        print(f"{i + 1}. {ex}")

    choice = input("Wybierz numer ćwiczenia lub wpisz nowe: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(current_exercises):
        exercise = current_exercises[int(choice) - 1]
    else:
        exercise = choice


    date_input = input(f"Podaj datę treningu (domyślnie {today}): ").strip()
    if date_input:
        try:
            date = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            print("Niepoprawny format daty, użyto domyślnej.")
            date = today
    else:
        date = today

    try:
        series_count = int(input("Ile serii chcesz dodać (1-5)? "))
        if not (1 <= series_count <= 5):
            raise ValueError
    except ValueError:
        print("Niepoprawna liczba serii.")
        return

    new_rows = []
    for i in range(series_count):
        reps = input(f"Seria {i + 1}: liczba powtórzeń: ")
        weight = input(f"Seria {i + 1}: ciężar (kg): ")
        new_rows.append({
            "Date": date,
            "Exercise": exercise,
            "Series": i + 1,
            "Reps": int(reps),
            "Weight": float(weight),
            "Week": week_num
        })

    global df
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print("Zapisano dane.")

def edit_entry():
    print("\nDostępne ćwiczenia do edycji:")
    current_exercises = list_exercises()
    for i, ex in enumerate(current_exercises):
        print(f"{i + 1}. {ex}")

    choice = input("Wybierz numer ćwiczenia, które chcesz edytować: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(current_exercises):
        exercise = current_exercises[int(choice) - 1]
    else:
        print("Niepoprawny wybór.")
        return

    print(f"Edytujesz ćwiczenie: {exercise}")
    df_ex = df[df["Exercise"] == exercise]
    print("Dostępne dni i serie:")
    print(tabulate(df_ex, headers='keys', tablefmt='fancy_grid', showindex=False))

    series_to_edit = input("Wybierz numer serii do edycji (np. 1, 2, 3): ").strip()
    if series_to_edit.isdigit() and 1 <= int(series_to_edit) <= 3:
        series_to_edit = int(series_to_edit)
        row = df_ex[df_ex["Series"] == series_to_edit].iloc[0]
        print(f"Edytujesz serię {series_to_edit}: {row['Reps']} reps, {row['Weight']} kg")

        new_reps = input(f"Nowa liczba powtórzeń (aktualnie {row['Reps']}): ")
        new_weight = input(f"Nowy ciężar (kg) (aktualnie {row['Weight']}): ")

        df.loc[(df["Exercise"] == exercise) & (df["Series"] == series_to_edit), "Reps"] = int(new_reps)
        df.loc[(df["Exercise"] == exercise) & (df["Series"] == series_to_edit), "Weight"] = float(new_weight)
        df.to_csv(DATA_FILE, index=False)
        print("Edytowano dane.")
    else:
        print("Niepoprawny wybór serii.")

def delete_entry():
    print("\nDostępne ćwiczenia do usunięcia:")
    current_exercises = list_exercises()
    for i, ex in enumerate(current_exercises):
        print(f"{i + 1}. {ex}")

    choice = input("Wybierz numer ćwiczenia, które chcesz usunąć: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(current_exercises):
        exercise = current_exercises[int(choice) - 1]
    else:
        print("Niepoprawny wybór.")
        return

    df_ex = df[df["Exercise"] == exercise]
    print(f"Dostępne dni i serie do usunięcia: ")
    print(tabulate(df_ex, headers='keys', tablefmt='fancy_grid', showindex=False))

    date = input("Wybierz datę (YYYY-MM-DD) do usunięcia lub wpisz 'cancel', aby przerwać: ")
    if date.lower() == 'cancel':
        return

    df_ex_date = df_ex[df_ex["Date"] == date]
    if df_ex_date.empty:
        print("Brak wpisu dla tej daty.")
        return

    print(f"Wpisy do usunięcia dla {exercise} na dzień {date}:")
    print(tabulate(df_ex_date, headers='keys', tablefmt='fancy_grid', showindex=False))

    series_to_delete = input("Wybierz serię do usunięcia (1-3): ").strip()
    if series_to_delete.isdigit() and 1 <= int(series_to_delete) <= 3:
        series_to_delete = int(series_to_delete)
        df.drop(df_ex_date[df_ex_date["Series"] == series_to_delete].index, inplace=True)
        df.to_csv(DATA_FILE, index=False)
        print("Usunięto dane.")
    else:
        print("Niepoprawny wybór serii.")

def show_data():
    print("\nDostępne dane:")
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

def show_sorted_data():
    print("\nWybierz sposób sortowania:")
    print("1. Po dacie")
    print("2. Po ćwiczeniu")
    print("3. Po ciężarze")
    print("4. Po powtórzeniach")
    print("5. Po tygodniach")
    print("6. Brak sortowania (wyświetl dane w kolejności dodania)")
    choice = input("Wybierz opcję sortowania: ")

    if choice == "1":
        sorted_df = df.sort_values(by="Date")
    elif choice == "2":
        sorted_df = df.sort_values(by="Exercise")
    elif choice == "3":
        sorted_df = df.sort_values(by="Weight", ascending=False)
    elif choice == "4":
        sorted_df = df.sort_values(by="Reps", ascending=False)
    elif choice == "5":
        sorted_df = df.sort_values(by="Week")
    elif choice == "6":
        sorted_df = df
    else:
        print("Niepoprawna opcja.")
        return

    print("Posortowane dane: ")
    print(tabulate(sorted_df, headers='keys', tablefmt='fancy_grid', showindex=False))

if __name__ == "__main__":
    while True:
        print("\n=== TRACK MY WORKOUT ===")
        print("1. Dodaj nowy trening")
        print("2. Pokaż dane (bez sortowania lub z sortowaniem)")
        print("3. Edytuj istniejący wpis")
        print("4. Usuń wpis")
        print("5. Wyjście")

        option = input("Wybierz opcję: ")

        if option == "1":
            add_new_entry()
        elif option == "2":
            show_sorted_data()
        elif option == "3":
            edit_entry()
        elif option == "4":
            delete_entry()
        elif option == "5":
            print("Do zobaczenia!")
            break
        else:
            print("Niepoprawna opcja.")
