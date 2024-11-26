import pandas as pd

# Funkcija za poređenje dva CSV fajla po 'id', ignorišući promene u 'Broj_zvezdica' i uključujući 'Naslov'
def compare_products_by_id(file1, file2, output_file):
    # Učitaj CSV fajlove
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Proveri da li kolona 'id' postoji
    if 'Id' not in df1.columns or 'Id' not in df2.columns:
        print("Oba fajla moraju da imaju kolonu 'id'.")
        return

    # Merge dva DataFrame-a po koloni 'id'
    merged_df = pd.merge(df1, df2, on='Id', how='inner', suffixes=('_file1', '_file2'))

    # Pronađi razlike u ostalim poljima, ignorišući 'Broj_zvezdica'
    differences = []
    for _, row in merged_df.iterrows():
        diff = {'Id': row['Id']}  # Uključujemo ID za identifikaciju proizvoda

        # Dodajemo kolonu 'Naslov' u izlaz
        if 'Naslov_file1' in merged_df.columns:
            diff['Naslov'] = row['Naslov_file1']

        # Provera razlika za ostale kolone, osim 'Broj_zvezdica' i 'id'
        for col in df1.columns:
            if col != 'Id' and col != 'Broj_zvezdica' and col != 'Naslov':
                if f"{col}_file1" in merged_df.columns and f"{col}_file2" in merged_df.columns:
                    if row[f"{col}_file1"] != row[f"{col}_file2"]:
                        diff[col] = {
                            "file1": row[f"{col}_file1"],
                            "file2": row[f"{col}_file2"]
                        }
        if len(diff) > 2:  # Ako postoji bilo koja razlika (osim 'id' i 'Naslov')
            differences.append(diff)

    # Kreiraj DataFrame za razlike i sačuvaj u fajl
    differences_df = pd.DataFrame(differences)
    differences_df.to_csv(output_file, index=False)
    print(f"Razlike su sačuvane u fajlu: {output_file}")

# Primer korišćenja
file1 = "Items1.csv"  # Prvi ulazni fajl
file2 = "Items2.csv"     # Drugi ulazni fajl
output_file = "differences.csv"

compare_products_by_id(file1, file2, output_file)
