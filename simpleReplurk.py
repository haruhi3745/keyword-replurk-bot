import sys
import json
import time
import urllib.request 

from plurk_oauth import PlurkAPI

def replurkthem( pidlist ):
# 轉噗
  if len(pidlist) > 0:
    idstr = json.dumps(pidlist)  
    plurk.callAPI('/APP/Timeline/replurk', options={'ids': idstr})

if __name__ == '__main__':

  keyword = "#關鍵字"  
  pidlist = [] # 待轉噗清單  
  last_pid = 0 #上輪搜尋的最後一筆id
  continue_search = True
  offset = 0 # 搜尋結果從結果的第offset筆開始回傳
  max_pid = 0  # 這輪搜尋id最大那筆

  plurk = PlurkAPI.fromfile('API.keys')  

  while True:
    # 搜尋 回傳筆數：預設值
    search_result = plurk.callAPI('/APP/PlurkSearch/search', options={'query':keyword, 'offset':offset } )  

    while continue_search and search_result['has_more']: # 要繼續找而且確認有搜尋結果

      for each_plurk in search_result['plurks']:
        
        # 如果是之前檢查過的就跳出迴圈不找了
        if each_plurk['plurk_id'] <= last_pid  :  
          continue_search = False
          break

        # 確認未轉過、開放轉噗、噗首扣掉引用連結後有關鍵字
        if ( not each_plurk['replurked'] ) and each_plurk['replurkable'] and ( keyword in each_plurk['content_raw'] ) : 
          pidlist.append(each_plurk['plurk_id'])  


      # end for # 這次回傳的都找完了 或 不找了
      
      # 轉噗(怕轉噗有最大值限制先轉)
      replurkthem( pidlist )
      pidlist.clear() # 清空清單

      if offset == 0 : # 紀錄這輪初次搜尋最新一筆噗id
        max_pid = search_result['plurks'][0]['plurk_id']  

      if continue_search : # 這次回傳的都找完了，繼續找
        offset = search_result['last_offset']
        search_result = plurk.callAPI('/APP/PlurkSearch/search', options={'query':keyword, 'offset':offset } )  

      else: # 不找了
        last_pid = max_pid

    # end while #

    #休息30分
    time.sleep(60*30) 
    