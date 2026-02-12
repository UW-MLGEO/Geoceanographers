import earthaccess 
import pandas as pd 

#Request earthaccess login 
earthaccess.login()

#Pulls all binned l3 data for chl from NASA 
results = earthaccess.search_data(
    short_name="MODISA_L3m_NSST",
    temporal=("2010-01-01", "2020-12-31"),
)

#Filters only for the monthly data at 4km per square resolution 
filtered = [r for r  in results if "L3m.MO"  in r['meta']['native-id'] and "4km.nc" in r['meta']['native-id']]
print(len(filtered)) 
earthaccess.download(filtered[0], ".")  
