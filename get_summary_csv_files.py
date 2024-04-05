import os
import json
import pandas as pd

with open('config.json', 'r') as json_data:
    INFO = json.loads(json_data.read())

PATH = os.path.join("data","raw")
COLUMN_ORDER = INFO.get("column_order")
xwalk = pd.read_excel('data/filename-crosswalk-csv-files.xlsx')
xwalk = {
    x: y
    for x,y in zip(xwalk['original_filename'], xwalk['formatted_filename'])
}
df_final = pd.DataFrame()
df = pd.DataFrame(columns=COLUMN_ORDER)
for x in [x for x in os.listdir(PATH) if '.csv' in x]:
    
    fname = xwalk.get(x.replace(".csv", ""), None) # remove .csv if any
    print(fname)
    assert fname is not None, "You did not inteprete this filename"
    
    fname = fname.split("-")
    df['potw'] = [fname[0]]
    df['location'] = [fname[1]]
    df['year'] = [fname[2]]
    df['matrix'] = [fname[3]]
    df['size_fraction'] = [fname[5]]
    df['replicate'] = [fname[6]]
    df['morphology'] = [fname[7]]
    df['particleid'] = [f"{fname[0]}_{fname[1]}_Year-{fname[2]}_{fname[3]}_{fname[5]}_{fname[6]}_{fname[4]}"]
    df['chemicalid'] = [fname[8]]

    df['width_um'] = ''
    df['height_um'] = ''
    df['pct_matched'] = '0.61'
    df['predetermined_mp_yesno'] = ''
    df['hqi_exceed_sixty_yesno'] = 'y'
    df['notes'] = 'All samples have pct_matched greater than 60%. 0.61 is just a representative number. The actual pct_matched is not specified.'
    df['original_filename'] = [x]
    df_final = pd.concat(
        [
            df_final,
            df
        ]    
    )

df_final.sort_values(['potw','year','location','matrix','size_fraction','replicate']) \
    .to_excel('data/csv-summary-files.xlsx',index=False)