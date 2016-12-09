# **Real-Stock-War**

这个游戏毫无疑问很好很强大！

虽然还没做完……

所以README后来再写吧！

## 新浪接口
http://hq.sinajs.cn/list=AUDCAD,AUDJPY,AUDUSD,CHFJPY,DINIW,EURCAD,EURCHF,EURGBP,EURJPY,EURUSD,GBPJPY,GBPUSD,NZDUSD,USDCAD,USDCHF,USDCNY,USDHKD,USDJPY,gb_dji,gb_ixic,hf_C,hf_CAD,hf_CL,hf_GC,hf_S,hf_SI,int_nikkei,rt_hkHSI
http://hq.sinajs.cn/?rn=1466266588386&list=AUDCAD,AUDJPY,AUDUSD,CHFJPY,DINIW,EURCAD,EURCHF,EURGBP,EURJPY,EURUSD,GBPJPY,GBPUSD,NZDUSD,USDCAD,USDCHF,USDCNY,USDHKD,USDJPY,gb_dji,gb_ixic,hf_C,hf_CAD,hf_CL,hf_GC,hf_S,hf_SI,int_nikkei,rt_hkHSI

货币缩写：http://www.easy-forex.com/au/zh-hans/currencyacronyms/

新浪 API：http://hq.sinajs.cn/list=

http://hq.sinajs.cn/ran=14785177617924297&format=json&list=theme_sh601015,theme_top3

http://vip.stock.finance.sina.com.cn/api/jsonp.php/var%20noticeData=/CB_AllService.getMemordlistbysymbol?num=8&PaperCode=601015

http://vip.stock.finance.sina.com.cn/api/jsonp.php/var%20noticeData=/CB_AllService.getMemordlistbysymbol?num=8&PaperCode=601015

http://vip.stock.finance.sina.com.cn/quotes_service/view/vML_DataList.php?asc=j&symbol=sh601015&num=11

http://hq.sinajs.cn/rn=1478508106794&list=s_sh000001,s_sz399001,CFF_RE_IC1611,rt_hkHSI,gb_$dji,gb_ixic,b_SX5E,b_UKX,b_NKY,hf_CL,hf_GC,hf_SI,hf_CAD

股票 新股 港股 美股 基金 期货 外汇 黄金 债券

http://vip.stock.finance.sina.com.cn/quotes_service/view/vML_DataList.php?asc=j&symbol=sh601015&num=11

## 数据结构

### App.gameData：游戏核心储存。

```json
App.gameData = {
    'stockCode_sh' = '',
    'new_data_sh' = '',
    'stockCode_sz' = '',
    'new_data_sz' = ''
}
```

### api_get_sinajs：

```json
code_raw_dict = {
    'code' = 'var hq_str_s_sh000001="上证指数,3230.1095,14.7437,0.46,1957242,21687605";'
}
```
### 股票

名称

今开

昨收

当前

最高

最低

买①

卖①

时间？

时间？

买①数量

买①价格

买②数量

买②价格

买③数量

买③价格

买④数量

买④价格

买⑤数量

买⑤价格

卖①数量

卖①价格

卖②数量

卖②价格

卖③数量

卖③价格

卖④数量

卖④价格

卖⑤数量

卖⑤价格

年月日

时分秒

？