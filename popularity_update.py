import csv
import main
import json
import sys

entityTypeToIdPrifix = {'GEO': 'LOCAL_GEO', 'EXPERIENCE': 'EXPERIENCE', 'CULINARY': 'CULINARY_RESTAURANTS',
                        'HOTEL': 'ACCOM_HOTELS'}

partialUpdateApi = 'https://vpc-srsdata-entity-996037dbb77d-yzau6raclfxc3kgbxxvjibwscm.ap-southeast-1.es.amazonaws.com/tvlk_entity_prod_read_alias/_update/{}'
csvFileName = sys.argv[1]
print(csvFileName)
with open(csvFileName) as csv_file:
    csv_reader = csv.reader(csv_file)
    skip = False
    for row in csv_reader:
        if skip:
            skip = False
            continue
        if float(row[5]) <= 0.0:
            continue
        id = entityTypeToIdPrifix[row[1]] + "_" + row[0]
        popKeyValue = [""]
        partialUpdatePayload = json.dumps(dict(doc=dict(normProps=dict(pS=float(row[5])))))
        print(id)
        try:
            main.post(str.format(partialUpdateApi,id),partialUpdatePayload)
        except Exception as e:
            print("failed to partial update on " + id +" " + e )
