 

#Otevřete soubor catalogue.json a načtěte si data do Pythonu.
import json
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
# FINAL project 1

file_save = r'C:\Users\Toshiba\.spyder-py3\catalogue.json'
with open (file_save, 'r') as file:
    data = json.load(file)



data    
list_merge = pd.DataFrame(data)    
    
list = data['list_of_branches'] 
print(list)
print(data.keys())
print(data['season'])
print(data['name_of_shop'])

data_branches = pd.DataFrame(data["list_of_branches"])
data_products = pd.DataFrame(data["list_of_products"])

data_branches
data_products



def verify_json(catalogue):
    count_check = 0
    for item in ["season", "name_of_shop", "list_of_branches", "list_of_products"]:
        if item in catalogue.keys():
            count_check += 1
    
    if count_check == 4:
        print("Soubor je kompletní")
    else:
        print("Soubor není celý, nebo obsahuje něco navíc")
    
    
    if catalogue['season'] == "2023/24":
        print("Je to správná sezóna.")
    else:
        print(f"Je to nesprávná sezóna. Katalog je za sezónu {catalogue['season']}.")

    pocet_pobocek = len(catalogue["list_of_branches"])
    print(f"Počet poboček: {pocet_pobocek}")

    pocet_novych_pobocek = 0
    output = {}

    for branch in catalogue["list_of_branches"]:
        otevreni = datetime.strptime(branch["Launch_Date"], "%Y-%m-%d")
        if otevreni > datetime.now():
            pocet_novych_pobocek += 1
            print("V datech je nová pobočka")
            if otevreni == datetime(2025, 1, 1):
                print(f"Nová pobočka {branch['Location']} otevírá 1.1.2025.")
            else:
                print(f"Nová pobočka {branch['Location']} otevírá {branch['Launch_Date']}") 
        output[branch["Name_of_Location_Manager"]] = branch["Contact_Number"]

    if pocet_novych_pobocek == 0:
        print("V datech není žádná nová pobočka")
    return output

contacts = verify_json(data)


    
#Final Project 2:


data_products = pd.DataFrame(data["list_of_products"])
data_products.info(['Category'])

data_products['Category'].unique()
#Kolik kategorií produktů nabízí One&Only Ski Shop?
#'Poles', 'Ski Helmets', 'Gloves', 'Ski Boots', 'Skis']
print("Kolik kategorií produktů nabízí One&Only Ski Shop?:", len(data_products["Category"].unique()))
# Kolik celkově produktů se nachází v katalogu? 78
print("Kolik celkově produktů se nachází v katalogu?:", len(data_products["ID"].unique()))
#Kolik značek má v nabídce One&Only Ski Shop?
print("Kolik značek má v nabídce One&Only Ski Shop?:", len(data_products["Brand"].unique()))
products = data_products['Brand'].unique()
len(products) 
#16
 


#Skontrolujte, zda se v datech nenacházejí nelogické hodnoty - zaměřte se na cenu
data_products['Catalogue_Price'].sort_values()
data_products['Catalogue_Price'].desribe()
45   -98731.86
68   -98233.68
34   -98208.90


#Smazan9 hodnot v dataframe
data_products.loc[data_products['Catalogue_Price'] < 0, 'ID']
data_products

data_products = data_products.drop(data_products.loc[data_products["Catalogue_Price"] <= 0].index)

data_products = data_products.drop(index = [45, 68, 34])
df.drop(index = [45, 68, 34])

#Jaká je průměrná cena všech produktů dohromady?
data_products['Catalogue_Price'].mean()
#Out[97]: 1562.4464
print("Jaká je průměrná cena všech produktů dohromady?", data_products["Catalogue_Price"].mean())

#Produkty které kategorie jsou nejdražší?
data_products.groupby('Category')['Catalogue_Price'].mean().sort_values()
Gloves         1245.750000
Ski Boots      1251.032727
Poles          1262.400500
Ski Helmets    1284.338571
Skis           2767.141333

print(data_products.groupby("Brand")["ID"].count().sort_values(ascending = False))

