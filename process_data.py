import pandas as pd
import pytz
df_product=pd.read_csv('source.csv')

df_product['Datetime'] = pd.to_datetime(df_product['Datetime'], utc=True)

df_product['Datetime'] = df_product['Datetime'].dt.tz_convert('Asia/Almaty')  # UTC+6


product_A = df_product[df_product['Name'] == 'ProductA'].copy()

product_B = df_product[df_product['Name'] == 'ProductB'].copy()


def Total_A(row):
    if row["Purity"]=="Impure":
        price=row['Price']*3/4
    else:
        price=row['Price']
    return row['Amount'] * price
    
product_A['total'] = product_A.apply(Total_A, axis=1)


product_B = product_B.merge(product_A[['Datetime', 'Price']], on='Datetime', suffixes=('B', 'A'))



def Total_B(row):
    if row["Purity"]=="Impure":
        price=row['PriceB']*3/4
    else:
        price=row['PriceB']-row['PriceA']
    return row['Amount'] * price

product_B['total'] = product_B.apply(Total_B, axis=1)


product_B=product_B[['Name', 'Datetime', 'Amount', 'PriceB', 'Purity', 'total']]
product_B.rename(columns={'PriceB': 'Price'}, inplace=True)

result = pd.concat([product_A, product_B], ignore_index=True)

result.to_csv("result.csv", index=False)

