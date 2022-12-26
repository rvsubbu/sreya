import pandas as pd
import requests

geo = requests.get("https://geosearch.planninglabs.nyc/v1/autocomplete?text=61 troutman")
data = geo.json()
#print(data["features"][0]["geometry"]["coordinates"])

requests311 = pd.read_csv("cleaned_311_data_hw2.csv")

filtered311 = requests311[requests311["latitude"].isna() & requests311["longitude"].isna() & requests311["incident_address"].notna() & requests311["borough"].notna()]
filtered311_30 = filtered311[['incident_address', 'borough', 'latitude', 'longitude']].head(30)
#print(filtered311_30)

def coord(row):
    if isinstance(row, str):
        geo = requests.get("https://geosearch.planninglabs.nyc/v1/autocomplete?text=" + row)
        try:
            data = geo.json()
            #return data["features"][0]["geometry"]["coordinates"]
            latlong = data["features"][0]["geometry"]["coordinates"]
            #print("latlong", latlong)
            return latlong[0], latlong[1]
        except:
            print("row:", row)
            return "invalid", "invalid"
            return ["invalid", "invalid"]
    else:
        return "invalid", "invalid"
        return ["invalid", "invalid"]

#print(coord("101 101 st"))

#filtered311_30[['latitude', 'longitude']] = filtered311_30['incident_address'].apply(coord)
#filtered311_30['latitude'], filtered311_30['longitude'] = filtered311_30['incident_address'].apply(coord)
filtered311_30['latlong'] = filtered311_30['incident_address'].apply(coord)
#print(filtered311_30['latlong'])

#df[['B1','B2']] = df['B'].apply(pd.Series)
filtered311_30[['longitude', 'latitude']] = filtered311_30['latlong'].apply(pd.Series)
#print(filtered311_30['latitude'])
#print(filtered311_30['longitude'])
filtered311_30.drop("latlong", axis=1, inplace=True)
print(filtered311_30.dtypes)
print(filtered311_30)

#filtered311_30['latitude'], filtered311_30['longitude'] = filtered311_30['latlong'].to_numpy()
#filtered311_30['latitude'] = filtered311_30['latlong'][0]
#filtered311_30['longitude'] = filtered311_30['latlong'][1]

