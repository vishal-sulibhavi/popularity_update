import csv
import main
import json

entityTypeToIdPrifix = {'GEO': 'LOCAL_GEO', 'EXPERIENCE': 'EXPERIENCE', 'CULINARY': 'CULINARY_RESTAURANTS',
                        'HOTEL': 'ACCOM_HOTELS'}

partialUpdateApi = 'https://vpc-srsdata-entity-996037dbb77d-yzau6raclfxc3kgbxxvjibwscm.ap-southeast-1.es.amazonaws.com/tvlk_entity_index_norm_pscore/_update/{}'

f = open("errorIds.txt", "a")

f.close()
with open('product_and_geo_popularity_score.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    skip = True
    for row in csv_reader:
        if skip:
            skip = False
            continue
        id = entityTypeToIdPrifix[row[1]] + "_" + row[0]
        popKeyValue = [""]
        partialUpdatePayload = json.dumps(dict(doc=dict(normProps=dict(pS=float(row[5])))))
        print(id)
        try:
            main.post(str.format(partialUpdateApi,id),partialUpdatePayload)
        except:
            f.write(id + " " + partialUpdatePayload)
f.close()