#Produkty které kategorie jsou nejlevnější?
print(data_products.query("Brand == 'One Way'").sort_values("Catalogue_Price"))
data_products.sort_values( by = ['Category','Catalogue_Price' ],
                             ascending = False,
                            )

      ID Category  ...                      Model Catalogue_Price
52  39299     Skis  ...          Stoeckli Model 11         4742.54
31  12693     Skis  ...           Nordica Model 28         4214.69
74  16655     Skis  ...          Stoeckli Model 46         4183.17
44  52107     Skis  ...             Atomic Model 6         3783.25
22  45222     Skis  ...          Stoeckli Model 24         3663.69
..    ...      ...  ...                        ...             ...
64  46212   Gloves  ...             Burton Model 6         1055.24
15  92798   Gloves  ...            Burton Model 24         1035.13
67  16102   Gloves  ...            Hestra Model 33          975.38
66  76235   Gloves  ...  Outdoor Research Model 33          613.02
4   35658   Gloves  ...            Hestra Model 42          570.00



# Která značka má nejvíce produktů v katalogu?
data_products['Brand'].value_counts().max()
#Out[110]: 13
data_products['Brand'].value_counts().idxmax()
#Out[107]: 'One Way'

#Který produkt této značky je nejdražší a kolik stojí?
data_products.loc[data_products['Brand'] =='One Way']


data_products.loc[data_products['Brand'] =='One Way'].max()
#ID                           99912
#Category                     Poles
#Brand                      One Way
#Model              One Way Model 9
#Catalogue_Price            1773.84
#dtype: object

#Který produkt této značky je nejlevnější a kolik stojí?

data_clear.loc[data_clear['Brand'] =='One Way'].min()
data_products.query("Brand == 'One Way'").sort_values("Catalogue_Price")
#ID                            18571
#Category                      Poles
#Brand                       One Way
#Model              One Way Model 11
#Catalogue_Price              523.95




# Průměrná cena produktů podle kategorií produktů (Horizontální sloupcový diagram)
prumerna_cena = data_products.groupby('Brand')['Catalogue_Price'].mean().sort_values()

plt.figure(figsize =(15,10))
plt.bar(prumerna_cena.index,prumerna_cena.values, color= 'green'   )
plt.ylabel('znacka')
plt.xlabel('Prumerna cena')
plt.title('Průměrnou cenu produktů podle jednotlivých značek')
plt.xticks(rotation=45)
plt.grid()
plt.savefig('prework15_12')
plt.show()

# Počet nabízených produktů podle kategorií (Koláčový graf)
product_count_per_category = data_products['Category'].value_counts()

plt.figure(figsize=(15, 10))
plt.pie(average_price_per_category.values, labels=average_price_per_category.index, autopct='%1.1f%%', startangle=45)
plt.title('Počet nabízených produktů podle kategorií')

# Průměrná cena produktů podle jednotlivých značek (Sloupcový diagram)
average_price_per_brand = data_products.groupby('Brand')['Catalogue_Price'].mean().sort_values()

plt.figure(figsize=(15, 10))
plt.bar(average_price_per_brand.index, average_price_per_brand.values, color='blue')
plt.xlabel("Značka")
plt.ylabel("Průměrná cena")
plt.title('Průměrná cena produktů podle značek')
plt.xticks(rotation=45)






#Final Project 3

#Načtěte si pomocí Pandas soubor ski_orders.csv.
df = pd.read_csv(r'C:\Users\Toshiba\.spyder-py3\ski_orders.csv ', sep = ',', encoding = 'UTF-8', decimal = ',')

df = pd.merge(df, data_branches, left_on = "Branch_ID", right_on = "ID", how = "left")
df = pd.merge(df, data_products, left_on = "Product_ID", right_on = "ID", how = "left")

data_branches = pd.DataFrame(data["list_of_branches"])
data_products = pd.DataFrame(data["list_of_products"])




--------------------------------------------------------------------------
#BeautifulSoup()

r = requests.get(r'https://www.fis-ski.com/DB/general/results.html?sectorcode=AL&raceid=122772')
soup = BeautifulSoup(r.text, 'html.parser')

print(soup.prettify())


results = soup.find("div", id = "events-info-results")
rows = results.find_all("div", class_ = "g-row justify-sb")

