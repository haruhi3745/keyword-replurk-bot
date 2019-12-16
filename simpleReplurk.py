import sys
import json
import time
import urllib.request 

from plurk_oauth import PlurkAPI

if __name__ == '__main__':

  keyword = "#關鍵字"  
  pidlist = [] # 待轉噗清單  

  plurk = PlurkAPI.fromfile('API.keys')  

  while True:
    # 搜尋 回傳筆數：預設值
    search_result = plurk.callAPI('/APP/PlurkSearch/search', options={'query':keyword } )  

    if search_result['has_more']: # 確認有搜尋結果

      for each_plurk in search_result['plurks']: 
        
        # 確認未轉過、開放轉噗、噗首扣掉引用連結後有關鍵字
        if ( not each_plurk['replurked'] ) and each_plurk['replurkable'] and ( keyword in each_plurk['content_raw'] ) : 
          pidlist.append(each_plurk['plurk_id'])  

    # 轉噗
    if len(pidlist) > 0:
      idstr = json.dumps(pidlist)  
      plurk.callAPI('/APP/Timeline/replurk', options={'ids': idstr})

    #休息30分
    time.sleep(60*30) 
    