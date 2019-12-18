import csv
import main
import json
import sys
from string import Template


def percent_rank(elements, value):
    cl = 0
    fi = 0
    for ele in elements:
        if value > ele:
            cl = cl + 1
        if value == ele:
            fi = fi + 1
    return (cl + (fi * 0.5)) / len(elements) * 100.0


# print(percent_rank([50.0, 65.0, 70.0, 72.0, 72.0, 78.0,
#                    80.0, 82.0, 84.01, 84.01, 85.0, 86.0, 88.0, 88.0,
#                    90.0, 94.0, 96.0, 98.0, 98.0, 99.0], 84.01))
landmarks = []
currentHits = []
landmarkScores = []
partialUpdateApi = 'https://vpc-srsdata-entity-996037dbb77d-yzau6raclfxc3kgbxxvjibwscm.ap-southeast-1.es.amazonaws' \
                   '.com/tvlk_entity_prod_read_alias/_update/{} '
entityInitialScrollApiUrl = 'https://vpc-srsdata-entity-996037dbb77d-yzau6raclfxc3kgbxxvjibwscm.ap-southeast-1.es.amazonaws' \
                            '.com/tvlk_entity_prod_read_alias/_search?scroll=10s'

entityInitialScrollApiBody = '{"size": 500,"query":{"match":{"pC":"LANDMARK"}},"sort":[{"s.ID_ID.p":{' \
                      '"order":"desc"}}],"_source":{"includes":["id","s.ID_ID.p"],"excludes":[]}} '

entityScrollApiUrl = 'https://vpc-srsdata-entity-996037dbb77d-yzau6raclfxc3kgbxxvjibwscm.ap-southeast-1.es.amazonaws' \
                            '.com/tvlk_entity_prod_read_alias/_search/scroll'
entityScrollApiBody = '{"size": 500,"scroll":"10s","scroll_id":"$scroll_id"}'

response = json.loads(main.post(entityInitialScrollApiUrl, entityInitialScrollApiBody).content)
currentHits = response['hits']['hits']
landmarks.extend(currentHits)
scroll_id = response["_scroll_id"]

while len(currentHits) > 0:
    Template(entityScrollApiBody).substitute(scroll_id=scroll_id)
    response = json.loads(main.post(entityScrollApiUrl, entityScrollApiBody).content)
    print(response)
    currentHits = response['hits']['hits']
    landmarks.extend(currentHits)
    scroll_id = response["_scroll_id"]
    print(len(landmarks))

for landmark in landmarks:
    landmarkScores.append(landmark['_source']['s']['ID_ID']['p'])

for landmark in landmarks:
    pS = percent_rank(landmarkScores,landmark['_source']['s']['ID_ID']['p'])
    partialUpdatePayload = json.dumps(dict(doc=dict(normProps=dict(pS=float(pS)))))
    try:
        main.post(str.format(partialUpdateApi, landmark['_source']['id']), partialUpdatePayload)
        print("updated id " + id + " ")
    except Exception as e:
        print("failed to partial update on " + id + " " + e)