output = []
for row in tqdm.tqdm(rows):
    fis_code = row.find("div", class_ = "pr-1 g-lg-2 g-md-2 g-sm-2 hidden-xs justify-right gray").text.split()[0]
    name = row.find("div", class_ = "g-lg-10 g-md-10 g-sm-9 g-xs-8 justify-left bold").text.split()
    name = " ".join(name)
    year = row.find("div", class_ = "g-lg-1 g-md-1 hidden-sm-down justify-left").text.split()[0]
    nation = row.find("div", class_ = "g-lg-1 g-md-1 g-sm-2 g-xs-3 justify-left").text.split()[0]
    output.append([fis_code, name, year, nation])
    
results_dnf = soup.find_all("div", class_ = "table table_min_height")[0].find_all("div", class_ = "table__body")[1]
rows = results_dnf.find_all("div", class_ = "g-row justify-sb")

for row in tqdm.tqdm(rows):
    fis_code = row.find("div", class_ = "pr-1 g-lg-2 g-md-2 g-sm-2 hidden-xs justify-right gray").text.split()[0]
    name = row.find("div", class_ = "g-lg-10 g-md-10 g-sm-9 g-xs-8 justify-left bold").text.split()
    name = " ".join(name)
    year = row.find("div", class_ = "g-lg-1 g-md-1 hidden-sm-down justify-left").text.split()[0]
    nation = row.find("div", class_ = "g-lg-1 g-md-1 g-sm-2 g-xs-3 justify-left").text.split()[0]
    output.append([fis_code, name, year, nation])
    
data_racers = pd.DataFrame(output, columns = ["FIS_Code", "Name", "Birth Year", "Nation"])
data_racers["FIS_Code"] = data_racers["FIS_Code"].astype(int)

df = pd.merge(df, data_racers, left_on = "Racer_ID", right_on = "FIS_Code", how = "left")

print(df)


--------------------------------------------------------------------
df.info()

df['total_value'] = df['Catalogue_Price'] * df['Quantity']

df.to_csv('final_project_3_part.csv', sep = ',', index = False)

### Některé produkty, které jste z katalogu odstranili, nyní mohou chybět. 
print("Kolik takových položek se nachází v tabulce?:", df.loc[df["ID_y"].isna()]["Order_ID"].count())
#Kolik takových položek se nachází v tabulce?: 986
### Kolik takových položek se nachází v tabulce? Kolik celkově bylo takto objednaných produktů?
print("Kolik celkově bylo takto objednaných produktů?:", df.loc[df["ID_y"].isna()]["Quantity"].sum())
#Kolik celkově bylo takto objednaných produktů?: 5347



