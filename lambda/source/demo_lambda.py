import os
import json
from pprint import pprint
from decimal import Decimal
from ddb import ddb_handler
from operator import itemgetter

DDB_INFERENCE_RES = os.environ['INFERENCE_RES_TABLE']
ddb_inf_res = ddb_handler(strTableName=DDB_INFERENCE_RES)

def get_similar_stores(nUserCode, sort_by_similarity=True):

    dicKey = {"store_id": nUserCode}
    dicRes = ddb_inf_res.get_item(dicKey)

    listInfo = dicRes["info"]
    if sort_by_similarity:
        listInfo = sorted(listInfo, key=itemgetter('유사도'), reverse=True)
    listSimStoreIDs = [int(dicInfo["유사판매처ID"]) for dicInfo in listInfo]

    return listSimStoreIDs

def get_recommedations():

    ## Your logic here
    ## things about the aurora here

    listRecomBestIDs = ["325396", "122762", "122751", "359769", "338779", "168337", "165245", "134571", "281558", "514939"]
    listRecomCrossIDs = ["278158", "101583", "159994", "252430", "157724", "118284", "132482", "107255", "177212", "224702"]
    listRecomManualIDs = ["516550", "324420", "209014", "809605", "162555", "372484", "171891", "373557", "170503", "373336"]

    return listRecomBestIDs, listRecomCrossIDs, listRecomManualIDs

def response_generator(listRecomBestIDs, listRecomCrossIDs, listRecomManualIDs):

    listResultData = []
    listResultData_append = listResultData.append

    for listRecomms, strType in zip([listRecomBestIDs, listRecomCrossIDs, listRecomManualIDs], ["best", "cross", "manual"]):
        for idx, strProductID in enumerate(listRecomms):
            dicRecord = {
                "productCode": strProductID,
                "recommendType": strType,
                "rank": str(idx+1),
            }
            listResultData_append(dicRecord)

    dicRes = {
        "resultCode": "200",
        "resultMsg": "Success",
        "resultData": listResultData
    }
    return dicRes


def lambda_handler(event, context):

    if not 'userCode' in event or not 'productInfo' in event or not 'option' in event:
       return {
           'statusCode': 200,
           'body': json.dumps('Error: Please specify all parameters (userCode, productInfo, option).')
       }
    
    print ("===============")
    pprint (f"Request: {event}")
    print ("===============")

    nUserCode = int(event["userCode"])
    listProductCode = event["productInfo"]["productCode"]
    dicOptions = event["option"]

    listSimStores = get_similar_stores(nUserCode, sort_by_similarity=True)
    listRecomBestIDs, listRecomCrossIDs, listRecomManualIDs = get_recommedations()

    print ("===============")
    pprint (f"userCode: {nUserCode}")
    pprint (f"productCode: {listProductCode}")
    pprint (f"option: {dicOptions}")
    pprint (f"store IDs similar to user code: {listSimStores}")
    print ("===============")

    #print (dicResponse)
    #print (json.dumps(dicResponse))
    return json.dumps(response_generator(listRecomBestIDs, listRecomCrossIDs, listRecomManualIDs))
