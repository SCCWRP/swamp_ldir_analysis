import pandas as pd
import json, os
import numpy as np

with open('config.json', 'r') as json_data:
    INFO = json.loads(json_data.read())

PATH = os.path.join("data","raw", "blanks")
COLUMN_ORDER = INFO.get("column_order")
FILENAME_DICT = pd.read_excel(os.path.join(os.getcwd(), "data", "filename-crosswalk-excel-files.xlsx"))
FILENAME_DICT = {
    x: y
    for x,y in zip(FILENAME_DICT['original_filename'], FILENAME_DICT['formatted_filename'])
}
df_final = pd.DataFrame()

for filename in [x for x in os.listdir(PATH) if '.xlsx' in x]:
    print(filename)
    
    # Read the file
    df = pd.read_excel(os.path.join(PATH, filename), sheet_name='Particles')

    # Only get the rows where there is no value in the Note column according to Sydney
    df = df[pd.isnull(df['Notes'])]

    # Read the interpretation of the filename
    info = FILENAME_DICT.get(os.path.splitext(filename)[0])

    assert info is not None, 'You did not interprete this filename'
    
    # Extract info from filenames
    info = info.split("-")
    potw = INFO.get(info[0][0].lower(), None)
    location = INFO.get(info[0][1].lower(), None)
    year = int(info[1].lower().replace("y",""))
    matrix = INFO.get(info[2].lower(), None)
    replicate = str(info[3]).replace("D","").replace("T","").replace("LG", "1")
    size_fraction = str(info[4]).replace("R","")
    additional_info = str(info[5] if len(info) >= 6 else "")
    
    # Making columns
    df["potw"] = potw
    df["year"] = year
    df["location"] = location
    df["matrix"] = matrix
    df["size_fraction"] = size_fraction
    df['replicate'] = replicate
    df['particleid'] = [f"{potw}_{location}_y{year}_{matrix}_{size_fraction}_rep{replicate}_{i}" for i in range(1, len(df) + 1)]
    df['chemicalid'] = df['Identification']
    df['chemical_type'] = ''
    df['width_um'] = df['Width (µm)']
    df['height_um'] = df['Height (µm)']
    df['morphology'] = ''
    df['pct_matched'] = df['Quality']
    df['predetermined_mp_yesno'] = ''
    df['hqi_exceed_sixty_yesno'] = np.where(df['pct_matched'] > 0.60, 'y', 'n')
    df['notes'] = df['Notes']
    df['original_filename'] = filename.replace(".xlsx","")
    df = df.assign(
        **{
            x: "" 
            for x in COLUMN_ORDER
            if x not in df.columns    
        }    
    )
    df = df[[x for x in COLUMN_ORDER]]
    df_final = pd.concat(
        [
            df_final,
            df
        ]    
    )
       
df_final.sort_values(['potw','year','location','matrix','size_fraction','replicate']) \
    .to_excel('data/excel-files-summary.xlsx',index=False)