### Některé položky jsou objednávky v budoucnosti - to nevadí. 
### Avšak problém je, pokud byla objednávka vytvořena na ještě neotevřené pobočce. 
print("Ověřte, zda se tam nacházejí takové objednávky.:", len(df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Order_ID"].unique()))
print("Jaká je jejich celková hodnota?:", df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Total_price"].sum())

### Pomocí .loc přiřaďte tyto objednávky do pobočky v Curychu.
df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "ID_x"] = 4346
df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Location"] = "Zurich"
df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Country"] = "Switzerland"
df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Name_of_Location_Manager"] = "Candace Perkins"
df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Contact_Number"] = "+41 44 668 18 00"
df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Branch_ID"] = 4346

#Celkova pocet objednavek v budoucnosti tedy na pobocce ktera nebyla otevrena.:
future_orders = len(df.loc[(df["Branch_ID"] == 9342) & (df["Date"] < df["Launch_Date"]), "Order_ID"].unique())
print(f'celkovy pocet objednavek, ktery jsou prirazene na pobocku v budoucnu Milan je {future_orders}')
future_orders
Out[29]: 37

#Celkova hodnota objednavk v budoucnosti tedy na pobocce ktera nebyla otevrena.:
future_orders_sum = df.loc[df["Branch_ID"] == 9342 & (df["Date"] < df["Launch_Date"]), "total_value"].sum()
future_orders_sum
print(f'celkova hodnota objednavek {future_orders_sum}')


#Kolik objednávek (počet unikátních Order_ID) vytvořil HROBAT Miha?
print("Kolik objednávek (počet unikátních Order_ID) vytvořil HROBAT Miha?:", len(df.loc[df["Name"] == "HROBAT Miha", "Order_ID"].unique()))

#Za jakou sumu celkově vytvořil objednávky MONSEN Felix?
print("Za jakou sumu celkově vytvořil objednávky MONSEN Felix?:", df.loc[df["Name"] == "MONSEN Felix", "Total_price"].sum())
Monsen_order = df.query( "Name == 'MONSEN Felix'") ['total_value'].sum()
'#Monsen Felix vytvoril objednavky za 4125924.66 
print(f'Monsen Felix vytvoril objednavky za {Monsen_order} ')

#odstraneni minusovych hodnot
df = df.drop(df.loc[df['Catalogue_Price'] <=0].index)




#Který závodník vytvořil nejdražší objednávku (součet celkové hodnoty total_value podle Order_ID)?
 print("Který závodník vytvořil nejdražší objednávku (součet celkové hodnoty total_value podle Order_ID)?", df.loc[df["Order_ID"] == id_1, "Name"].iloc[0])
id_1 = df.groupby("Order_ID")["total_value"].sum().idxmax()
id_1

name_races = df.loc[df['Order_ID'] == id_1, 'Name_of_Location_Manager' ].iloc[0]
name_races
print(f'Neslo mi naleznout Name, tak jsem to zmenil na Name_of_Location_Manager: {name_races} ')
# Todd Anderson 

#Závodníci, z které země objednali nejvíce kusů produktů?

top_orders = df.groupby("Nation")["Quantity"].sum().idxmax()
top_orders
#Out[80]: 'SUI'

print(f' nejvice zbozi objednavili {top_orders}')


#Jaké produkty si objednal ZABYSTRAN Jan? Kolik za ně celkově zaplatil?
print(df.loc[df["Name"] == "ZABYSTRAN Jan", ["Model", "Total_price"]].groupby("Model").sum().sort_values("Total_price"))


Jan_orders = df.query("Name == 'ZABYSTRAN Jan' ")[['Model', 'total_value']].groupby('Model').sum().sort_values('total_value', ascending = False)
Jan_orders


Model                                 
Burton Model 32                2778.10
Outdoor Research Model 33      3678.12
Hestra Model 42                5700.00
Hestra Model 2                 8778.14
Burton Model 6                10552.40
                               ...
Kaestle Model 33             169607.49
Atomic Model 6               200512.25
Nordica Model 28             240237.33
Stoeckli Model 46            259356.54
Stoeckli Model 11            284552.40

#Který závodník udělal úplně první objednávku - podle data?
print("Který závodník udělal úplně první objednávku - podle data?:", df.loc[df["Date"].idxmin(), "Name"])
df.loc[df['Date'].idxmin(), 'Name']
Out[104]: 'NEGOMIR Kyle'

#Která pobočka je nejúspěšnější? Zhodnoťte to podle více parametrů:
#
top_pieces = df.groupby("Branch_ID")["Quantity"].sum().idxmax()
Out[106]: 4950

location = data_branches.loc[data_branches['ID'] == top_pieces, 'Location'].values[0]
location
Out[119]: 'Denver'
print(f' Pobocka ktera ta nejuspesnejsi dle prodaneho mnozstvi {location}')


#Počet unikátních objednávek.
top_orders = df.groupby("Branch_ID")["Order_ID"].nunique().idxmax()
top_orders_unique = data_branches.loc[data_branches['ID'] == top_orders, 'Location'].values[0]

print("Počet prodaných kusů.:", df.groupby("Location")["Quantity"].sum().idxmax())

print(f'pocet unikatnich ORDER ID neboli objednavek {top_orders_unique}' )
pocet unikatnich ORDER ID neboli objednavek Zurich

#Celková hodnota objednávek.
top_values = df.groupby('Branch_ID')['total_value'].sum().idxmax()
top_values_result = data_branches.loc[data_branches['ID'] == top_values, 'Location'].values[0]

print(f'Celkova hodnota objednavek {top_values_result}' )
Celkova hodnota objednavek Denver


print("Který produkt se nejlépe prodává?:", df.groupby("Model")["Quantity"].sum().idxmax())


df["Month"] = df["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").month)
df["Year"] = df["Date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").year)

