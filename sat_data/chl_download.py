import earthaccess 

earthaccess.login() 
temporal_bounds = (
    "2013-10-06",
    "2025-12-31"
)

#Start time 2013-16-06, end time 2025-12-16 
results = earthaccess.search_data(short_name="MODISA_L3m_CHL", 
                                 temporal = temporal_bounds)

earthaccess.download(results, local_path = "./chl_buoytimespan", show_progress = True) 