# Ve kterých třech měsících byla nejvyšší hodnota objednávek (pomocný sloupec month)?
df.groupby("Month")["total_value"].sum().sort_values(ascending = False)[:3]

Month
4    20433777.17
5    19332311.55
3    19320177.75


# Jak se měnila celková hodnota objednávek v jednotlivých rocích (pomocný sloupec year)?
df.groupby("Year")["total_value"].sum()
Year
2015     4643840.92
2016    16188299.66
2017    24513389.98
2018    27687392.85
2019    37404361.43
2020    36783016.45
2021    30767581.02
2022    21261750.97
2023    13574623.11
2024     9117332.67

df.groupby("Year")["total_value"].sum().plot()


actual_date = datetime.now()

actual_date.month





#Project final 4 --------------------------------------------------------
#Vytvořte si tabulku - nový dataframe, který bude obsahovat následující sloupce:
#FIS Code
#Jméno závodníka
#Značku lyží
#Značku bot
#Značku holí

### BeautifulSoup
output = []
for fis_code in tqdm.tqdm(data_racers.FIS_Code):
    r = requests.get(f"https://www.fis-ski.com/DB/general/athlete-biography.html?sectorcode=al&fiscode={fis_code}")
    soup = BeautifulSoup(r.text, 'html.parser')
    time.sleep(1)

    racer_name = soup.find("h1", class_ = "athlete-profile__name").text
    racer_name = racer_name.split()
    racer_name = " ".join(racer_name) 
    
    skis_info = soup.find("li", id = "Skis")
    skis_text = skis_info.find("span", class_ = "profile-info__value").text
    
    boots_info = soup.find("li", id = "Boots")
    boots_text = boots_info.find("span", class_ = "profile-info__value").text
    
    poles_info = soup.find("li", id = "Poles")
    poles_text = poles_info.find("span", class_ = "profile-info__value").text
    
    output.append([fis_code, racer_name, skis_text, boots_text, poles_text])
    time.sleep(1)

racers_details = pd.DataFrame(output, columns = ["FIS_Code", "Name", "Skis_brand", "Boots_brand", "Poles_brand"])






df = pd.merge(df, racers_details, left_on = "Racer_ID", right_on = "FIS_Code", how = "left")
df.drop(["FIS_Code_y", "Name_y"],axis = 1, inplace = True)
df.rename({"FIS_Code_x":"FIS_Code", "Name_x":"Name"}, inplace = True)

# Kontrolný stoupec
df.loc[df.Category == "Skis", "Brand_kontrola"] = df.loc[df.Category == "Skis", "Skis_brand"]
df.loc[df.Category == "Ski Boots", "Brand_kontrola"] = df.loc[df.Category == "Ski Boots", "Boots_brand"]
df.loc[df.Category == "Poles", "Brand_kontrola"] = df.loc[df.Category == "Poles", "Boots_brand"]
df.loc[df.Brand_kontrola.isna(), "Brand_kontrola"] = "bez_kontroly"

df.loc[df.Brand_kontrola != "bez_kontroly", "Brand_kontrola"] = df.Brand_kontrola == df.Brand
df.loc[df.Brand_kontrola == "bez_kontroly", "Brand_kontrola"] = None

# Vytvořte graf/grafy pomocí matplotlib:
## Celkový podíl špatně objednaných značek
brand_kontrola_counts = df['Brand_kontrola'].value_counts()

plt.figure(figsize=(15, 10))
plt.pie(brand_kontrola_counts.values, labels=brand_kontrola_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Počet nabízených produktů podle kategorií')

## Podíl špatně objednaných značek pro jednotlivé kategorie
brand_kontrola_by_category = df.groupby("Category")["Brand_kontrola"].value_counts(normalize=True).unstack()
ax = brand_kontrola_by_category.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'red'])
ax.set_xlabel('Kategórie')
ax.set_ylabel('Podíl')
ax.set_title('Podíl správně objednaných značek')
plt.xticks(rotation=0)  # Rotate category labels to horizontal
plt.legend(title='Kontrola značek', labels=['Nesprávně', 'Správně'])
plt.show()