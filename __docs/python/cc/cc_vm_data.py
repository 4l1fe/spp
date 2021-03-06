# -- coding: utf-8 -*-
%load_ext autoreload
%autoreload
import os, sys
DIRCWD=  'G:/_devs/project27/' if sys.platform.find('win')> -1   else  '/home/ubuntu/notebook/' if os.environ['HOME'].find('ubuntu')>-1 else '/media/sf_project27/'
os.chdir(DIRCWD); sys.path.append(DIRCWD + '/aapackage'); # sys.path.append(DIRCWD + '/linux/aapackage')
execfile( DIRCWD + '/aapackage/allmodule.py')
import util,  numpy as np, gc
import  pandas as pd, sqlalchemy as sql, dask.dataframe as dd, dask, datanalysis as da, arrow
from attrdict import AttrDict as dict2
from collections import defaultdict
############################################################################################


######################### FOLDERS ##########################################################
execfile( DIRCWD + '/aapackage/coke_functions.py')
execfile( DIRCWD + '/unerry/cc_folders.py')



#### 1) Read CSV FULL: partial columns,   ##################################################
'''  2016 : '/vm_csv/2016/area_all_2016_BIG.txt
2015 :  /vm_csv/2015/area_all_2015.txt'
2014:   /vm_csv/2014/area_all_2014.txt

'''
df2= pd.read_csv(uri.raw+ '/vm_csv/2015/area_all_2015.txt', nrows=10**8)       
gc.collect()       
df.fillna(0, inplace=True)

util.pd_info(df)     ;   util.pd_dtypes(df, returnasdict=0)



###### HOT / COLD separate   ###############################################################
df.columns
Index([u'-RowNum-', u'お得意様CD', u'お得意様名', u'ロケCD', u'FS納品場所CD', u'FS納品場所名',
       u'取引開始年月日_FS物流管理', u'取引終了年月日_FS物流管理', u'戦略チャネル階層4CD', u'戦略チャネル階層4名',
       u'統合商品CD', u'統合商品名', u'HOTCOLD区分', u'HOTCOLD区分名', u'バラ_2015年10月',
       u'バラ_2015年11月', u'バラ_2015年12月', u'バラ_2016年01月', u'バラ_2016年02月',
       u'バラ_2016年03月', u'バラ_2016年04月', u'バラ_2016年05月', u'バラ_2016年06月',
       u'バラ_2016年07月', u'バラ_2016年08月', u'バラ_2016年09月', u'バラ_2016年10月',
       u'バラ_2016年11月', u'バラ_2016年12月', u'total', u'product_type',
       u'product_size', u'total_bottl', u'local_basho', u'inout', u'bashotype',
       u'total_summer', u'total_winter'],

       
df1= df[[ '統合商品CD', '統合商品名', 'HOTCOLD区分', 'HOTCOLD区分名'   ]].drop_duplicates()
 

###  
df3= pd.concat( (df[[ '統合商品CD', '統合商品名', 'HOTCOLD区分', 'HOTCOLD区分名'   ]], df2[[ '統合商品CD', '統合商品名', 'HOTCOLD区分', 'HOTCOLD区分名'   ]]    ) )         
df3= df3.drop_duplicates()
df3.to_csv('G:/_project/CCWJ/MASTER/product_list_fromSKUsales.txt', index=0)


''' Same SKU, but HOT/COLD Flag is differnt  ''''











       
       


##### Add missing files  ###################################################################
df= pd.read_csv(uri.raw+ r'/vm_csv/2015_201605/csv/44_utf8.txt', nrows=10**8)    
gc.collect()  ; df.columns   


df1= pd.read_csv(uri.raw+ r'/vm_csv/2015_201605/csv/34_1_utf8.txt', nrows=10**8)      
gc.collect()  
df1.columns  

df.columns == df1.columns

df1.columns=  df.columns

df= pd.concat((df,df1), axis=0 )


#####
# df.to_csv(uri.raw+ r'/vm_csv/2015/area_all_2015_big.txt', index=False, mode='w')







##### Select only CC Brand  ################################################################
usecols=[ "FS納品場所CD",  '統合商品名', 
'バラ_2016年04月', 'バラ_2016年05月', 'バラ_2016年06月',  'バラ_2016年07月', 
'バラ_2016年08月',  'バラ_2016年09月', 'product_type'    
]

df2= df2[  usecols   ]
df= df[  usecols   ]


mlist= df["FS納品場所CD"].unique()
mlist2= df2["FS納品場所CD"].unique()
set.intersection(set(mlist) ,  set(mlist2))    



#####Merge
df3= pd.concat((df, df2), axis=0)
len(df3["FS納品場所CD"].unique())
# Unique VM 292534
len(mlist) + len(mlist2)


def add_id(x) :
  try :  return int(x)
  except:   return -1
   
   
df["FS納品場所CD"]= df["FS納品場所CD"].apply( add_id)
df2= df[  df["FS納品場所CD"] != -1 ]
df= df2


# df3.to_csv(uri.raw+ r'/vm_csv/20170120/area_ALL_Summer.txt', index=False)
#  compression="gzip", encoding="utf-8"

df= df3


############################################################################################
# mlist2[0]
# 400036164 in mlist
df["FS納品場所CD"].values[8556]


def iscol_exist(x):
   try :
      if x in mlist :
         return 1
      else :
         return 0
   except: 
      return 0


df2['isexist']=  df2["FS納品場所CD"].apply( iscol_exist  ) 



############################################################################################
'''
df1= pd.read_csv(uri.raw+ '/vm_csv/a_34__20.txt', nrows=10**8) 
df2= pd.read_csv(uri.raw+ '/vm_csv/a_34_out_20.txt', nrows=10**8) 
df3= pd.read_csv(uri.raw+ '/vm_csv/a_41.txt', nrows=10**8) 
df4= pd.read_csv(uri.raw+ '/vm_csv/a_42.txt', nrows=10**8) 

dfa= pd.concat((df1, df2, df3, df4 ), ignore_index=False, axis=0)

dfmi=  dfa[  dfa['FS納品場所CD']== 400000991  ] 
dfa.fillna(0, inplace=True)

gc.collect()

dfa['FS納品場所CD']= dfa['FS納品場所CD'].astype('int64')

util.pd_info(dfa)

df1.columns

dfmi=  dfa[  dfa['FS納品場所CD']== 400000991.0  ]

dfmi.to_csv(uri.raw+ '/vm_csv/a400000991.txt', index=False)

df.to_csv(uri.raw+ '/vm_csv/20170120/4334with20a41a34out20_NEW.txt', index=False, mode='w') 
'''





############################################################################################
#### Generate Product_Code JS_code for VM files ############################################
df= pd.read_csv(uri.raw+ r'/vm_csv/area_ALL_BIG.txt', nrows=10**8)   






############################################################################################
df1= df[[ '統合商品CD' , '統合商品名', 'product_type'  ]]
df1.drop_duplicates( '統合商品名',    inplace= True)
df1.to_csv( uri.map + '/map_vm_jscode_name_2015.txt', mode='w' )


df1= df1[ df1.product_type == -1]
df1.to_csv( uri.map + '/map_vm_jscode_name_2015_missing.txt', mode='w' )



def isint(x):
   try : return int(x)
   except: return -1

df['isint']= df['統合商品CD'].apply(isint)


df['統合商品CD'].astype(str)





####  Cannot Print the dataframe   #########################################################
'''         
お得意様CD object <type 'str'> 0K13000003
お得意様名 object <type 'str'> ニュースターコミュニケーションズ株式会社
ロケCD int64 <type 'numpy.int64'> 1
FS納品場所CD int64 <type 'numpy.int64'> 400036164
FS納品場所名 object <type 'str'> ニュースターコミュニケーションズ
取引開始年月日_FS物流管理 float64 <type 'numpy.float64'> 20150615.0
取引終了年月日_FS物流管理 float64 <type 'numpy.float64'> 99991231.0
戦略チャネル階層4CD int64 <type 'numpy.int64'> 31110
戦略チャネル階層4名 object <type 'str'> KO機
統合商品CD float64 <type 'numpy.float64'> 19404.0
統合商品名 object <type 'str'> ﾘｱﾙｺﾞｰﾙﾄﾞ 缶 190ml (0608)
HOTCOLD区分 float64 <type 'numpy.float64'> 1.0
HOTCOLD区分名 object <type 'str'> コールド
バラ_2015年02月 float64 <type 'numpy.float64'> 0.0
バラ_2015年03月 float64 <type 'numpy.float64'> 0.0
バラ_2015年04月 float64 <type 'numpy.float64'> 0.0
バラ_2015年05月 float64 <type 'numpy.float64'> 0.0
バラ_2015年06月 float64 <type 'numpy.float64'> 0.0
バラ_2015年07月 float64 <type 'numpy.float64'> 8.0
バラ_2015年08月 float64 <type 'numpy.float64'> 0.0
バラ_2015年09月 float64 <type 'numpy.float64'> 0.0
バラ_2015年10月 float64 <type 'numpy.float64'> 0.0
バラ_2015年11月 float64 <type 'numpy.float64'> 2.0
バラ_2015年12月 float64 <type 'numpy.float64'> 0.0
バラ_2016年01月 float64 <type 'numpy.float64'> 2.0
バラ_2016年02月 float64 <type 'numpy.float64'> 7.0
バラ_2016年03月 float64 <type 'numpy.float64'> 5.0
バラ_2016年04月 float64 <type 'numpy.float64'> 6.0
バラ_2016年05月 float64 <type 'numpy.float64'> 8.0
'''



##### 1) dtype0   definition   #############################################################
dtype0= { 'QTSeq':'int64', 
'お得意様CD':'object', 'お得意様名':'object', 'ロケCD':'int64', 
'FS納品場所CD':'object', 
'FS納品場所名':'object', '取引開始年月日_FS物流管理':'float32', 
'取引終了年月日_FS物流管理':'float32', '戦略チャネル階層4CD':'float32', '戦略チャネル階層4名':'object', 
'統合商品CD':'float32',
'統合商品名':'object', 'HOTCOLD区分':'float32', 
'HOTCOLD区分名':'category', 'バラ_2015年02月':'int32', 'バラ_2015年03月':'float32', 
'バラ_2015年04月':'float32', 'バラ_2015年05月':'float32', 'バラ_2015年06月':'float32', 
'バラ_2015年07月':'float32', 'バラ_2015年08月':'float32', 'バラ_2015年09月':'float32', 
'バラ_2015年10月':'float32', 'バラ_2015年11月':'float32', 'バラ_2015年12月':'float32', 
'バラ_2016年01月':'float32', 'バラ_2016年02月':'float32', 'バラ_2016年03月':'float32', 
'バラ_2016年04月':'float32', 'バラ_2016年05月':'float32' }



#### 1) mapping vm_drink  ---->  obppc_drink ###############################################
usecols=[ "FS納品場所CD",  '統合商品名', 
'バラ_2016年04月', 'バラ_2016年05月', 'バラ_2016年06月',  'バラ_2016年07月', 
'バラ_2016年08月',  'バラ_2016年09月', 'product_type'    
]


df= pd.read_csv(uri.raw+ '/vm_csv/20170120/4334with20a41a34out20_NEW.txt',  usecols= usecols, nrows=2*10**8)           
gc.collect()     




###################  Data   ################################################################
dfmi= df[  df[  "FS納品場所CD" ]== 400000991  ]

dfmi.to_csv( uri.raw +'/obppc_csv/b_400000991.csv', index=False  )

dfmi= df_ccwj[  df_ccwj[  "FS納品場所CD" ]== 400000991  ]




############################################################################################
#### 1) Add product_type Column + SKU Size #################################################
########### Product Category / Product Size  ###############################################
df_product= pd.read_csv( uri.map + '/map_cokeon_productname_master.txt')
df_product.columns
''' Index([u'js_code', u'product_name', u'brand_en_name', u'brand_name',
       u'product_type', u'SKU_name', u'canpet', u'bottle_size'],
'''

map_canpet=     util.pd_df_todict(df_product, colkey= "js_code" , colval= "canpet" )  
map_bottlesize= util.pd_df_todict(df_product, colkey= "js_code" , colval= "bottle_size" )  
map_productype= util.pd_df_todict(df_product, colkey= "js_code" , colval= "product_type" )  


def add_canpet(js_code) :
   try :      return map_canpet[js_code]
   except :   return ''

def add_bottlesize(js_code) :
   try :      return int(map_bottlesize[js_code])
   except :   return 0


def add_productype(js_code) :
   try :      return map_productype[js_code]
   except :   return ''
   

df_sku["canpet"]=      df_sku["統合商品CD"].apply(add_canpet      ).astype('category') 
df_sku["bottlesize"]=  df_sku["統合商品CD"].apply(add_bottlesize  ).astype('int16') 
df_sku["productype"]=  df_sku["統合商品CD"].apply(add_productype  ).astype('category') 

df_sku.columns
col0= [  'お得意様CD', 'お得意様名', 'ロケCD', 'FS納品場所CD', 
        '戦略チャネル階層4CD', 
       '統合商品CD', 'HOTCOLD区分', 'バラ_2015年02月',
       'バラ_2015年03月', 'バラ_2015年04月', 'バラ_2015年05月', 'バラ_2015年06月',
       'バラ_2015年07月', 'バラ_2015年08月', 'バラ_2015年09月', 'バラ_2015年10月',
       'バラ_2015年11月', 'バラ_2015年12月', 'バラ_2016年01月', 'バラ_2016年02月',
       'バラ_2016年03月', 'バラ_2016年04月', 'バラ_2016年05月', 'productype',
       'canpet', 'bottlesize']

       
       
df_sku=  df_sku[col0]

'''
df_cate=
map_product_cate= da.csv_todictmap(uri.map + 'map_vm_productname_category.txt') 
map_product_cate2= map_product_cate['type_cokeon'] 

def addcol_productcat(x) :
   try :   return  map_product_cate2[x]
   except : return -1

df_sku['product_type']= df_sku['統合商品名'].apply(addcol_productcat)
df.product_type.unique()

def addcol_productsize(x) :
   try :   return  map_product_cate['SKU_size'][x]
   except : return -1

df['product_size']= df['統合商品名'].apply(addcol_productsize)
print  df.columns


df_err= df[ df.product_size == -1]
df_err.head()
'''


####### Missing product ####################################################################
vm_basho_code= df[ "FS納品場所CD"].unique()


vm_basho_code_dict= {}
for x in vm_basho_code :
   vm_basho_code_dict[x]= 1


#### is CCWJ
def addcol_isccwj(x) :
   try :   return  vm_basho_code_dict[x]
   except : return -1

df['is_ccwj2']= df["FS納品場所CD" ].apply(addcol_isccwj)




######### Missing Product ##################################################################
df_missing=  df[ (df.is_ccwj2 == 1) &  (df.product_type == '-1') ]
            
aa= df_missing[  '統合商品名' ].unique()                
                
pd.DataFrame(aa, columns=['product_name']).to_csv(uri.raw + '/obppc_csv/product_missing.csv')
               
dfmi= df[  df[  "FS納品場所CD" ]== 400000991  ]

dfmi[  df.product_type == '-1'   ]


df.columns



##### Select only CC Brand  ################################################################
df_ccwj=  df[ df.product_type != -1 ]


usecols=[ "FS納品場所CD",  '統合商品名', 
'バラ_2016年04月', 'バラ_2016年05月', 'バラ_2016年06月',  'バラ_2016年07月', 
'バラ_2016年08月',  'バラ_2016年09月', 'product_type'    
]

df= copy.deepcopy( df_ccwj[  usecols   ])


# df.to_csv(  'G:/_data/raw/obppc_csv/df_vm_summer_2016_final.csv', index=False, mode='w'  )







########## SUMMER 2017 STUDY ###############################################################
####### USE THIS ONE     ###################################################################
df= pd.read_csv(  'G:/_data/raw/vm_csv/area_ALL_summer_final.csv' )
gc.collect()



####Aggregate the Months  ##################################################################
df.fillna(0, inplace=True)
df["FS納品場所CD"]= df["FS納品場所CD"].astype('int64')
df['バラ_2016年04月']= df['バラ_2016年04月'].astype('float32')
df['バラ_2016年05月']= df['バラ_2016年05月'].astype('float32')
df['バラ_2016年06月']= df['バラ_2016年06月'].astype('float32')
df['バラ_2016年07月']= df['バラ_2016年07月'].astype('float32')
df['バラ_2016年08月']= df['バラ_2016年08月'].astype('float32')
df['バラ_2016年09月']= df['バラ_2016年09月'].astype('float32')

df['バラ_2016年04月']= df['バラ_2016年04月'].astype('int32')
df['バラ_2016年05月']= df['バラ_2016年05月'].astype('int32')
df['バラ_2016年06月']= df['バラ_2016年06月'].astype('int32')
df['バラ_2016年07月']= df['バラ_2016年07月'].astype('int32')
df['バラ_2016年08月']= df['バラ_2016年08月'].astype('int32')
df['バラ_2016年09月']= df['バラ_2016年09月'].astype('int32')


df['total']= df['バラ_2016年04月'] + df['バラ_2016年05月']+ df['バラ_2016年06月'] + df['バラ_2016年07月'] + df['バラ_2016年08月']  + df['バラ_2016年09月']
df['total']= df['total'].astype('int32')


df['product_size']= df['product_size'].astype('int32')
df['total2']= df['total'] * df['product_size']   #Bottle


#   df.to_csv(  'G:/_data/raw/vm_csv/area_ALL_summer_final.csv', index=False, mode='w'  )



############################################################################################
##### Per product_type RANKING #############################################################
product0= 'ENERGY'
df_1= df[ df.product_type==  product0 ]

df_pivot1= pd.pivot_table(df_1, index="FS納品場所CD", columns='product_type', 
                          values='total', aggfunc='sum' )


df_pivot1.sort_values( by = [ product0 ], ascending= 0, inplace= True)


######
df_pivot1.to_csv( uri.raw + '/newproduct_csv/VM_'+product0+'_ranking.csv', index=True, mode='w'  )



#####
'''
array([-1, 'COCA', 'ENERGY', 'WATER', 'JUICE', 'NST', 'COFFEE', 'SPORTS',
       'SSD', 'OTHER', 'BLACK TEA', 'LACTIC'], dtype=object)

'''







############ Per VM : Bottle Calculation     ############################################### 
df_pivot1= pd.pivot_table(df, index="FS納品場所CD", columns='product_type', 
                          values='total', aggfunc='sum' )

gc.collect()
df_pivot1.fillna(0, inplace=True)


df_pivot1['total_bottle']= df_pivot1.apply(lambda row : np.sum(row), axis=1)

for icol in [u'BLACK TEA', u'COCA', u'COFFEE', u'ENERGY', u'JUICE', u'LACTIC',  u'NST', u'OTHER', u'SPORTS', u'SSD', u'WATER']   :              
   df_pivot1[ icol + '_w']=  df_pivot1[icol] * 1.0 / df_pivot1['total_bottle']

df_pivot1.sort_values(by=['total_bottle'], inplace=True, ascending= False)


df_pivot1.to_csv(uri.raw+'/obppc_csv/pivot_vm_machine_productype_201604_201612_bottle.csv', mode='w')






########## Per VM : SKU Calculation     ####################################################
df_pivot1= pd.pivot_table(df, index="FS納品場所CD", columns='product_type', 
                          values='total', aggfunc='sum' )

gc.collect()
df_pivot1.fillna(0, inplace=True)

df_pivot1['total_SKU']= df_pivot1.apply(lambda row : np.sum(row[0:11]), axis=1)

for icol in [u'BLACK TEA', u'COCA', u'COFFEE', u'ENERGY', u'JUICE', u'LACTIC',  u'NST', u'OTHER', u'SPORTS', u'SSD', u'WATER']   :              
   df_pivot1[ icol + '_w']=  df_pivot1[icol] * 1.0 / df_pivot1['total_SKU']

df_pivot1.sort_values(by=['total_SKU'], inplace=True, ascending= False)


df_pivot1.to_csv(uri.raw+'/obppc_csv/pivot_vm_machine_productype_area4443_201604_201612_SKU.csv', mode='w')





############################################################################################
###### Manual check ########################################################################
df= pd.read_csv('G:/_data/raw/obppc_csv/df_vm_summer_2016_final.csv')

df["FS納品場所CD"]= df["FS納品場所CD"].astype('int64')
df['total']=  df['total'].astype('int32')
df['total2']= df['total2'].astype('int32')
df['統合商品名']= df['統合商品名'].astype('category')



basho_list= [  100026162,100164569,100819794,200004240,200009018,200015289,200028128,200034515,200036885,200040064,200042987,200046887,200049156,200050130,200050954,200053116,200063258,200064938,200066435,200066786,200071588,200071855,200075237,200077373,200117641,200153028,200164798,200164801,200393967,200427284,200475017,200580837,200580952,200586264,200587663,200588552,200591990,200592033,200592244,200592434,200593359,200593924,200596636,200597531,200597787,200599297,200599342,200599397,200599495,200600322,200600480,200600580,200600603,200600609,200601958,200602121,200602209,200602258,200602613,200603812,200605791,200607145,200607191,200674222,200704229,200785377,200897701,201701894,201703455,201703501,201703528,201703552,201703625,201711768,201738526,201743910,201744569,201778846,202501139,202750244,202757958,202763001,202775921,202775948,202780917,202789299,203200137,210301132,210326741,210402183,210611110,210703760,211304170,215356920,215759630,215773700,215778620,216072210,230001794,230011137,230054987,230069760,230079858,230080705,230082554,230105007,230111015,230111260,230126616,230135909,230136468,230140476,230147036,230154911,230172561,230221786,230247971,230273619,230294058,230380213,230392769,230425365,230478299,230487476,230490027,230490248,230520848,230526951,230564306,230602046,230616721,230632468,230648844,230675949,230694838,230724044,230739203,230768289,230774505,230778233,230787852,230799907,230802444,230818502,230854231,232123186,400000075,400000991,400003099,400005843,400005884,400006420,400007767,400010593,400013075,400015986,400016075,400016076,400016261,400019427,400020395,400020987,400026452,400026753,400027636,400036032,400036328,400036790,400037171,400037553,400039678,400039680,400039901,400040400,400047252,400048931,400049356,400049364,400049365,400049366,400049378,400049386,400049389,400052465,400052924,400054180,400054417,400064236,400064595,400064714,400064722,400064821,400064827,400066647,400067147,400067150,400068835,400068878,400069200,400070038,400070358,400070702,400071113,400071337,400071779,400072207,400072600,400072662,400073148,400074213,400074251,400075426
 ]

# df_all= dfi


basho_id=  325341401  
dfi= df[  df["FS納品場所CD"]==    basho_id  ]



basho_id=  
df_all= None

for basho_id in basho_list :
  dfi= df[  df["FS納品場所CD"]==    basho_id  ]
  dfi.sort_values(by= 'total', ascending=False, inplace= True)
  dfi['rank']=   np.arange(0, len(dfi)) + 1  

  if df_all is None :
     df_all= dfi
  else :   
     df_all= pd.concat((df_all, dfi  ), axis=0) 


     

df_all.to_csv(  uri.raw+'/obppc_csv/check_all.csv'  )






 dfi[['FS納品場所CD', '統合商品名',  'product_type', 'total'    ]]


















#############################################################################################
df_pivot1.columns



util.save(df_pivot1, uri.raw+'/obppc_csv/pivot_vm_machine_obppctype_201604_201612.pkl')



df1= copy.deepcopy(df_pi)
 



############################################################################################
###### Manual check ########################################################################
df= pd.read_csv('G:/_data/raw/obppc_csv/VM_CCWJ_summer_2016.csv')

df["FS納品場所CD"]= df["FS納品場所CD"].astype('int64')
df['total']=  df['total'].astype('int32')
df['total2']= df['total2'].astype('int32')
df['統合商品名']= df['統合商品名'].astype('category')


df.columns


basho_id= 400026452


dfi= df[  df["FS納品場所CD"]==    basho_id  ]
dfi.to_csv(  uri.raw+'/obppc_csv/summer_check_'+ str(basho_id) +'.csv'  )



#  df.to_csv(  'G:/_data/raw/obppc_csv/VM_CCWJ_summer_2016.csv', index=False, mode='w'  )


df.columns
gc.collect()

############################################################################################
###### WATER Selection #####################################################################

df_water= df[  df["product_type"]==   'WATER'  ]



df_water2= pd.pivot_table(df_water, index="FS納品場所CD", columns='product_type', 
                          values='total2', aggfunc='sum' )

df_water2.sort_values(by=['WATER'], ascending=0, inplace= True)

df_water2.to_csv(  'G:/_project/CCWJ/SHIN_SHOUHIN/WATER/vmsales_water_ranking.csv '  )


 os.environ['COMPUTERNAME']



### read dict  mapping vm_drink  ---->  obppc_drink #####################################################################
in5= r'G:/_project/cokeon/OBPPC/'
vv= pd.read_csv(in5 +  'mapping_product_vm_obppc_type.txt' )
vv= vv.values

dmap= util.np_dictordered_create()
sh= np.shape(vv)
for i in xrange(0, sh[0]) :
  dmap[ vv[i,0] ] = vv[i, 1]


def getobbpc(x) :
   try : return dmap[ x ]
   except :   return -1   


#### Apply       
df['obppc_type']= df['統合商品名'].apply(getobbpc)        
      
      
len(df['obppc_name'].unique())
df2= df.loc[  df['obppc_name']  !=  -1 ]


print df2.iloc[15552, 1],  df2.iloc[15552, 8],  df2.iloc[15552, 9:], 







######  Test Mapping    ###################################
v = df[ '統合商品名'].values
for i in xrange(0, 1*10**6) :
   try :
      print dmap[ v[i] ]
   except : pass







for i in xrange(0, 2*10**6) :
   try :
      dmap[ df.iloc[i, 1] ]
      
   except : pass



5 + 6




for k,x in dmap.items():
   print k

   
   
   


  
############################################################################################
da.csv_col_get_dict_categoryfreq()



#### 1) Pivot Machine__Drink__SKU_volume  ##################################################
usecols=[ "FS納品場所CD", '統合商品CD', 
'バラ_2016年04月', 'バラ_2016年05月', 'バラ_2016年06月',  'バラ_2016年07月', 
'バラ_2016年08月',  'バラ_2016年09月'    
]



df= pd.read_csv(in4+ '4334with20a41a34out20_.txt', dtype= dtype0, usecols= usecols, nrows=10**8)           
gc.collect()       
util.pd_info(df)     
df.head()

df.fillna(0, inplace=True)
df["FS納品場所CD"]= df["FS納品場所CD"].astype('int64')
df['統合商品CD']= df['統合商品CD'].astype('int32')
df['バラ_2016年04月']= df['バラ_2016年04月'].astype('int32')
df['バラ_2016年05月']= df['バラ_2016年05月'].astype('int32')
df['バラ_2016年06月']= df['バラ_2016年06月'].astype('int32')
df['バラ_2016年07月']= df['バラ_2016年07月'].astype('int32')
df['バラ_2016年08月']= df['バラ_2016年08月'].astype('int32')
df['バラ_2016年09月']= df['バラ_2016年09月'].astype('int32')

df['total']= df['バラ_2016年04月'] + df['バラ_2016年05月']+ df['バラ_2016年06月'] + df['バラ_2016年07月'] + df['バラ_2016年08月']  + df['バラ_2016年09月']



df_pivot1= pd.pivot_table(df, index="FS納品場所CD", columns='統合商品CD', 
                          values='total', aggfunc='sum' )
gc.collect()
df_pivot1.fillna(0, inplace=True)
df_pivot1.to_csv(out1+'pivot_vm_machine_product_skuvol_201604_201612.csv')
util.save(df_pivot1, 'df_pivot1_ref')




#### 2) Pivot Location__Drink__SKU_volume  ###########################################
usecols=[ "FS納品場所CD", '統合商品名', 
'バラ_2016年04月', 'バラ_2016年05月']
         
         
df= pd.read_csv(in3+ '44_utf8.txt', dtype= dtype0, usecols= usecols, nrows=10**8)           
gc.collect()       
util.pd_info(df)     
df.head()

df.fillna(0, inplace=True)
df["FS納品場所CD"]= df["FS納品場所CD"].astype('int64')
df['統合商品CD']= df['統合商品CD'].astype('int32')
df['バラ_2016年04月']= df['バラ_2016年04月'].astype('int32')
df['バラ_2016年05月']= df['バラ_2016年05月'].astype('int32')

df['total']= df['バラ_2016年05月'] + df['バラ_2016年04月']


df_pivot1= pd.pivot_table(df, index="FS納品場所CD", columns='統合商品CD', 
                          values='total', aggfunc='sum' )
gc.collect()
df_pivot1.fillna(0, inplace=True)
df_pivot1.to_csv(out1+'pivot_vm_machine_product_skuvol.csv')
util.save(df_pivot1, 'df_pivot1_ref')




#### 2) Get unique names  ###################################################################

#### 1) Pivot Machine__Drink__SKU_volume  ###########################################
usecols=[ '統合商品名', '統合商品CD']
         


df= pd.read_csv(in4+ '4334with20a41a34out20_.txt', dtype= dtype0, usecols= usecols, nrows=10**8)           
gc.collect()       
util.pd_info(df)     
df.head()


a= df['統合商品名'].unique()
print a

pd.DataFrame(a, columns=['col']).to_csv(in3+ 'all_product_name.txt')









################## User filter  ########################################################
# df= df.astype(dtype0)
dtype0= {'amount': 'int16',
 'area_code': 'int32',
 'bottler_code': 'int16',
 'bottler_name': 'category',
 'id': 'int32',
 'js_code': 'int32',
 'location_code': 'int32',
 'machine_code': 'int64',
 'price': 'int16',
 'product_name': 'category',
 'promotion_id': 'float16',
 'purchased_at': 'object',
 'temperature': 'int16',
 'user_id': 'int32'}


### CCWJ  :   Bottler code


###########################################################################################  
from collections import defaultdict
import arrow
fmt='YYYY-MM-DD'

def np_list_tofreqdict(l1) :
   dd= dict()
   for x in l1 :
     try :    dd[x]+= 1
     except : dd[x]=1
   return dd
   
def date_diffstart(t) : return date_diffsecond(str_t1=t, str_t0=t0)
def date_diffend(t) :   return date_diffsecond(str_t1=t1, str_t0=t)
   
def date_diffsecond(str_t1, str_t0, fmt='YYYY-MM-DD HH:mm:SS') :
   dd= arrow.get(str_t1, fmt) - arrow.get(str_t0, fmt) 
   return dd.total_seconds()

 
def np_dict_tolist(dd) :
    return [ val  for _, val in dd.items() ]
            
def np_dict_tostr_val(dd) :
    return ','.join([ str(val)  for _, val in dd.items() ])
         
def np_dict_tostr_key(dd) :
    return ','.join([ str(key)  for key,_ in dd.items() ])


   
   
    
############################################################################################
##### Excel User Group   Export  to csv   ##################################################
user_group= pd.read_csv(in3 + 'user_group.csv',  nrows=10**8)    
user_group.set_index('user_id', inplace=True)
user_group= user_group.to_dict('dict')['rank_volume'] 
gc.collect()       
   

### assign in dataframe   ###############################
usecols=["user_id", "machine_code", "location_code",  "bottler_code", 'product_name', 
         'temperature', "amount",'purchased_at', 'user_rank_vol']
         
df= pd.read_csv(in2+ 'purchasings_user.csv', dtype= dtype0, usecols= usecols, nrows=10**8)       
df['user_rank_vol']= df['user_id'].apply( lambda x:  user_group[x]  )
gc.collect()       
util.pd_info(df)


### Save 
df.to_csv(in2+ 'purchasings_user2.csv', index=False)
gc.collect()  
############################################################################################
 

### assign in dataframe   ###############################
usecols=["machine_code"]
df= pd.read_csv(in2+ 'purchasings_user.csv', dtype= dtype0, usecols= usecols, nrows=10**8) 


a= df.machine_code.unique()
len(a)


 104231
   

 
 
 
 
 
 
 
 
 
 
 
 
 


######   Concatenate MDB CSV files  ########################################################
df= pd.read_csv(uri.raw+ '/vm_csv/20170120/txt/area_44_43.txt', nrows=10**9)   

dfi= pd.read_csv(uri.raw+ r'/vm_csv/20170120/txt/area_42.txt', nrows=10**9)   
len(dfi)


df= pd.concat((df, dfi  ), axis=0) 
df.columns


len(df), len(dfi)
df.to_csv(uri.raw+ r'/vm_csv/area_ALL_BIG.txt', index=False, mode='w')
  
'''
6661418    area_44_43.txt
1791054    area_34_FS_20.txt
2676174    area_34_FS20_igai.txt
2618506    area_41.txt
2618506    area_42.txt
 15397801= 6661418   + 1791054   +  2676174   +  2618506  +   1650649  
'''
############################################################################################



 
 
 
 
 
 
 
 
 
 
   
############################################################################################
#### 1) Read CSV FULL: partial columns,   ###########################################
#          0          1                2                 3                4
usecols=["user_id", "machine_code", "location_code",  "bottler_code", 'product_name', 
         'temperature', "amount",'purchased_at', 'user_rank_vol']

df= pd.read_csv(in2+ 'purchasings_user2.csv', dtype= dtype0, usecols= usecols, nrows=10**8)       
gc.collect()       
util.pd_info(df)     



#### Filter Best users
'''
rpt[rpt['STK_ID'].isin(stk_list)]
    
rpt.query('STK_ID in (600809,600141,600329)')
''' 

user_best= np.array( [33773,189358,41064,40072,95159,76099,674357,139721,267645,177021,27890,633606,165095,139100,17751,128694,38366,111123,296462,32884,53440,179550,85099,91373,140496,46180,28345,204684,618921,75835,264568,50521,48165,167654,80114,322621,16383,42311,37629,110467,251101,49439,200571,31321,24600,15027,24190,41577,80898,258517,31129,387998,23797,93517,33160,75431,34008,26141,176791,52474,819215,597166,125189,28556,143992,32451,41477,310476,16956,23285,638011,86725,79665,593825,42820,51485,434415,26471,86813,59256,28666,32006,54444,54585,38658,46619,482816,118147,82557,236459,92178,602912,126438,727334,660911,19491,114610,563354,275109,127589,46424,83233,30400,60238,82175,160046,81865,165294,18732,72534,435156,108744,15249,67219,162859,14064,73011,121532,84304,133538,87263,93613,575186,233843,261318,37354,198779,22829,50879,114689,157724,17105,137437,76548,255087,101561,52365,169727,53651,236900,187195,536388,36445,112033,618504,94843,100320,72177,275473,168260,625164,291378,86034,25480,42109,90468,567922,33468,109404,222600,15222,94269,196200,554276,27882,597136,496833,126381,251043,201193,159945,266323,235410,272431,27566,62366,82456,597520,656088,132660,6036,62536,78618,275104,873267,15389,29741,36080,44576,292593,552342,17354,58155,19093,23022,623147,62537,82060,228109,622331,141451,157798,48551,439838,93286,101580,28883,599444,94230,139645,72612,89655,85666,259446,21506,16870,229252,61852,182122,15487,239161,38565,77011,85302,477747,622546,674142,83457,138346,269716,297058,82759,140552,600445,91098,137993,193360,304094,79177,601006,54953,110081,189027,259004,669540,13389,109934,41181,53557,257757,34379,82930,96422,510746,45427,82648,42940,246818,568548,229925,39117,97520,272980,352719,41228,121906,25543,73318,143961,304970,35036,153485,187904,620960,23644,157017,4540,15961,20342,25661,72075,24314,192230,304251,26310,108374,136967,114814,17519,125264,290137,658494,76851,75909,34588,49259,133409,59780,666235,162955,36835,42939,62164,162243,236637,79823,36870,321822,487242,598185,80488,85032,323704,517791,572215,205159,226359,16993,48517,50733,120390,241306,26238,33942,54313,257737,304693,258585,27867,93223,23142,27450,88010,414897,68149,80400,799838,196469,289936,192613,647153,775099,16386,73541,399441,36633,49687,49900,199062,249311,290621,381224,52875,77986,63172,138940,172304,358507,24218,50200,209709,741704,67348,94504,105509,236198,76074,602550,115536,259616,72968,116749,54558,167760,173142,44574,46084,164897,167332,27790,87544,172338,60561,199009,39842,85376,177274,651242,60268,137734,19283,51952,614749,14547,263824,19617,620177,622841,657188,72029,28148,53686,80693,762589,38335,39262,149580,48816,109262,131753,66962,134799,165937,289529,266144,626556,33998,132372,179057,206371,14014,288675,666241,63103,17705,68041,211644,301766,33256,96995,142142,171408,599374,131062,618574,117676,160384,674176,86163,115072,308008,43420,58889,519420,628799,17390,258504,25369,49855,61210,165610,273893,297400,782205,84087,133188,223659,47973,259829,508924,679056,32274,656300,689199,63003,109919,570777,179469,254048,298746,25614,60850,83331,28960,33097,36367,39244,101577,485357,519369,28863,710396,324865,32474,102422,272568,61883,111710,116085,137194,95022,330032,66463,112171,260648,63107,229966,19560,119770,37615,45818,322053,41241,79043,115816,15188,48235,148286,38930,79808,238613,28162,42631,94267,139879,80009,128766,417816,21144,46173,160819,211740,398,28469,61958,96746,825826,39067,40698,42228,53133,316793,579700,39451,45527,138693,390304,539453,46086,120019,13633,22875,37641,80427,155969,299377,28161,83014,91533,162019,169744,83785,103641,133139,175686,672661,34383,61547,23224,99640,167051,182128,502279,607546,16036,49529,172759,194650,506142,648850 ] )

user_best= np.array( [33773,189358,41064,40072,95159,76099,674357]  )

user_all=  df.user_id.unique()



##### Select Data from  users  #############################################################
df_best= df.query(' user_id in ' +str(user_best) )


df_all= df.query(' user_rank_vol < 0.95 ' )  #2 purchases above
user_all=   df_all.user_id.unique()




#### Transaction  ----> Alll user_list   #######################################################
user_select=   user_all
df_select=     df
user_label =  'user_all_'

users= util.np_dictordered_create()
for kk in user_select :  users[kk]= {}


for ii, kk in enumerate(user_select) :
 if ii > -1 : 
  dfi= df_select[df_select.user_id == kk ]

  datei= dfi.purchased_at.values  
  t0, t1=  datei[0], datei[-1]

  users[kk]['t0']= t0
  users[kk]['t1']= t1

  dt=      date_diffsecond(t1 , t0 ) 
  users[kk]['date_total']= dt

  x=  dfi.amount.sum() * 1.0
  users[kk]['amount_total']=   x                        #  604800s in 1 week

  if ii %  10**3 == 0 :      print(str(ii))
  if ii %  (5*10**4) == 0 :  util.save(users, user_label + '_' + str(ii) )

  
#  util.save_test( user_label + '_' + str(ii) ) 


#Export dict to csv table -------------------------------------------------------------
ii=0
with open(in3 + 'user_info.csv', 'w') as f:
  for key, value in users.items() :
    ii+=1
    #if ii > 10 : break
    if ii==1 : f.write(  'user_id,' +  np_dict_tostr_key(value)  + '\n')
    f.write( '{0},{1}\n'.format(key, np_dict_tostr_val(value) ) ) 
  
    

    

############################################################################################
#### Transaction  ---->  BIG user_list   ###################################################
user_select=   user_all
df_select=     df_all
user_label =   'user_all_'


users= util.np_dictordered_create()
for kk in user_select :  users[kk]= OrderedDict()   # {}

for ii, kk in enumerate(user_select) :
  if ii < -1  : break 
   
  dfi= copy.deepcopy(df_select[df_select.user_id == kk ])
  # dfi.sort_values('purchased_at', inplace=True)
  del dfi['user_id']


  # User group :
  users[kk]['user_rank_vol']=  dfi['user_rank_vol'].values[0]

  #Time series
  datei= dfi.purchased_at.values  
  t0, t1=  datei[0], datei[-1]
  dt=      date_diffsecond(t1 , t0 ) 
  users[kk]['date_total']= dt
  users[kk]['t0']= t0
  users[kk]['t1']= t1

  users[kk]['date']= datei  
  users[kk]['date_sec_end']= np.array([ date_diffsecond(str_t1=t1, str_t0=x) for x in datei  ])


  #Put in dataframe
  dfi['date_sec_start']= dfi['purchased_at'].apply( lambda x: date_diffsecond(x, str_t0=t0)   )
  dfi['date_sec_end']=   dfi['purchased_at'].apply( lambda x: date_diffsecond(str_t1=t1, str_t0=x)  )

  
  x=  dfi.amount.sum() * 1.0
  users[kk]['amount_sum']= x
  # users[kk]['amount_perweek']=   x / ( dt / 6048005.0)  #  604800s in 1 week
  # users[kk]['amount_perday']=    x / ( dt / 86400.0)  #  604800s in 1 day
  # users[kk]['amount_permonth']=  x / ( dt / 18295200.0)  #  604800s in 1 month
  
  
  #Basket profile
  users[kk]['drink_nb']=  len(list(dfi.product_name.unique()))
  users[kk]['drink']=     np_list_tofreqdict(dfi.product_name.values)
  
  users[kk]['location_nb']=  len(list(dfi.location_code.unique()))
  users[kk]['location']=     np_list_tofreqdict(dfi.location_code.values)
  

  users[kk]['nb_last_week1']=  int(dfi[dfi.date_sec_end <  604800   ].amount.sum())
  users[kk]['nb_last_week2']=   int(dfi[dfi.date_sec_end <  604800*2 ].amount.sum())
  users[kk]['nb_last_week3']=   int(dfi[dfi.date_sec_end <  604800*3 ].amount.sum())
  users[kk]['nb_last_week4']=  int(dfi[dfi.date_sec_end <  604800*4 ].amount.sum())
  users[kk]['nb_last_week5']=  int(dfi[dfi.date_sec_end <  604800*5 ].amount.sum())
  
  # users[kk]['dfi']=  dfi

  if ii %  10**3 == 0 :      print(str(ii))
  if ii %  (5*10**4) == 0 :  util.save(users, user_label + '_' + str(ii) )
util.save(users, user_label + '_' + str(ii) )

  
util.save_test(user_label + '_' + str(ii) )
gc.collect()





for k,x in users.items() :
  v= users[k]
  print v['amount_sum'], v['amount_perweek'], v['nb_last_week1'], v['nb_last_week4'], v['nb_last_week3']
############################################################################################













############################################################################################
v= df_best['user_id'].values

  
  
  #  dfi.purchased_at.values.sort()   #sort the dates
  # Keep the dataframe
  users[kk]['purchased_at']= dfi.purchased_at.to_string(index=False)   #.replace('\n',',') 
  users[kk]['amount']=       dfi.amount.to_string(index=False)
  users[kk]['product_name']= dfi.product_name.to_string(index=False).replace('          ','')
  users[kk]['machine_code']= dfi.machine_code.to_string(index=False) 


  datei= dfi.purchased_at.values  
  t0=  datei[0]   
  t1=  datei[-1]
  users[kk]['t0']= t0
  users[kk]['t1']= t1   
  users[kk]['date_total']= date_diffsecond(t1 , t0 )    
  users[kk]['date_sec_start']= [ date_diffsecond(t, t0) for t in datei  ] # from Start
  users[kk]['date_sec_end']= [ date_diffsecond(t1, t) for t in datei  ]  # From end




users[kk]['date_sec_end'][-20]



date_diffsecond('2016-12-15 22:36:00', '2016-12-15 08:00:00') / (3600.)
   

  dfi.purchased_at.to_string
  
  
    
#### issues    
eval( str(dfi.product_name.values))
 print users[kk]['product_name'].split('\n')

  
n= len(df_best)
for i in xrange(0,n) :
   kk=  df_best.iloc[i, 7]
   #idate= arrow.get(df_best.iloc[i, 6], fmt )
   idate= df_best.iloc[i, 6]
   user_id[kk].append(idate)



###date, day creation    ##########################################################
for k, datek in user_id.items() :
    datek.sort()
    ndate= len(datek)
    dateday= np.zeros(ndate, dtype=np.int32)

    
    datek0=  arrow.get(datek[0], fmt)
    for i in xrange(0, len(datek)) :
       dateday[i]=   (arrow.get(datek[i], fmt) - datek0).days

    user_id[k]['date']= datek
    user_id[k]['day']=  dateday



##################################################################################
#### Data model to user





import copy
user_id2= copy.deepcopy(user_id)


def weekday(s, fmt='YYYY-MM-DD', i0=0, i1=10):
  s2= s[i0:i1]
  try :
    return  cache_weekday[s2]
  except KeyError:
    wd= arrow.get(s2, fmt).weekday()


    


#==============================================================================
####### Pivot Table on the CSV file   ###############################################
df_pivot1= pd.pivot_table(df,
  index='user_id' ,   columns='bottler_code', 
  values='amount', aggfunc='sum' )
df_pivot1.to_csv(out1+ 'byuser_bottler_amount.csv', index=True)





####### Pivot Table on the CSV file   ###############################################
df_pivot1= pd.pivot_table(df,
  index='user_id' ,   columns='product_name', 
  values='amount', aggfunc='sum' )


df_pivot1.fillna(0, inplace=True)
df_pivot1


file1= 'df_pivot1_user_product_amount'
df_pivot1.to_csv(out1+ file1+'.csv', index=True)
util.save(df_pivot1, out1+file1 + '.pkl')
gc.collect()



df_pivot1['product_name'] = df_pivot1.index

df_pivot1.columns


#### Pandas Pivo


df_pivot1.to_csv(out1+ file1+'.csv', index=False)
















#################################################################################################
###### Read file and extract data pattern:  .csv,  .txt, .xls  ##################################
file1= u'【OBPPCデータ】ロケチャネル×VPM.xlsx'
dir1= u'E:/_data/unerry/csv/vm_csv/20161208 OBPPC-1/'


file1= u'*.xlsx'
dir1= u'E:/_data/unerry/csv/vm_csv/'
da.xl_getschema(dir1, filepattern=file1, outfile=dir1+'/schema.xlsx')








#----- Extract zip to folder                            -----------------------------
#   util.os_zipextractall(in1+'/zip/*.zip',  in1+'/csv/')


#### unicode  --- > utf-8, before SAVING
df2['VALIDEND']= df2['VALIDEND'].apply(util.str_to_utf8)
df2['COUPON_ID_hash']= df2['COUPON_ID_hash'].apply(util.str_to_utf8)


######################## CSV Aanalysis    ###########################################
# Parse CSV Files: put Summary into Excel + Type_guess  --------------------------------
in2= 'E:/_data/unerry/csv/cokeon_csv/'
df_schema, df_type_guess_all=  da.csv_col_schema_toexcel(dircsv=in2, filepattern='*.csv',
                                  outfile=in2 + '/_meta.xlsx',
                                  maxrow= 500000, returntable=1)

## 11 mio lines


df_schema, df_type_guess_all= util.load(in2+'_meta_schema.pkl'),  util.load(in2+'_meta_type_guess.pkl')



###### Update meta database  ########################################################
#  ALLDB= util.load( in1+'ALL_DB_META.pkl')
#   ALLDB={'cokeon':  { } }

'''
ALLDB= da.db_meta_add(ALLDB, 'cokeon', schema=df_schema, df_table_uri=None, df_table_columns=None)
ALLDB['cokeon']['table_uri']
util.save(ALLDB, in1+'ALL_DB_META.pkl')
  
ALL_schema, ALL_type_guess_all= util.load(in2+'_meta_schema.pkl'),  util.load(in2+'_meta_type_guess.pkl')

ALLDB= da.db_meta_add(metadb= ALLDB, dbname='cokeon', new_table= ('type_guess', ALL_type_guess_all)   )

ALLDB= da.db_meta_add(ALLDB, 'cokeon', df_table_uri=df_uri  )

ALLDB= da.db_meta_add(ALLDB, 'cokeon', df_table_columns=df_col)


'''

###Access to DB, table fromm ALLDB,  Look_up in all table  ##########################
#### Query the Meta Table  and get list of URI 
db_find_rs= da.db_meta_find(ALLDB, query='bottler')


db_find_rs=  da.db_meta_find(ALLDB, query='bottler.csv', filter_db=['cokeon'],   filter_table=['table'], filter_column=['table'] )

db_find_rs[0][0], db_find_rs[0][1], db_find_rs[0][2]


da.db_meta_find(ALLDB, query='bottler', filter_db=['cokeon'],   filter_table=['table'], filter_column=['table'] )


da.db_meta_find(ALLDB, query='bottler', filter_db=['cokeon'],   filter_table=['table'] )


da.db_meta_find(ALLDB, query='bottler', filter_db=['cokeon'])


#### Query Dataframe
ALLDB['cokeon']['table_uri'].query("table== '"+ table1 +"'")




#### Find Pattern in Pandas dataframe  ##############################################
util.pd_find(df, '08:31', doreturnposition=True )
util.pd_find(df, '08:29', col_restrict=['purchased_at'], doreturnposition=True )
util.pd_find(df, '08:29', col_restrict=['bottler_name'] )
util.pd_find(df, 100.0, isnumeric=True )


## 10mio Transact, 1.5Go,  find takes 5s to list all patterns
df_find, df_find_pos= util.pd_find(df, '08:31', doreturnposition=True )





#####################################################################################



################### CSV Files Transfomation   #######################################      
df= pd.read_csv(in2+ 'purchasings.csv', nrows=10**3)      
gc.collect()                    
df.head(),  util.pd_info(df)           
           
           
''' Transformation of data :

purchase_at --->  month, day, year, hour, weekday, daytime


location_code -->
   location__type, location__building_type1, location__building_type2, 
   location__inout, location__conbini_dist, location__info1, location__info2


product_name -->  
   product__brand_code,   product__brand_en_name,  categories__code, categories__abbr


Create  a view:
df_v1= df[[col1, col2, col3  ]] 
df_v1[newcol]=   
  


'''           

#2) Save the table in csv or in DB


#3) Process to Pivot table:  VIEWS


#4)  Generate Report


'''
Cluster of   (Machine, Users)
        of   (Users, Drink)

Marketing Campaign ---> Select Target Population
   system --> select machines  Targets
   Validation of user
   
   ---> Can generate report on Sales

Think of colums to be seen

'''

##### 0) Create Flat View in SQL join of all multi table columns ---> Generate the CSV
import datanalysis as da


#### 1) Test CSV and Find Dtypes    #################################################
table1= 'purchasings'




##### ressource locator   ###########################################################
url1= in2+ 'purchasings.csv'    #Be careful of DASK
url1= ALLDB['cokeon']['table_uri'][table1]


df= pd.read_csv(ALLDB['cokeon']['table_uri'][table1], nrows=10**3)       
gc.collect()                   
df.head(),  util.pd_info(df)     

util.pd_dtypes(df, returnasdict=0)


ALLDB['cokeon']['type_guess']['purchasings']

dtype0= {'amount': 'int16',
 'area_code': 'int32',
 'bottler_code': 'int16',
 'bottler_name': 'category',
 'id': 'int32',
 'js_code': 'int32',
 'location_code': 'int32',
 'machine_code': 'int64',
 'price': 'int16',
 'product_name': 'category',
 'promotion_id': 'float16',
 'purchased_at': 'object',
 'temperature': 'int16',
 'user_id': 'int32'}


df= df.astype(dtype0)





#### 1) Read CSV FULL: partial columns,   ###########################################
usecols=["user_id", "machine_code", "location_code",  "area_code", 'product_name', 
         'temperature', "amount",'purchased_at']

df= pd.read_csv(in2+ 'purchasings.csv', dtype= dtype0, usecols= usecols, nrows=10**8)       
gc.collect()       
util.pd_info(df)     







#### Create view with new columns
df_v1= df.loc[:,("user_id", "machine_code", "location_code",  "area_code", 'product_name', 
              'temperature', "amount",'purchased_at')]
# df_v1= df[['machine_code', 'location_code', 'purchased_at' ]]   #Error
df_v1.dtypes
del df; gc.collect()

df_v1.iloc[0,2]

 

### Add Date  ----------------------------------------------------------------------
import arrow
###################Faster one   #####################################################
#'YYYY-MM-DD    HH:mm:ss'
#"0123456789_10_11
def day(s):    return int(s[8:10])
def month(s):  return int(s[5:7])
def year(s):   return int(s[0:4])
def hour(s):   return int(s[11:13])
# def weekday(s):  return arrow.get(s, 'YYYY-MM-DD HH:mm:ss').weekday()



###Super Fast because of caching
cache_weekday= {}
def weekday(s, fmt='YYYY-MM-DD', i0=0, i1=10):
  s2= s[i0:i1]
  try :
    return  cache_weekday[s2]
  except KeyError:
    wd= arrow.get(s2, fmt).weekday()
    cache_weekday[s2]= wd
  return wd

def season(d):
  m=  int(d[5:7])
  if m > 3 and m  < 10: return 1
  else: return 0 


def daytime(d):
  h= int(d[11:13])
  if   h < 11 :   return 0
  elif h < 14 : return 1    #lunch
  elif h < 18 : return 2    # afternoon
  elif h < 21 : return 3    # dinner
  else :        return 4   #night



coldate=  'purchased_at'   ; fmt= 'YYYY-MM-DD HH:mm:ss'
# df_v1['month']=   df_v1[coldate].apply(lambda t: arrow.get(t, fmt).month).astype('int8') 
df_v1['day']=     df_v1[coldate].apply(day).astype('int8') 
df_v1['month']=   df_v1[coldate].apply(month).astype('int8') 
df_v1['year']=    df_v1[coldate].apply(year).astype('int16') 
df_v1['hour']=    df_v1[coldate].apply(hour).astype('int8') 
df_v1['season']=  df_v1[coldate].apply(season).astype('int8') 
df_v1['daytime']= df_v1[coldate].apply(daytime).astype('int8') 
gc.collect()  


#--- Cache : Accelerate the compute Super Slow, dont forget the function weekday()  
df_v1['weekday']= df_v1[coldate].apply( weekday ).astype('int8') 
gc.collect()  


del df_v1['purchased_at']
df_v1.head()


df_v1.to_csv(out1+'/purchasings_v2.csv', index=False)
gc.collect()  





####### Pivot Table on the CSV file   ###############################################
df_pivot1= pd.pivot_table(df_v1,
  index='product_name' ,   columns='location_code', 
  values='amount', aggfunc='sum' )


df_pivot1.fillna(0, inplace=True)
df_pivot1


file1= 'df_pivot1_product_name_area_code_amount'
df_pivot1.to_csv(out1+ file1+'.csv', index=True)
util.save(df_pivot1, out1+file1 + '.pkl')
gc.collect()


df_pivot1['product_name'] = df_pivot1.index

df_pivot1.columns


#### Pandas Pivo


df_pivot1.to_csv(out1+ file1+'.csv', index=False)




###Location filtering  --------------------------------------------------------------




#### Pivot on items 






### Export to Excel






#####################################################################################
######Caching for date parsing



#### Pandas #########################################################################
df= pd.read_csv( in2 + 'purchasings.csv', sep=',')   ##ll int

df_pivot1= pd.pivot_table(df, index='product_name', columns='bottler_code', 
                          values='price', aggfunc='sum' )


df_pivot1.fillna(0, inplace=True)
df_pivot1.to_csv(out1+'pivot_1.csv')
util.save(df_pivot1, 'df_pivot1_ref')


del df; gc.collect()
           
           
          
### DASK   ##########################################################################
df = dd.read_csv( in2 + 'giving_tickets.csv', sep=',')

df.head(), len(df)

 
 
df = dd.read_csv( in2 +  'purchasings.csv', sep=',')
df.head(), len(df)
gc.collect() 


df['bottler_code']= df['bottler_code'].astype('category')
df_pivot2= df.pivot_table(index='product_name', columns='bottler_code', 
                          values='price', aggfunc='sum' )
 
 
df_pivot2= df_pivot2.compute()
           
df_pivot2.fillna(0, inplace=True)    

df_pivot1.values - df_pivot2.values
###Works ok











################# Pandas SQL  to POSTGRES  ####################################################
import sqlalchemy as sql

# Start Postgres DB in pgadmin
# psycopg2
# dbengine = sql.create_engine('postgresql+psycopg2://postgres:postgres@localhost/coke')
dbengine= util.sql_create_dbengine('postgres',  dbname='coke', login='postgres', password='postgres', port=5432) 


df_q= util.sql_query(dbengine=dbengine, sqlr= ''' 
select * from purchasings where bottler_name='CCWJ' 


''')



util.pd_dtypes(df, returnasdict=0)








### ok works, no Encoding issues  !!!
df_q.to_sql('purchasings2', dbengine)





### Get SQL
####in PgAdmin4 :
### http://www.vertabelo.com/blog/technical-articles/creating-pivot-tables-in-postgresql-using-the-crosstab-function
#CREATE extension tablefunc
'''
### Pivot table is NOT DYNAMIC !!!!!
Need to specify the columns  ---> Bad

'''

#####################################################################################
  




######################### CSV to HDFS ###############################################
print df_type_guess_all['purchasings']

dtype0= {'user_id': 'int32', 'temperature': 'int16', 'js_code': 'int32', 'bottler_code': 'int16', 
'area_code': 'int32', 'location_code': 'int32', 'machine_code': 'int64', 'price': 'int16', 
'amount': 'int16', 'id': 'int32', 'promotion_id': 'float16', 'purchased_at': 'object',
 'bottler_name': 'category', 'product_name': 'object'}

util.pd_h5_fromcsv_tohdfs(in2, 'purchasings.csv', tofilehdfs= in2 + 'purchasings.h5',
                          chunksize= 2000000, tablename='df', mode='w',
                          dtype0=dtype0)
                  
                  
df2= pd.read_hdf(in2 + 'purchasings.h5', 'df', start=0, stop=100)                      
df2.head(),  util.pd_info(df2)           
                  
                  

util.a_info_packagelist()


### DASK   ###############################################################
df = dd.read_csv(in2 + 'user_groups.csv')




df = dd.read_hdf(in2 + 'purchasings.h5', key='df', start=0, stop= 100)
df.head(),  df.dtypes
'nrow', len(df)

# df['company']= df['company'].astype('category')
df['purchaseamount']= df['purchaseamount'].astype('float32')
df['purchaseamount']= df['purchaseamount'].fillna(0.0)

# Left: index, Colums: top, values: center
df_pivot= df.pivot_table(index='chain', columns='dept', values='purchaseamount', aggfunc='sum')
df_pivotr= df_pivot.compute()
gc.collect()  #free memory
df_pivotr.shape


df['chain'].drop_duplicates().count().compute() #134
#


df['purchaseamount'].head()
df['purchaseamount'].sum().compute()


#############################################################################################


#Valid in DASK
df[df.resource_record!='AAAA'].resource_record.value_counts().compute()
df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})


####Saving DASK on disk
df.to_hdf('bigfile_merge.hdf', 'df',  compute=True)
gc.collect()  #free memory




################# Pandas SQL : Crashing with Unicode   #####################################################
from pandasql import *
import pandas as pd
pysqldf = lambda q: sqldf(q, globals())


#Clean to unicode
df= df.apply(da.str_to_unicode)     

           
q= """
SELECT m.product_name, m.js_code
FROM
  df m
WHERE
    m.bottler_code > 25;
"""        

###  Crash due to encoding issue
df_rs= pysqldf(q)           
           
           
df_rs= df[[ 'product_name', 'js_code' ]].where(df.bottler_code > 25 )
           

           
           











######################## DTYPES   ###############################################################
''' 'Object',  'bool', 'string_', 'unicode' float16, float32, int8, int16, int32, int64, uint8, uint16, uint32, uint64
'''
 
df= pd.read_csv(in2+'file_big01.csv', nrows=1000)
df.describe()
df_dtype0= util.pd_info(df) ; df_dtype0

dtype0= {'COUPON_ID_hash': 'object',
 'ITEM_COUNT': 'int16',
 'I_DATE': 'object',
 'PURCHASEID_hash': 'object',
 'SMALL_AREA_NAME': 'category',
 'USER_ID_hash': 'category'}

df= df.astype(dtype0)

######  To small int
for col in [ 'purchasequantity'  ] :
  df[col]=  df[col].astype('int32')


  

########## Japanese Text ############################################################
df= pd.read_csv('E:/_data/kaggle/couponjapan/rawcsv//coupon_list_test.csv')
df.dtypes

df2= df.astype(type_guess_all['coupon_list_test'])
df2.dtypes


#### unicode  --- > utf-8, before SAVING
df2['VALIDEND']= df2['VALIDEND'].apply(util.str_to_utf8)
df2['COUPON_ID_hash']= df2['COUPON_ID_hash'].apply(util.str_to_utf8)

df2.to_hdf('E:/_data/kaggle/couponjapan/rawcsv//coupon_list_test2.h5', 'df', format='table')





######################### CSV to HDFS ###############################################
in1= 'E:/_data/kaggle/test/'
util.pd_h5_fromcsv_tohdfs(in1, 'ja*.csv', tofilehdfs= in1 + 'fileja_hdf_compress3.h5',
                          chunksize= 10000, tablename='df', mode='w', dtypes=None, col_category=[])

store= pd.HDFStore(in1 + 'fileja_hdf_compress3.h5')
for df in store.select( 'df',  chunksize=5000)  :
   print df.shape,

###### BIG CSV
util.pd_h5_fromcsv_tohdfs(in1, '*big*.csv', tofilehdfs= in1 + 'file_big_hdf_compress.h5',
                          chunksize= 100000, tablename='df', mode='a')


store= pd.HDFStore(in1 + 'file_big_hdf_compress.h5')
for df in store.select( 'df',  chunksize=500000) :
   print df.shape,



######### Operation on store    #####################################################
# http://pandas.pydata.org/pandas-docs/stable/io.html#query-via-data-columns
df.head()
df.index

store.get_storer('df').nrows


#Get Specific
df_col1= store.select('df', columns=['SMALL_AREA_NAME'])


#Select on range of Index
ix0 = store.select_as_coordinates('df','index> 5000')
ix0.summary()
store.select('df', columns=['SMALL_AREA_NAME'],   where=ix0)


#Select using a mask criteria
where = c[pd.DatetimeIndex(c).month==5].index
store.select('df_mask',where=where)

# Another way is to pass a PyTables query to the HDF file:
df= store.select('df', '(column1 == 1.0) & (column2 > 2.5) & (column3 < 10) & …)')





#####################################################################################
#####################################################################################
df = pd.DataFrame({'a':['1','2',3], 'b':['ホテ','・旅館', 'ホテル']})
df.dtypes


df= df.astype({'a': 'unicode', 'b': 'str'})
type(df.iloc[0, 0])


df_col= df.columns.values


df_type_len= [ df[col].map(len).max()  if str(df[col].dtype) == 'object' else 0  for col in df.columns.values ]


for col in df.columns.values :
  if str(df[col].dtype) == 'object'  :
    df[col].fillna('', inplace=True)
    print  df[col].map(len).max()

type(df.iloc[0,0])
df.iloc[0,0].decode('utf-8')


def pd_str_isascii(x):
  try :
    x.decode('ascii'); return True
  except: return false

   
def str_to_utf8(x):
  return x.encode('utf-8')


#####################################################################################
df['SMALL_AREA_NAME']= df['SMALL_AREA_NAME'].apply(to_unicode)

util.pd_toexcel(df, outfile=in2+'test.xlsx')



2. Unicode everywhere
to_unicode_or_bust(ivan_uni)


3. Encode late
Encode to <type 'str'> when you write to disk or print

f = open('/tmp/ivan_out.txt','w')
f.write(ivan_uni.encode('utf-8'))
f.close()


np.finfo(np.float16).max

da.csv_analysis()
df1.dtypes.tolist()

type(df1.iloc[0,1])









#------ Parse CSV Files and put Summary into Excel   --------------------------------
da.csv_col_schema_toexcel(dircsv=indir0 + '/rawcsv', outfile=indir0 + '/meta_summary2.xlsx', returntable=1,
                          maxcol_pertable=90, maxstrlen='U80')


#------   Need to find Type:
 int, float, string lenght, min length



#########################  Pivot Table #########################################################################
df_pivot1= da.csv_pivotable(fileh5=in1+'fileja_hdf_compress3.h5',
                            leftX='I_DATE', topY='SMALL_AREA_NAME', centerZ='ITEM_COUNT', mapreduce='sum',
                            chunksize= 50000, tablename='df')
df_pivot1

store.get_storer('df').nrows



### 1.2 Go Big table :  OK !!
df_pivot1= da.csv_pivotable(fileh5=in1+'/file_hdf_table_compress.h5',
leftX='chain', topY='company', centerZ='purchasequantity', mapreduce='sum', chunksize= 800000, tablename='df')
df_pivot1


util.save(df_pivot1, in1+'/df_pivot1.pkl')



######## On Disk Storage #######################################################################

#### pkl file:  No issue, 1.7go --->  1.3 go      OK validate
util.py_save_obj(df, in1+'/transaction_red.pkl')

df= util.py_load_obj(in1+'/transaction_red.pkl', isabsolutpath=1)


#### hdf:  Low size +  Super Fast
df.to_hdf(in1+'transact_hdf.h5','df',mode='w',format='table')


#### hdf:  Compress 0.7Go
# def to_hdf(self, path_or_buf, key, mode='a', append=False, get=None, **kwargs)
df.to_hdf(in1+'file_hdf_table_compress.h5','df',mode='w',format='table', complib='blosc')


#### Read needs 6Go in memory....., can sub-select
df= pd.read_hdf(in1+'file_hdf_table_compress.h5','df', start=75000, stop= 60000)
df.info()


##################################################################################################
#################### Japanese Text ###############################################################
df= pd.read_csv('E:/_data/kaggle/couponjapan/rawcsv/coupon_detail_train.csv')
df.info()

#### cannot reduce type


#### hdf:  23Mo --> 17Mo  compress
# def to_hdf(self, path_or_buf, key, mode='a', append=False, get=None, **kwargs)
df.to_hdf(in1+'japa_hdf_table_compress.h5','df',mode='w',format='table', complib='blosc')


#### Read needs 6Go in memory....., can sub-select
df= pd.read_hdf(in1+'japa_hdf_table_compress.h5','df', start=75, stop= 6000)
df.info()
##################################################################################################





############# POSGRES Database      ###################################################################
odo(df, 'postgresql://localhost:5432::transact')  # Migrate dataframe to Postgres

odo('myfile.*.csv', 'postgresql://hostname::tablename')  # Load CSVs to Postgres

psycopg2
conda install -c conda-forge psycopg2=2.6.2






################## Initial Load and type check Max Value    ###############################################
df1= pd.read_csv(file_transact, sep=',', nrows= 100)
dfs= df1.describe()
print df1.head(10),"\n",  "\n\n",  util.pd_dtype_print(df1)
dfs[dfs.index.isin(['min', 'max'])]


ds= {'id': 'uint32', 'chain': 'uint16', 'dept': 'uint16', 'category': 'uint32', 'company': 'uint32',
'brand': 'uint32', 'date': 'object', 'productsize': 'float16', 'productmeasure': '|S2',
'purchasequantity': 'uint16', 'purchaseamount': 'float16'}


DIRRAW= ''
DBNAME + TABLE1= ''


DIR0 = '  '
df1= pd.read_csv(f_transactions_red.csv, sep=',', nrows= 100)


file1= in1 + 'trainHistory.csv'
file2= in1 + 'transactions_red.csv'
file3= in1 + 'transactions_red2.csv'

df_bz= bz.data( file2)
df_bz.dshape

pivot1= bz.by( df_bz.chain ,  col1=  df_bz.purchaseamount.sum() )


df= odo(file3, pd.DataFrame)
df.dtypes



by(merge(df.name, df.id), amount=df.amount.mean())

#### SQL to Blaze
http://blaze.readthedocs.io/en/latest/rosetta-sql.html




import dask
df= dask.dataframe.csv.read_csv(file3)



 by(table.grouping_columns, name_1=table.column.reduction(),
                         name_2=table.column.reduction(),)
Here is a concrete example. Find the shortest, longest, and average petal length by species.

 from blaze import by
 by(iris.species, shortest=iris.petal_length.min(),
                  longest=iris.petal_length.max(),
                average=iris.petal_length.mean())




##### Load 2.6Go in RAM
df= pd.read_csv(in1 + '/transactions_red.csv')



df_pivot1= da.csv_pivotable(fileh5=in1+'japa_hdf_table_compress2.h5',
                            leftX='I_DATE', topY='SMALL_AREA_NAME', centerZ='ITEM_COUNT', mapreduce='sum',
                            chunksize= 5000, tablename='df')


df_pivot1.info()
df_pivot1.head()


store= pd.get_store(in1+'japa_hdf_table_compress.h5')

pivotable1 = reduce(lambda x, y: x.add(y, fill_value=0), (df.groupby(by='SMALL_AREA_NAME').sum() for df in store.select(tablename, chunksize=chunksize)))


df_pivot= df.pivot(index='I_DATE', columns='SMALL_AREA_NAME', values='ITEM_COUNT')

I_DATE,SMALL_AREA_NAME,


pivot_i = pd.DataFrame.pivot_table(df, values='ITEM_COUNT', index=['I_DATE'],
                                 columns=['SMALL_AREA_NAME'], aggfunc=np.sum,
                                 fill_value=0)

pivot0= pd.concat([pivot0, pivot_i]).groupby(by=['I_DATE']).sum()




table.info()
df_list = [table, table]

pd.concat([x1, x2]).groupby(["city", "school"], as_index=False)["count"].sum()

table.index


df_pivot1= da.csv_pivotable(dircsv='', filepattern='', fileh5=in1+'japa_hdf_table_compress.h5',
                            leftX='chain', topY='market', mapreduce='sum', chunksize= 500000, tablename='df')


'''
http://stackoverflow.com/questions/32298047/efficient-storage-of-large-string-column-in-pandas-dataframe

df.to_hdf('test_compression_table.h5','df',mode='w',format='table',complib='blosc')

df['A'] = df['A'].astype('category')

df.to_hdf('test_categorical_table.h5','df',mode='w',format='table')

'''


util.pd_dtype_print(df2)



########## 1.7Go CSV file   ######################################################################
util.pd_h5_fromcsv_tohdfs(in1, filepattern='transactions_red.csv', tofilehdfs=in1+'file2.h5', tablename='df',  chunksize= 1000000)


df= util.pd_h5_load(in1+'/file2.h5', 'df', rowstart=0, rowend=10)



util.pd_h5_dumpinfo(in1+'/file2.h5')


df_pivot1= da.csv_pivotable(dircsv=in1, filepattern='coupon_detail_train.csv', fileh5=in1+'/transact01.h5',
                            leftX='chain', topY='market', mapreduce='sum', chunksize= 500000, tablename='df')




id,chain,dept,category,company,brand,date,productsize,productmeasure,purchasequantity,purchaseamount
86246,205,99,9909,104538848,15343,2012-03-02,16,OZ,1,2.49
86246,205,21,2106,105100050,27873,2012-03-02,64,OZ,1,3.29




###########################################################################################






util.pd_h5_fromcsv_tohdfs(in1, filepattern='*.csv', tofilehdfs=in1+'file1.h5', tablename='data', encoding='utf-8', chunksize= 2000000)


util.os_file_listall(in1, pattern='*train*.csv')[2]



df[columns] = df[columns].applymap(str)



format='table', min_itemsize={'A': 30}


'''
# import the modules
import unicodedata as ucd
import pandas as pd

# open the data file
df = pd.read_csv('path/to/file.csv', encoding='utf-8')

# the column we want to normalize is named 'page'
df['page'] = df['page'].map(lambda x: ucd.normalize('NFKD', x))


'''

filelist1= util.os_file_listall(dircsv=in1, pattern='*train*.csv')

filelist1[2]

csvlist=   filelist1[:,0]


id,chain,offer,market,repeattrips,repeater,offerdate


id,chain,dept,category,company,brand,date,productsize,productmeasure,purchasequantity,purchaseamount





#############################################################################################
########################### Blaze Load  #####################################################

df = bz.data(file1)
print df.peek()
df.count()

df.dshape

ds= od.dshape("""var * {
  id: int64,
  chain: int32,
  dept: int32,
  category: int64,
  company: int64,
  brand: int64,
  date:  string[30, 'ascii'],
  productsize: float32,
  productmeasure: string[10, 'ascii'],
  purchasequantity: int32,
  purchaseamount: float32
  }""")

df = bz.data(file1, dshape=ds)

#Selection with Blaze
df2= df[  df.month  > 10]
df2= df2[ df2.dateyear  > 2015 ]

df2.head(10)
df_pd=df2.head(10)
df_pd= odo(df_pd, pd.DataFrame)


bz.mean(df2.close)

#Export to DataFrame the sub-selection
df_pd= odo(df2, pd.DataFrame)

#Export to Numpy
df_np=  df_pd[['close']].values
len(df_np)
#############################################################################################





















#-------------- Details:  -----------------------------------------
util.session_load('/kaggle/kaggle_supermarket_01')

util.a_help()



##########################################################################################
#Kaggle Challenge:
#'Reduce the data and generate features' by Triskelion
# 10 mio:  1.5Go, 30mio: 4.6Go


#########################################################################################
#########################  Data Selection ###############################################
in1= 'E:/_data/kaggle/largesuper/csv/'
out1= 'E:/_data/kaggle/out/'

file1= in1+'*.csv'  #Full

file1= in1+'transactions.csv.gz'

loc_offers =   in1+ "offers.csv"
file_transact= in1+ "transactions_red.csv"
file_reduced =  out1+ "/transac_red.csv" # will be created


'''
0   1     2     3         4      5    6      7              8               9                10
id,chain,dept,category,company,brand,date,productsize,productmeasure,purchasequantity,purchaseamount
86246,205,7,707,1078778070,12564,2012-03-02,12,OZ,1,7.59
86246,205,63,6319,107654575,17876,2012-03-02,64,OZ,1,1.59
86246,205,97,9753,1022027929,0,2012-03-02,1,CT,1,5.99
'''

###### Need to find type in



################## Initial Load and type check Max Value    ##########################################
df1= pd.read_csv(file_transact, sep=',', nrows= 100)
dfs= df1.describe()
print df1.head(10),"\n",  "\n\n",  util.pd_dtype_print(df1)
dfs[dfs.index.isin(['min', 'max'])]


ds= {'id': 'uint32', 'chain': 'uint16', 'dept': 'uint16', 'category': 'uint32', 'company': 'uint32',
'brand': 'uint32', 'date': 'object', 'productsize': 'float16', 'productmeasure': '|S2',
'purchasequantity': 'uint16', 'purchaseamount': 'float16'}


#Check
df1= pd.read_csv(file_transact, sep=',', nrows= 10, dtype=ds)
print util.pd_dtype_print(df1), '\n', df1.head(3)



#Full Load, 10mio: 1.5Go, Remove Columns
df1= pd.read_csv(file_transact, sep=',', nrows= 1*10**6, usecols=np.arange(1,9), dtype=ds)
print df1.describe(),"\n",  util.pd_info_memsize(df1)

# util.session_save('kaggle_supermarket02', globals())


################## Get  Category distribution   ##################################################
catdict  = da.csv_col_get_dictfreq(file_transact, category_cols= [1, 2, 3, 4, 5, 7, 8], maxline=1 * 10 ** 6)
util.py_save_obj(catdict, '/kaggle/catdict')
# 'D:\\_devs\\Python01\\project27/aaserialize/catdict.pkl'


catfreq= da.col_categorydict_freqstudy(catdict)
# util.py_save_obj(catfreq, '/kaggle/catfreq')



catfreq= util.py_load_obj('/kaggle/catfreq')


# Generate the categories values to be kept   -----------------------------------------------------
file_category=  in1+ "offers.csv"
ncol= 8   #nb of Column than in Transaction File
catval_tokeep=[ {} for i in xrange(0, ncol)]
for i, line in enumerate(open(file_category)):
    ll=  line.split(",")
    catval_tokeep[3][  ll[1] ]  = 1  # Offer_file_col1 --> Transact_file_col_3
    catval_tokeep[4][  ll[3] ] =  1  # Offer_file_col3 --> Transact_file_col_4

catval_tokeep


#Filter function to select row based on some pre-filled category / conditions---------------------
def condfilter(colk, catval_tokeep) :
  if colk[3] in catval_tokeep[3] or colk[4] in catval_tokeep[4]: return True
  else: return False


da.csv_row_reduce_line(fromfile=file_transact, tofile=file_reduced, condfilter=condfilter,
                       catval_tokeep=catval_tokeep, maxline=100)


infile2=  file_reduced


#------Features Generation from data   ---------------------------------------------------------
util.session_save('/kaggle/supermarket_01', globals())


catval_tokeep2= util.np_dict_tolist(catval_tokeep)




### Add Date  ----------------------------------------------------------------------
import arrow
### arrow is super slow

def day(t):   return arrow.get(t, 'YYYY-MM-DD HH:mm:ss').day
def season(d):
  m= arrow.get(d, 'YYYY-MM-DD HH:mm:ss').month
  if m > 3 and m  < 10 : return 1 
  else : return 0  

def daytime(d):
  h= arrow.get(d, 'YYYY-MM-DD HH:mm:ss').hour
  if h < 11 :   return 0
  elif h < 14 : return 1    #lunch
  elif h < 18 : return 2    # afternoon
  elif h < 21 : return 3    # dinner
  else :        return 4   #night

coldate=  'purchased_at'   ; fmt= 'YYYY-MM-DD HH:mm:ss'
df_v1['day']=     df_v1[coldate].apply(day).astype('int8') 
df_v1['month']=   df_v1[coldate].apply(lambda t: arrow.get(t, fmt).month).astype('int8') 
df_v1['year']=    df_v1[coldate].apply(lambda t: arrow.get(t, fmt).year).astype('int16') 
df_v1['hour']=    df_v1[coldate].apply(lambda t: arrow.get(t, fmt).hour).astype('int8') 
df_v1['weekday']= df_v1[coldate].apply(lambda t: arrow.get(t, fmt).weekday).astype('int8') 
df_v1['season']=  df_v1[coldate].apply(season).astype('int8') 
df_v1['daytime']= df_v1[coldate].apply(daytime).astype('int8') 


df_v1.to_csv(out1+'/purchasings_v1.csv')









##################################################################################################
'''
Batch mode to re-collect the data
SQL batch on 1 million line
 Year / Month  /  LocationType  / DrinkType /Brand

Flat Files

10 million DAY


MachineID, DrinkID

pivot

http://jihan.30maps.com/map/67061


'''


''' Map Reduce
product ---> Soda / Coffee / Water   Hot / Cold

Machines ---> LocationType         Conbini /
(Onsen area, bath, Sport area, Functionnal, ...)


Seasonanlity ---> Split in Time


SQL Data


From one Place ---> Need to find amenuiities within 50m

'''


util.session_save("/kaggle/kaggle_supermarket_01")


# Distribition

# pandas Method for First Analysis :
df.describe(), df1.hist()


#Histogram by Class
df1.groupby('company').hist()


# Feature vs Feature Distribution / Col vs Col
from pandas.tools.plotting import scatter_matrix
scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
'''
# 25s for 1m line

'''
#--------------------------
SALES.groupby('name')['quantity'].sum().plot(kind="bar")

'''
# Accidents which happened on a Sunday, > 20 cars
rs = df[ (df.Day_of_Week == 1) & (df.Number_of_Vehicles > 20)]

# Convert date to Pandas date/time
london_data_2000 = data[
    (pd.to_datetime(data['Date'], coerce=True) >
        pd.to_datetime('2000-01-01', coerce=True)) &
    (pd.to_datetime(data['Date'], coerce=True) <
        pd.to_datetime('2000-12-31', coerce=True))
]
'''


data_csv_mapreduce(loc_offers, loc_transactions, loc_reduced)






################################  IN MEMORY Structure #############################################
# Info Type :
util.pd_info_memsize(df2)

#Convert to pandas dataframe
df_pd= odo(df, pd.DataFrame)

util.pd_info_memsize(df_pd)



#------- Data Clean Up Before Saving -------------------------------------------------------------
df_pd2=  util.pd_dtypes_type1_totype2(df_pd, fromtype=np.datetime64, targetype=str)

df_pd2=  util.pd_dtypes_type1_totype2(df_pd, fromtype=np.int64, targetype=np.int32)

df_pd2= util.pd_h5_cleanbeforesave(df_pd2)


util.pd_h5_save(df_pd2, 'F:/_data/stock/intraday/q5min/usetf1.h5', 'data')


df3= util.pd_h5_load('F:/_data/stock/intraday/q5min/usetf1.h5', 'data')

util.pd_info_memsize(df3)

df.dshape



################### transformation Columns ######################################################
'''
transformation Columns :

df[['col2','col3']] = df[['col2','col3']].apply(pd.to_numeric)

df.apply(lambda x: pd.to_numeric(x, errors='ignore'))


'''


dir1= 'E:/_data/kaggle/largesuper/csv/'
df= odo(dir1 + '*train*.csv', pd.DataFrame) # Stream through many CSV files

odo(dir1 + '*train*.csv', 'hdfstore://'+dir1 +'file.h5::/df/')



################################ Saving File on DISK #############################################
#  Show data Type
pd.discover(df),  df.dshape

# ODO Conversion possibilities
 odo(df, list)  # create new list from Pandas DataFrame
 odo(df, [])  # append onto existing list
 odo(df, 'myfile.json')  # Dump dataframe to line-delimited JSON
 odo('myfiles.*.csv', Iterator) # Stream through many CSV files
 odo(df, 'postgresql://hostname::tablename')  # Migrate dataframe to Postgres
 odo('myfile.*.csv', 'postgresql://hostname::tablename')  # Load CSVs to Postgres
 odo('postgresql://hostname::tablename', 'myfile.json') # Dump Postgres to JSON
 odo('mongodb://hostname/db::collection', pd.DataFrame) # Dump Mongo to DataFrame


# To ensure that you encode your dataset appropriately we recommend passing a datashape explicitly.
# As in our previous example this can often be done by editing automatically generated datashapes
# Transpose into Datashape  Before Converting to Flat File
# ds = dshape("var * {name: string[20, 'ascii'], amount: float64}")
d.dshape

ds= od.dshape("""var * {
  date: string[30, 'unicode'],
  open: float64, high: float64, low: float64, close: float64, volume: int64,
  symbol: string[6, 'unicode'],
  dateyear: int32, month: int32,day: int32,   hour: int32,  minute: int32
  }""")

#Size of Datetime : len(str( df_pd['date'].values[0]  ))


#  Convert to Format
odo(df_pd, 'F:/_data/stock/intraday/q5min/usetf2.bcolz', dshape=ds)


#Test of Loading it
df2= bz.data('F:/_data/stock/intraday/q5min/usetf1.bcolz')
df2.head(5),  bz.mean(df2.close






# BCOLZ :  Only for Numerical / Need Datashape to reformat data
odo(file1, 'F:/_data/stock/intraday/q5min/q5min_etf.bcolz')


#NO NO ODO HDFS: ODO is bad   : Need to Clean Up the data, BETTER TO Pandas Directly
odo(df2, 'hdfstore://F:/_data/stock/intraday/q5min/usetf9.h5::/data/')

odo(df_pd[['open','close', 'symbol']], 'hdfstore://F:/_data/stock/intraday/q5min/usetf2.h5::/data/')


#Pandas HDFS: Need to Clean Up the data, BETTER TO Pandas Directly, Release Lock
df_pd= util.pd_hdfs_cleanbeforesave(df_pd)

util.pd_h5_save(df_pd2[['open','sym']], 'F:/_data/stock/intraday/q5min/usetf11.h5', 'data')

df3= util.pd_h5_load('F:/_data/stock/intraday/q5min/usetf9.h5', 'data')


# into  SINGLE CSV
odo(df_pd, 'F:/_data/stock/intraday/q5min/usetf.csv')


#PKL on Pandas table
util.py_save_obj(df_pd, 'F:/_data/stock/intraday/q5min/usetf.pkl', otherfolder=1)


# SQLite  Database


# Job Lib to save Numpy array : Better
# Joblib, with 2 different versions, 0.9.4 and master (dev),




'''

#NO NO  ODO  Pytable NO NOcannot support date  NEVER USE
odo(df3, 'F:/_data/stock/intraday/q5min/usetf.h5::/data/')

#NO NO :   NUMPY MEMMAP : NO only 2.5go
    generators (e.g. to read a file a line at a time)
    Key-value stores (e.g. redis)
    SQL and NoSQL databases (e.g. sqlite3)
'''


###########################################################################################




#Unicode Issues with HFS
types = df_pd.apply(lambda x: pd.lib.infer_dtype(df_pd.values))

types[types=='unicode']

for col in types[types=='unicode'].index:
   # df_pd[col] = df_pd[col].astype(str)
   df[col] = df[col].apply(lambda x: x.encode('utf-8').strip())






#  Expression Interactive :

db.iris.species.<tab
db.iris.species.columns       db.iris.species.max
db.iris.species.count         db.iris.species.min
db.iris.species.count_values  db.iris.species.ndim
db.iris.species.distinct      db.iris.species.nunique
db.iris.species.dshape        db.iris.species.relabel
db.iris.species.expr          db.iris.species.resources
db.iris.species.fields        db.iris.species.schema
db.iris.species.head          db.iris.species.shape
db.iris.species.isidentical   db.iris.species.sort
db.iris.species.label         db.iris.species.species
db.iris.species.like          db.iris.species.to_html
db.iris.species.map











#Cannot Compute any expression in Blaze

from dateutil.parser import parse
dateparse= lambda x: parse(x)





#  Cannot apply
def colfun(x) : lambda  : x+5
   x+5


bz.transform(df, dateday = util.datestring_todatetime(df.date) )

datetimes = t.time.map(datetime.utcfromtimestamp,     schema='{time: datetime}')


df[0,5].values

df.amount.map(lambda x: x + 1,  'int64')

df_pd= df[1:500]

df_pd.count()


bz.mean(df.close)



df2= df.apply(colfun, dshape='float32')  # Hash value of resultant dataset


#  Data
http://blaze.pydata.org/blog/2015/09/08/reddit-comments/

http://blaze.pydata.org/blog/2015/09/08/reddit-comments/


# Type Conversion
Type conversion of expressions can be done with the coerce expression. Here’s how to compute the average account balance
for all the deadbeats in my accounts table and then cast the result to a 64-bit integer:


 deadbeats = accounts[accounts.balance < 0]
 avg_deliquency = deadbeats.balance.mean()
 chopped = avg_deliquency.coerce(to='int64')
 chopped.mean(accounts[accounts.balance < 0].balance).coerce(to='int64')


############## Cost      ########################
http://odo.pydata.org/en/latest/aws.html



#####################################################################################
#########################  LOAD Data  ###############################################
df = bz.data('sqlite:///%s::iris' % bz.utils.example('iris.db'))

df = bz.data('my-small-file.csv')

df = bz.data('myfile-2014-01-*.csv.gz')

HDFS  ::/datapath

engine = sql.create_engine('postgresql://%s:%s@localhost:5432/%s' %(myusername, mypassword, mydatabase))
df     = bz.data(engine)

engine = sql.create_engine('postgresql://myusername:mypassword@localhost:5432/mydatabase' %(myusername, mypassword, mydatabase))



#Show the data
df.peek()




#----------------------Server     ---------------------------------------------------
from numba import vectorize, float64
from numpy import linspace, pi
from blaze import Data, discover, sqrt, exp
x = Data(linspace(-5, 5, 100000000))
mu, sigma = -1.33, 1.25
expr = 1 / (sigma * sqrt(2 * pi)) * exp(-(x - mu) ** 2 / (2 * sigma ** 2))






#####################################################################################
#########################  CLEAN   ##################################################
df.relabel(name='alias',  amount='dollars')

#Remove Duplicate
df.distinct()
df.name.distinct()


df= df[df.amount < 0]

#####################################################################################
#########################  MAP REDUCE  ##############################################
# Group by and Map-Reduce operations
bz.by(df.species, minimum=df.petal_length.min(), maximum=df.petal_length.max(),
                  ratio= df.petal_length.max() - df.petal_length.min())


df['petal_length'].count()

df['petal_length'].map(lambda x: x + 1,'int64')


bz.transform(df, sepal_ratio = df.sepal_length / df.sepal_width,
                 petal_ratio = df.petal_length / df.petal_width)


df.petal_length.map(lambda x: x + 1,'float64')



#Find Colmun= text
df[df.species.like('*versicolor')]


# Add new Columns : Add new columns using the transform function

transform(iris, sepal_ratio = iris.sepal_length / iris.sepal_width,
                petal_ratio = iris.petal_length / iris.petal_width)


#Convert file to dataframe
odo((1, 2, 3), pd.DataFrame)




#####################################################################################
#########################  LOAD Data  ###############################################
df = bz.data('sqlite:///%s::iris' % bz.utils.example('iris.db'))

df = bz.data('my-small-file.csv')

df = bz.data('myfile-2014-01-*.csv.gz')

#Show the data
df.peek()




Basic Queries
Here we give a quick overview of some of the more common query functionality.

We use the well known iris dataset

 from blaze import data
 from blaze.utils import example
 iris = data(example('iris.csv'))
 iris.peek()
    sepal_length  sepal_width  petal_length  petal_width      species
0            5.1          3.5           1.4          0.2  Iris-setosa
1            4.9          3.0           1.4          0.2  Iris-setosa
2            4.7          3.2           1.3          0.2  Iris-setosa
3            4.6          3.1           1.5          0.2  Iris-setosa
...
Column Access
Select individual columns using attributes

 iris.species
        species
0   Iris-setosa
1   Iris-setosa
2   Iris-setosa
3   Iris-setosa
...
Or item access

 iris['species']
        species
0   Iris-setosa
1   Iris-setosa
2   Iris-setosa
3   Iris-setosa
...
Select many columns using a list of names

 iris[['sepal_length', 'species']]
    sepal_length      species
0            5.1  Iris-setosa
1            4.9  Iris-setosa
2            4.7  Iris-setosa
3            4.6  Iris-setosa
...
Mathematical operations
Use mathematical operators and functions as normal

 from blaze import log
 log(iris.sepal_length * 10)
    sepal_length
0       3.931826
1       3.891820
2       3.850148
3       3.828641
...
Note that mathematical functions like log should be imported from blaze. These will translate to np.log, math.log, sqlalchemy.sql.func.log, etc. based on the backend.

Reductions
As with many Blaze operations reductions like sum and mean may be used either as methods or as base functions.

 iris.sepal_length.mean()
5.84333333333333...

 from blaze import mean
 mean(iris.sepal_length)
5.84333333333333...
Split-Apply-Combine
The by operation expresses split-apply-combine computations. It has the general format

 by(table.grouping_columns, name_1=table.column.reduction(),
...                            name_2=table.column.reduction(),
...                            ...)
Here is a concrete example. Find the shortest, longest, and average petal length by species.

 from blaze import by
 by(iris.species, shortest=iris.petal_length.min(),
...                   longest=iris.petal_length.max(),
...                   average=iris.petal_length.mean())
           species  average  longest  shortest
0      Iris-setosa    1.462      1.9       1.0
1  Iris-versicolor    4.260      5.1       3.0
2   Iris-virginica    5.552      6.9       4.5
This simple model can be extended to include more complex groupers and more complex reduction expressions.

Add Computed Columns
Add new columns using the transform function

 transform(iris, sepal_ratio = iris.sepal_length / iris.sepal_width,
...                 petal_ratio = iris.petal_length / iris.petal_width)
    sepal_length  sepal_width  petal_length  petal_width      species  \
0            5.1          3.5           1.4          0.2  Iris-setosa
1            4.9          3.0           1.4          0.2  Iris-setosa
2            4.7          3.2           1.3          0.2  Iris-setosa
3            4.6          3.1           1.5          0.2  Iris-setosa

    sepal_ratio  petal_ratio
0      1.457143     7.000000
1      1.633333     7.000000
2      1.468750     6.500000
3      1.483871     7.500000
...
Text Matching
Match text with glob strings, specifying columns with keyword arguments.

 iris[iris.species.like('*versicolor')]
    sepal_length  sepal_width  petal_length  petal_width          species
50           7.0          3.2           4.7          1.4  Iris-versicolor
51           6.4          3.2           4.5          1.5  Iris-versicolor
52           6.9          3.1           4.9          1.5  Iris-versicolor
Relabel Column names
 iris.relabel(petal_length='PETAL-LENGTH', petal_width='PETAL-WIDTH')
    sepal_length  sepal_width  PETAL-LENGTH  PETAL-WIDTH      species
0            5.1          3.5           1.4          0.2  Iris-setosa
1            4.9          3.0           1.4          0.2  Iris-setosa
2            4.7          3.2           1.3          0.2  Iris-setosa
Examples
Blaze can help solve many common problems that data analysts and scientists encounter. Here are a few examples of common issues that can be solved using blaze.

Combining separate, gzipped csv files.
 from blaze import odo
 from pandas import DataFrame
 odo(example('accounts_*.csv.gz'), DataFrame)
   id      name  amount
0   1     Alice     100
1   2       Bob     200
2   3   Charlie     300
3   4       Dan     400
4   5     Edith     500
Split-Apply-Combine
 from blaze import data, by
 t = data('sqlite:///%s::iris' % example('iris.db'))
 t.peek()
    sepal_length  sepal_width  petal_length  petal_width      species
0            5.1          3.5           1.4          0.2  Iris-setosa
1            4.9          3.0           1.4          0.2  Iris-setosa
2            4.7          3.2           1.3          0.2  Iris-setosa
3            4.6          3.1           1.5          0.2  Iris-setosa
4            5.0          3.6           1.4          0.2  Iris-setosa
5            5.4          3.9           1.7          0.4  Iris-setosa
6            4.6          3.4           1.4          0.3  Iris-setosa
7            5.0          3.4           1.5          0.2  Iris-setosa
8            4.4          2.9           1.4          0.2  Iris-setosa
9            4.9          3.1           1.5          0.1  Iris-setosa
...
 by(t.species, max=t.petal_length.max(), min=t.petal_length.min())
           species  max  min
0      Iris-setosa  1.9  1.0
1  Iris-versicolor  5.1  3.0
2   Iris-virginica  6.9  4.5





#############################################################################################################
#############################################################################################################
#------ Output Directory    ####################################################################
dir2='E:/_data/stock/intraday/raw/'
now1= util.date_now()


#------------------Download 5min US ETF ########################################################
sym= alldata.us_etf_all_0
inter_sec= 300; nday=6000
for symbol in sym:
  pf.imp_googleIntradayQuoteSave(symbol,  inter_sec, nday, dircsv= dir2 +  'usetf_' + now1  )



#------------------Download 5min US Stock- #####################################################
sym= alldata.us_sp2000
inter_sec= 300; nday=6000
for symbol in sym:
  pf.imp_googleIntradayQuoteSave(symbol,  inter_sec, nday, dircsv= dir2 + 'ustock_' + now1 )





#------------------ Backup database  #####################################################
now1= util.date_now()
util.os_zipfolder('E:/_data/stock/intraday/q5min/',  'E:/_data/stock/intraday/q5min_'+now1 +'.zip',
                  iscompress= True)



#------------------ update Master  DB ###################################################
indir0=   'E:/_data/stock/intraday/raw/'
dirlist=    util.os_file_listall(indir0, '*', 1, onlyfolder=1)[0]

for dir0 in dirlist :
  dirname=  dir0[:dir0.find('_')]
  indir1= indir0 + dir0 +'/'
  file1= util.os_file_listall(indir1, '*.csv', 0)[:,0]
  file1= np.array([  x+'.csv' for  x in   file1  ])

  print dir0, dirname, len(file1)

  imp_db_csv_update(indir=indir1,
                      outdir='E:/_data/stock/intraday/q5min/'+dirname+'/', filelist=file1, intype='csv',
                      refcols=['date', 'open', 'high', 'low', 'close', 'volume', 'symbol'])

#############################################################################################################
#############################################################################################################






#   Select Column not in the Dataframe




raise KeyError('%s not in index' % objarr[mask])
KeyError: "['date' 'open' 'high' 'low' 'close' 'volume' 'symbol'] not in index"



'''
indir1= indir0 + 'usetf_20161208/'
file1= util.os_file_listall(indir1, '*.csv', 0)[:,0]
file1= np.array([  x+'.csv' for  x in   file1  ])


df= imp_csv_dbupdate(indir=indir1,
                      outdir='E:/_data/stock/intraday/q5min/usetf/', filelist=file1, intype='csv',
                      refcols=['date', 'open', 'high', 'low', 'close', 'volume', 'symbol'])



#------------------ update Master STOCK  ##############################################
indir1= 'E:/_data/stock/intraday/raw/' + 'ustock_20161208/'

file1= util.os_file_listall(indir1, '*.csv', 0)[:,0]
file1= np.array([  x+'.csv' for  x in   file1  ])


df= imp_csv_dbupdate(indir=indir1,
                      outdir='E:/_data/stock/intraday/q5min/ustock/', filelist=file1, intype='csv',
                      refcols=['date', 'open', 'high', 'low', 'close', 'volume', 'symbol'])





df= imp_csv_dbupdate(indir=indir1,
                      outdir='E:/_data/stock/intraday/q5min/us/etf/', filelist=file1, intype='csv',
                      refcols=['date', 'open', 'high', 'low', 'close', 'volume', 'symbol'])




df





#------------------ Put into Database -------------------------------------------



import odo

odo('sqlite:///db.db::q5min_etf', )






import bcolz


file1= 'E:/_data/stock/intraday/20161207_etf/NKE_20160928_300_6000.csv'
df= pf.imp_csv_toext(file1= file1,  sym='NKE', header=0,
cols= ['date', 'symbol','open','high','low','close','volume'], date=[1],
fromzone='Japan', tozone='UTC')



dircsv= 'E:/_data/stock/intraday/20161115_etf/'
df= pf.imp_hdfs_db_updatefromcsv(dircsv,filepd= r'E:/_data/stock/intraday/q5min/us/etf/',
                                 fromtimezone='Japan', tozone='UTC')



DIRCWD= 'E:/_data/stock/intraday/intraday_google_usetf2.h5'
df= pf.imp_hdfs_getquote(DIRCWD, 'SPY')
df1 = df[['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']]




df2= pf.imp_csv_toext(file1='E:/_data/stock/intraday/q5min/us/etf/SPY.csv',
      fromzone='Japan', tozone='UTC', header=0,
      cols=['date', 'open','high','low','close','volume', 'symbol'])

df2.date.values[0]










sym1= np.array(['AAXJ','ACWI','ACWV','ACWX','AGG','AGZ','AMJ','AMLP','AMU','AOM','ASHR','ATMP','BAB','BBH','BIL','BIV','BKLN','BLV','BND','BNDS','BNDX','BNO','BOND','BSCG','BSCH','BSCI','BSCJ','BSCK','BSCM','BSJH','BSJI','BSJJ','BSV','BWX','CHAD','CIU','CLY','CMF','CORN','CORP','CSJ','CSM','CWB','CWI','DBA','DBAW','DBB','DBC','DBEF','DBEM','DBEU','DBJP','DBKO','DBO','DBP','DEM','DES','DFE','DFJ','DGL','DGRO','DGRW','DHS','DIA','DIV','DJP','DLN','DLS','DNO','DOG','DON','DSI','DTN','DTO','DVY','DWM','DWX','DXJ','DZZ','ECH','EDV','EELV','EEM','EEMA','EEMS','EEMV','EFA','EFAV','EFG','EFV','EFZ','EIDO','EIS','EMB','EMLC','EMLP','EPHE','EPI','EPOL','EPP','EPU','ERUS','EUFN','EUM','EWA','EWC','EWD','EWG','EWH','EWI','EWJ','EWL','EWM','EWN','EWP','EWQ','EWS','EWT','EWU','EWW','EWY','EWZ','EXI','EZA','EZU','FBT','FCG','FCOM','FDL','FDN','FDT','FENY','FEX','FEZ','FHLC','FIDU','FLOT','FM','FNCL','FNDA','FNDF','FNDX','FNX','FPE','FPX','FSTA','FTA','FTC','FTSD','FTSL','FTSM','FUTY','FV','FVD','FXA','FXB','FXC','FXD','FXE','FXG','FXH','FXI','FXL','FXO','FXU','FXY','FYX','GDX','GDXJ','GGOV','GLD','GMF','GMM','GNR','GOVT','GREK','GSG','GSLC','GSY','GUNR','GVI','GWX','GXC','HACK','HDG','HDGE','HDV','HEDJ','HEFA','HEWG','HEWJ','HEZU','HYD','HYEM','HYG','HYLS','HYMB','HYS','IAT','IAU','IBB','ICF','IDLV','IDU','IDV','IEF','IEFA','IEI','IEMG','IEO','IEUR','IEV','IEZ','IFGL','IGE','IGF','IGOV','IGV','IHDG','IHE','IHF','IHI','IJH','IJJ','IJK','IJR','IJS','IJT','ILF','INDA','INDY','ISTB','ITA','ITB','ITE','ITM','ITOT','ITR','IUSG','IUSV','IVE','IVV','IVW','IWB','IWC','IWD','IWF','IWM','IWN','IWO','IWP','IWR','IWS','IWV','IWY','IXC','IXJ','IXP','IXUS','IYC','IYE','IYF','IYG','IYH','IYJ','IYK','IYM','IYR','IYT','IYW','IYY','IYZ','JJC','JKE','JNK','KBE','KBWB','KIE','KRE','KWEB','KXI','LEMB','LQD','LTPZ','MBB','MCHI','MDY','MDYG','MDYV','MGC','MGK','MGV','MINT','MLPI','MLPN','MOO','MTUM','MUB','NEAR','NIB','NOBL','NTG','OEF','OIH','OIL','ONEQ','OUSA','PALL','PBP','PCY','PDP','PEJ','PEY','PFF','PGF','PGX','PHB','PHDG','PHYS','PICK','PID','PIE','PIN','PJP','PKW','PPH','PPLT','PRF','PSL','PSP','PSQ','PWB','PWV','PXH','PZA','QAI','QDEF','QDF','QQEW','QQQ','QUAL','REGL','REM','RFG','RGI','RHS','RIGS','RLY','RPG','RPV','RSP','RSX','RWO','RWR','RWX','RYH','RYT','RYU','SBIO','SCHA','SCHB','SCHC','SCHD','SCHE','SCHF','SCHG','SCHH','SCHM','SCHO','SCHP','SCHR','SCHV','SCHX','SCHZ','SCIF','SCPB','SCZ','SDIV','SDOG','SDY','SGOL','SH','SHM','SHV','SHY','SHYG','SIL','SJB','SJNK','SKYY','SLV','SLYG','SMH','SNLN','SOXX','SPHD','SPHQ','SPLV','SPY','SPYG','SRLN','STIP','STPZ','SUB','SVXY','SWH','TAN','TBF','TFI','THD','TILT','TIP','TLH','TLO','TLT','TLTD','TLTE','TOTL','TTFS','TUR','TUZ','UGA','UNG','USL','USMV','USO','UUP','VAW','VB','VBK','VBR','VCIT','VCLT','VCR','VCSH','VDC','VDE','VEA','VEU','VFH','VGIT','VGK','VGLT','VGSH','VGT','VHT','VIG','VIIX','VIS','VIXY','VLUE','VMBS','VNM','VNQ','VNQI','VO','VOE','VONG','VONV','VOO','VOOG','VOT','VOX','VPL','VPU','VRP','VSS','VT','VTEB','VTI','VTIP','VTV','VUG','VV','VWO','VWOB','VXF','VXUS','VXX','VXZ','VYM','WDTI','WOOD','XBI','XES','XHB','XIV','XLB','XLE','XLF','XLG','XLI','XLK','XLP','XLU','XLV','XLY','XME','XMLV','XOP','XPH','XRT','ZROZ'])


imp_csv_dbupdate(indir='E:/_data/stock/intraday/intraday_google_usetf2.h5',
                  outdir='E:/_data/stock/intraday/q5min/us/etf/', symbols=sym1  ,intype='hdfs')



pf.imp_hdfs_db_dumpinfo()



sym= np.array(['A','AA','AAL','AAP','AAPL','AAXJ','ABBV','ABC','ABT','ACAD','ACC','ACGL','ACH','ACHC','ACHN','ACM','ACN','ACOR','ACWI','ACWV','ACWX','ADAP','ADBE','ADI','ADM','ADP','ADRO','ADS','ADSK','ADT','AEE','AEG','AEM','AEP','AER','AES','AET','AFG','AFL','AFSI','AGG','AGIO','AGN','AGNC','AGQ','AGR','AGU','AGZ','AIG','AIMT','AIV','AIZ','AJG','AKAM','ALB','ALDR','ALGN','ALK','ALKS','ALL','ALLE','ALLY','ALNY','ALR','ALV','ALXN','AMAT','AMCX','AME','AMG','AMGN','AMJ','AMLP','AMP','AMRI','AMT','AMU','AMZN','AN','ANAC','ANIK','ANSS','ANTM','AOM','AON','AOR','AOS','APA','APC','APD','APH','AR','ARE','ARG','ARIA','ARMK','ARRS','ARW','ASH','ASHR','ASX','ATHN','ATMP','ATO','ATR','ATRA','ATVI','AU','AVAL','AVB','AVGO','AVT','AVY','AWK','AXON','AXP','AXS','AXTA','AYI','AZO','BA','BAB','BAC','BAP','BAX','BBBY','BBH','BBT','BBY','BCH','BCR','BDX','BEAV','BEN','BEP','BG','BGNE','BHI','BIB','BIIB','BIL','BIP','BIS','BIV','BK','BKFS','BKLN','BLK','BLL','BLUE','BLV','BMRN','BMS','BMY','BND','BNDS','BNDX','BNO','BOND','BPL','BPY','BR','BRFS','BRKR','BRO','BRX','BRZU','BSAC','BSCG','BSCH','BSCI','BSCJ','BSCK','BSCL','BSCM','BSJH','BSJI','BSJJ','BSMX','BSV','BSX','BUFF','BWA','BWX','BXLT','BXP','BZQ','C','CA','CAG','CAH','CAT','CB','CBG','CBM','CBOE','CBPO','CBS','CCE','CCI','CCJ','CCK','CCL','CDK','CDNS','CDW','CE','CEA','CELG','CEMP','CERN','CERS','CF','CFG','CG','CGW','CHAD','CHAU','CHD','CHK','CHRS','CHRW','CI','CIB','CINF','CIT','CIU','CL','CLB','CLLS','CLR','CLVS','CLX','CLY','CMA','CMCSA','CME','CMF','CMG','CMI','CMS','CNA','CNC','CNCO','CNHI','CNP','COF','COG','COH','COL','COMM','COO','COP','CORN','CORP','COST','COTY','CPB','CPG','CPGX','CPL','CPN','CPRT','CPT','CQH','CQP','CRI','CRM','CSCO','CSGP','CSJ','CSL','CSM','CSRA','CSX','CTAS','CTL','CTSH','CTXS','CUBE','CURE','CVC','CVE','CVS','CVX','CWB','CWI','CX','CXO','D','DAL','DBA','DBAW','DBB','DBC','DBEF','DBEM','DBEU','DBGR','DBJP','DBKO','DBO','DBP','DD','DDM','DDR','DE','DEG','DEM','DERM','DES','DEW','DFE','DFJ','DFS','DG','DGAZ','DGL','DGLD','DGRO','DGRW','DGX','DHI','DHR','DHS','DIA','DIG','DIS','DISCA','DISCK','DIV','DJP','DKS','DLN','DLPH','DLR','DLS','DLTR','DNB','DNO','DO','DOG','DON','DOV','DOW','DOX','DPS','DPZ','DRE','DRI','DRIP','DRN','DSI','DTE','DTN','DTO','DUG','DUK','DUST','DVA','DVAX','DVN','DVY','DVYE','DWM','DWTI','DWX','DXCM','DXD','DXJ','DZZ','EA','EBAY','EBS','ECA','ECH','ECL','ED','EDC','EDIT','EDU','EDV','EDZ','EELV','EEM','EEMA','EEMS','EEMV','EEP','EFA','EFAV','EFG','EFV','EFX','EFZ','EIDO','EIS','EIX','EL','ELS','EMB','EMC','EMLC','EMLP','EMN','EMR','ENDP','ENI','ENTA','EOG','EPC','EPHE','EPI','EPOL','EPP','EPU','EPZM','EQGP','EQIX','EQM','EQR','EQT','ERIE','ERJ','ERUS','ERX','ERY','ES','ESRX','ESS','ETE','ETFC','ETN','ETR','EUFN','EUM','EUO','EW','EWA','EWBC','EWC','EWD','EWG','EWH','EWI','EWJ','EWL','EWM','EWN','EWP','EWQ','EWS','EWT','EWU','EWW','EWX','EWY','EWZ','EXC','EXEL','EXI','EXPD','EXPE','EXR','EZA','EZU','F','FANG','FAS','FAST','FAZ','FB','FBHS','FBR','FBT','FCAU','FCG','FCOM','FCX','FDC','FDL','FDN','FDS','FDT','FDX','FE','FENY','FEP','FEX','FEZ','FFIV','FGEN','FHLC','FIDU','FIS','FISV','FITB','FL','FLEX','FLIR','FLOT','FLR','FLS','FLT','FM','FMC','FNCL','FNDA','FNDF','FNDX','FNF','FNV','FNX','FOLD','FOX','FOXA','FPE','FPRX','FPX','FRC','FRT','FSLR','FSTA','FTA','FTC','FTI','FTNT','FTR','FTSD','FTSL','FTSM','FUTY','FV','FVD','FWP','FXA','FXB','FXC','FXD','FXE','FXG','FXH','FXI','FXL','FXO','FXP','FXU','FXY','FYX','G','GAS','GASL','GASX','GBT','GD','GDDY','GDX','GDXJ','GE','GG','GGG','GGOV','GGP','GIB','GIL','GILD','GIS','GLD','GLPG','GLW','GM','GMF','GMM','GNR','GNTX','GOLD','GOOG','GOOGL','GOVT','GPC','GPN','GPS','GRA','GREK','GRFS','GRMN','GS','GSG','GSLC','GSY','GT','GUNR','GUSH','GVI','GWW','GWX','GXC','GXP','H','HACK','HAL','HALO','HAR','HAS','HBAN','HBI','HCA','HCN','HCP','HD','HDG','HDGE','HDS','HDV','HEDJ','HEFA','HES','HEWG','HEWJ','HEZU','HFC','HIG','HII','HIW','HLF','HOG','HOLX','HON','HOT','HP','HPE','HPQ','HRB','HRL','HRS','HSIC','HST','HSY','HTZ','HUBB','HUM','HYD','HYEM','HYG','HYLS','HYMB','HYS','IAT','IAU','IBB','IBM','ICE','ICF','ICL','ICPT','IDLV','IDU','IDV','IDXX','IEF','IEFA','IEI','IEMG','IEO','IEP','IEUR','IEV','IEX','IEZ','IFF','IFGL','IGE','IGF','IGM','IGOV','IGV','IHDG','IHE','IHF','IHG','IHI','IHS','IJH','IJJ','IJK','IJR','IJS','IJT','ILB','ILF','ILMN','IM','IMGN','IMS','INCY','INDA','INDY','INGR','INO','INSM','INSY','INTC','INTU','IONS','IP','IPG','IPGP','IPS','IQDF','IR','IRM','ISRG','ISTB','IT','ITA','ITB','ITC','ITCI','ITE','ITIP','ITM','ITOT','ITR','ITW','IUSG','IUSV','IVE','IVV','IVW','IVZ','IWB','IWC','IWD','IWF','IWM','IWN','IWO','IWP','IWR','IWS','IWV','IWY','IXC','IXJ','IXP','IXUS','IYC','IYE','IYF','IYG','IYH','IYJ','IYK','IYM','IYR','IYT','IYW','IYY','IYZ','JAH','JAZZ','JBHT','JBLU','JCI','JDST','JEC','JHX','JJC','JKD','JKE','JKHY','JLL','JNJ','JNK','JNPR','JNUG','JO','JPM','JUNO','JWN','K','KAR','KB','KBE','KBWB','KERX','KEY','KEYS','KHC','KIE','KIM','KITE','KKR','KLAC','KMB','KMI','KMX','KO','KOF','KORS','KR','KRC','KRE','KSS','KSU','KT','KWEB','KXI','L','LABD','LABU','LAMR','LAZ','LB','LEA','LEG','LEMB','LEN','LGND','LH','LII','LKQ','LLL','LLTC','LLY','LM','LMCA','LMCK','LMT','LNC','LNG','LNT','LOW','LPL','LPT','LQD','LRCX','LTPZ','LUK','LULU','LUV','LVLT','LXRX','LYB','LYV','M','MA','MAA','MAC','MACK','MAN','MAR','MAS','MAT','MBB','MBLY','MBT','MCD','MCHI','MCHP','MCK','MCO','MCRB','MD','MDLZ','MDT','MDVN','MDY','MDYG','MDYV','MELI','MET','MGC','MGK','MGM','MGNX','MGV','MHG','MHK','MIC','MIDD','MIK','MINT','MJN','MKC','MKL','MKTX','MLM','MLPI','MLPN','MMC','MMM','MNK','MNKD','MNST','MO','MON','MOO','MOS','MPC','MPEL','MPLX','MRK','MRKT','MRO','MRVL','MS','MSCI','MSFT','MSI','MSM','MT','MTB','MTD','MTN','MTUM','MU','MUB','MUR','MVV','MXIM','MYL','N','NANR','NAVI','NBL','NCLH','NDAQ','NEAR','NEE','NEM','NEU','NFLX','NFX','NI','NIB','NK','NKE','NKTR','NLNK','NLSN','NLY','NNN','NOBL','NOC','NOV','NOW','NRG','NSC','NTAP','NTG','NTRS','NUAN','NUE','NUGT','NVAX','NVDA','NVR','NWL','NWSA','NYCB','O','OA','OAK','OC','ODFL','OEF','OGE','OHI','OI','OIH','OIL','OKE','OKS','OMC','OMER','ONCE','ONEQ','OPHT','OPK','ORCL','ORI','ORLY','OTEX','OUSA','OXY','PAA','PAC','PACB','PAGP','PALL','PANW','PAYX','PBA','PBCT','PBI','PBP','PBYI','PCAR','PCG','PCLN','PCY','PDCO','PDLI','PDP','PEG','PEJ','PEP','PEY','PF','PFE','PFF','PFG','PG','PGF','PGR','PGX','PH','PHB','PHDG','PHI','PHM','PHYS','PICK','PID','PIE','PII','PIN','PINC','PJP','PKG','PKI','PKW','PLD','PM','PNC','PNR','PNRA','PNW','PNY','POST','PPC','PPG','PPH','PPL','PPLT','PRF','PRGO','PRTA','PRU','PSA','PSL','PSLV','PSO','PSP','PSQ','PSX','PSXP','PTLA','PVH','PWB','PWR','PWV','PX','PXD','PXF','PXH','PYPL','PZA','Q','QAI','QCOM','QDEF','QDF','QGEN','QID','QIHU','QLD','QQEW','QQQ','QRVO','QSR','QUAL','QUNR','R','RACE','RAD','RAI','RARE','RCL','RDUS','RDY','RE','REG','REGL','REGN','REM','RF','RFG','RGA','RGEN','RGI','RHI','RHS','RHT','RIG','RIGS','RJF','RL','RLGY','RLY','RLYP','RMD','RNR','ROK','ROL','ROP','ROST','RPG','RPM','RPV','RRC','RS','RSG','RSP','RSX','RTN','RUSL','RUSS','RVNC','RWM','RWO','RWR','RWX','RYE','RYH','RYT','RYU','RZV','SABR','SAGE','SBAC','SBH','SBIO','SBNY','SBUX','SCG','SCHA','SCHB','SCHC','SCHD','SCHE','SCHF','SCHG','SCHH','SCHM','SCHO','SCHP','SCHR','SCHV','SCHW','SCHX','SCHZ','SCI','SCIF','SCO','SCPB','SCZ','SDIV','SDOG','SDOW','SDS','SDY','SE','SEE','SEF','SEIC','SEP','SERV','SGEN','SGOL','SH','SHI','SHLX','SHM','SHV','SHW','SHY','SHYG','SIG','SIL','SIVB','SIX','SJB','SJM','SJNK','SJR','SKF','SKX','SKYY','SLB','SLG','SLV','SLW','SLYG','SMG','SMH','SNA','SNDK','SNI','SNLN','SNPS','SO','SON','SOXL','SOXS','SOXX','SPB','SPG','SPGI','SPHD','SPHQ','SPIL','SPLK','SPLS','SPLV','SPR','SPXL','SPXS','SPXU','SPY','SPYG','SQM','SQQQ','SRC','SRCL','SRE','SRLN','SRPT','SRS','SRTY','SSNC','SSO','ST','STE','STI','STIP','STJ','STLD','STM','STPZ','STT','STWD','STX','STZ','SUB','SVXY','SWH','SWK','SWKS','SWN','SXL','SYF','SYK','SYMC','SYY','T','TAN','TAP','TARO','TBF','TBPH','TBT','TDC','TDG','TE','TEAM','TECH','TECL','TEL','TFI','TFSL','TFX','TGNA','TGT','THD','THS','TIF','TILT','TIP','TJX','TKC','TLH','TLO','TLT','TLTD','TLTE','TMF','TMK','TMO','TMV','TNA','TOL','TOTL','TQQQ','TRGP','TRIP','TRMB','TROW','TRQ','TRU','TRV','TS','TSCO','TSN','TSO','TSRO','TSS','TSU','TTC','TTFS','TUR','TUZ','TVIX','TWC','TWM','TWTR','TWX','TXN','TXT','TYC','TYL','TZA','UA','UA.C','UAL','UBIO','UCO','UDOW','UDR','UGA','UGAZ','UGI','UGLD','UGP','UHAL','UHS','ULTA','ULTI','UMC','UNG','UNH','UNM','UNP','UPRO','UPS','URBN','URE','URI','URTY','USB','USDU','USL','USLV','USMV','USO','UTHR','UTX','UUP','UVXY','UWM','UWTI','UYG','V','VAL','VAR','VAW','VB','VBK','VBR','VCIT','VCLT','VCR','VCSH','VDC','VDE','VEA','VER','VEU','VFC','VFH','VGIT','VGK','VGLT','VGSH','VGT','VHT','VIAB','VIG','VIIX','VIP','VIPS','VIS','VIXY','VLO','VLUE','VMBS','VMC','VNM','VNO','VNQ','VNQI','VNTV','VO','VOE','VONG','VONV','VOO','VOOG','VOOV','VOT','VOX','VOYA','VPL','VPU','VRP','VRSK','VRSN','VRTX','VSS','VT','VTEB','VTI','VTIP','VTR','VTV','VUG','VV','VWO','VWOB','VXF','VXUS','VXX','VXZ','VYM','VZ','WAB','WAT','WBA','WBC','WCN','WDAY','WDC','WDTI','WEC','WES','WF','WFC','WFM','WFT','WGP','WHR','WLK','WLTW','WM','WMB','WMT','WOOD','WOOF','WPC','WPZ','WR','WRB','WREI','WRI','WRK','WSM','WSO','WST','WTR','WU','WUBA','WWAV','WY','WYN','WYNN','XBI','XEC','XEL','XES','XHB','XIV','XL','XLB','XLE','XLF','XLG','XLI','XLK','XLNX','XLP','XLRN','XLU','XLV','XLY','XME','XMLV','XNCR','XOM','XON','XOP','XPH','XRAY','XRT','XRX','XT','XYL','Y','YANG','YHOO','YINN','YNDX','YPF','YUM','YZC','ZAYO','ZBH','ZBK','ZION','ZIOP','ZNH','ZROZ','ZTS'])





imp_csv_dbupdate(indir='E:/_data/stock/intraday/intraday_google_us.h5',
                  outdir='E:/_data/stock/intraday/q5min/us/stock/', symbols=sym  ,intype='hdfs')







def imp_db_hdfs_tonumpy()





Source de data

dest de data










df2['open']= 5

df=df2

from dateutil import parser


df.date= [util.datenumpy_todatetime(x)for x in  df.date.values ]



x= df.date.values[0]

datetime.fromtimestamp(x.astype('O')/1e9)


'''




'''
############## What to put in BColz/ zarr
   3D Array:  Time x Asset x Open Close High Low
   1 million quote per day
   2500 * 5= 12500







'''
##






type(df2.date.values[0])

df2

from dateutil.parser import parse

dateutil.parser.parse()

import pandas as pd


df3= pd.concat([df, df2], axis=0)


df4= df3.sort('date')



type(df.date.values[0])


from dateutil import parser
parser.parse("9/27/2016  10:55:00 PM")






   from_zone = tz.gettz(fromzone);   tozone = tz.gettz(tozone)
   dateparse= lambda x: (pd.datetime.strptime(x,'%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone).astimezone(tozone))
   # dateparse= lambda x: parse(x, tzinfos=from_zone).astimezone(to_zone)

   df = pd.read_csv(file1,sep=',',header=header, names=cols, parse_dates={'date': coldate }, date_parser=dateparse)
   df.date= [pd.to_datetime((str(x)[:-6])) for x in  df.date]
   df.date= [x.to_datetime() for x in  df.date]

   df.columns = [  x.lower() for x in df.columns.values ]
   # df.columns = ['date', 'symbol','open','high','low','close','volume']

   if util.find('symbol', df.columns.values) < 0 :
     df= util.pd_addcolumn(df, 'symbol')
     df['symbol']= sym

   return df


import util


df.drop(df.columns[[0]], axis=1, inplace=True)


'''
have long hungered for the ultimate, super-fast, super-scaleable data storage solution. I have used relational databases, kdb, flatfiles, and binary files. In the end, I used binary files in my research language of choice. My advice is to KISS. The choice of storage is actually not that critical (unless maybe you're working with options tick data). What is critical is how you decide to splay the data.

If you look at kdb, it can actually be quite slow if you don't splay (segment) the data for your particular need. It just gives you a fast management layer, but it is up to you to design the data storage on disk for your need. What you are trying to do is store the data in such a way so that you group together the data that you need and minimize the amount of extra data that has to be read off disk.

For me, I found storing data in binary format in the language that I do research in is the least amount of overhead. Managing a simple splay is easy. One key is don't be afraid to store multiple copies of your data for different research tasks, so long as the creation of the copies is driven off of one golden source. So for example, if you very often need all ticks for one stock for the past 5 years, then I would splay by stock. But if you also need all stocks for a given day, then I would store another dataset that splays by day. Process and store the data in a way that will be most useful to you.

If you are a big institution, then by all means spend the big $ to get kdb and hire a hotshot q programmer (b/c you are probably not going to figure it out on your own very easily). It is quite nice. But, if you are an individual, do the simple thing and move on to more interesting work.
'''


# create an in-memory numpy container
a = np.arange(10)
In [4]:
# create an in-memory carray container
b = bcolz.carray(a)

a= np.array( ['dsfsfksfksfufshjsfjjksfklsf sjfsdfs']*10*1000*1000 )


# create an in-memory carray container
b = bcolz.carray(a)




# create an on-disk carray container
c = bcolz.carray(a, rootdir='test3.bcolz', mode='w' )
c.flush()



d= bcolz.carray()


import util

df= util.pd_array_todataframe()


file1= 'E:/_data/stock/intraday/20161207_etf/NKE_20160928_300_6000.csv'
import bcolz
import pandas as pd

df = pd.read_csv(file1, delimiter=',')


ct = bcolz.ctable.fromdataframe(df, rootdir='dataframe.bcolz', mode='w' )











#---------------------- Ok,

Generally speaking, what was really important in this one was to find a way to cross validate(1st problem!)
and retain features (or interactions of them ) and then again there was the big difference
between the offers in the training and test set (2nd problem!).

For the first one we generally used a 1-vs-rest offers
' approach to test the AUC and sometimes even derivatives of that. For the second (problem) we tried to maximize the with-in offers' auc (how well the offers score individually irrespective of the rest) and the total AUC (e.g. how the different offers blend together) as separate objectives.

We used 3 (conceptually) different approaches (and some other minor blends):

1. Train with similar offers
2. Train with whether the customer would have bought the product anyway
3. Assume that some features work for all offers in the same way (like: if you bought the product before, that increases the probability of becoming/staying a repeater)

I can't stress enough how important it was to treat high-transaction IDs separate ' \
     'from "regular" IDs.
I shot up 150 places on the leader board just by doing that.

Then, breaking out training/testing by offer department was what made the rest of the difference.



--------------------------------------------------------------------------------------------------


Feature engineering

Feature engineering will be important in this competition, no matter the language or algorithms used.


We will generate the following features:

has_bought_company: the number of times a shopper has bought from the company on offer
has_bought_company_a: the total amount the shopper has bought from the company on offer
has_bought_company_q: the quantity of items bought from the company on offer.
has_bought_company_30: the number of times a shopper has bought from the company on offer in the 30 days before the date the coupon was offered.
has_bought_company_60: the number of times a shopper has bought from the company on offer in the 60 days before the date the coupon was offered.
...
has_bought_company_180: 180 days before
has_never_bought_company: a negative feature for when the shopper has never bought from the company on offer before.
These same features for:

has_bought_category: the number of times a shopper has bought from the category on offer
has_bought_brand: the number of times a shopper has bought from the brand on offer
Combinations of these:

has_bought_company_brand_category: if this feature is present the shopper has bought from the company, brand, and category on offer.
has_never_bought_company_brand: negative feature for the combination of brand and company purchase history.
Offer-related:

offer_value: The value of the coupon offer
offer_quantity: The number of products to redeem with the coupon
Total shopper spend:

total_shopper_spend: We take the total amount spend by the shopper in the reduced dataset.
Can you name some other possibly interesting features to generate?

Vowpal Wabbit

We train Vowpal Wabbit using quantile regression, 40 passes and a learning rate of 0.85. We turn the predictions into Kaggle's submission format.

Feature visualisation

Using the output from Vowpal Wabbit's wrapper vw-varinfo we generate the feature relevance plot below (code to generate this included):





#Kaggle Challenge:
#'Reduce the data and generate features' by Triskelion
#Very mediocre and hacky code, single-purpose, but pretty fast

from datetime import datetime, date
from collections import defaultdict

loc_offers = "kaggle_shop\\offers.csv"
loc_transactions = "kaggle_shop\\transactions.csv"
loc_reduced = "kaggle_shop\\reduced2.csv" # will be created


def data_csv_mapreduce(file_category, file_transact, file_reduced):
  ''' Reduce Data by filtering on some Category '''
  start = datetime.now()

  #Parse all categories and comps on offer in a dict
  offers_cat, offers_co = {}, {}
  for i, line in enumerate(open(file_category)):
    ll=  line.split(",")
    offers_cat[ ll[1] ] = 1
    offers_co[  ll[3] ] = 1


  #open output file
  with open(file_reduced, "wb") as outfile:
    #go through transactions file and reduce
    jj_new = 0
    for i, line in enumerate(open(file_transact)):
      if i == 0: outfile.write(line) #print header
      else:
        ll=  line.split(",")
        if ll[3] in offers_cat or ll[4] in offers_co:    #Condition  Filter : if category in offers dict
          outfile.write( line )
          jj_new += 1

      #progress
      if i % 5000000 == 0:  print i, jj_new, datetime.now() - start
  print i, jj_new, datetime.now() - start



def data_csv_mapreduce_chunk(csv_bigfile):
  chunksize =     10 * 10 ** 6
  df= pd.read_csv(csv_bigfile, chunksize=chunksize, lineterminator=',')




  df.to_csv(filenew, sep=',')



#reduce_data(loc_offers, loc_transactions, loc_reduced)

def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days


loc_train = "kaggle_shop\\trainHistory.csv"
loc_test = "kaggle_shop\\testHistory.csv"
loc_transactions = "kaggle_shop\\reduced2.csv"
loc_out_train = "kaggle_shop\\train.vw"
loc_out_test = "kaggle_shop\\test.vw"
def generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test):
	#keep a dictionary with the offerdata
	offers = {}
	for e, line in enumerate( open(loc_offers) ):
		row = line.strip().split(",")
		offers[ row[0] ] = row

	#keep two dictionaries with the shopper id's from test and train
	train_ids = {}
	test_ids = {}
	for e, line in enumerate( open(loc_train) ):
		if e > 0:
			row = line.strip().split(",")
			train_ids[row[0]] = row
	for e, line in enumerate( open(loc_test) ):
		if e > 0:
			row = line.strip().split(",")
			test_ids[row[0]] = row
	#open two output files
	with open(loc_out_train, "wb") as out_train, open(loc_out_test, "wb") as out_test:
		#iterate through reduced dataset
		last_id = 0
		features = defaultdict(float)
		for e, line in enumerate( open(loc_transactions) ):
			if e > 0: #skip header
				#poor man's csv reader
				row = line.strip().split(",")
				#write away the features when we get to a new shopper id
				if last_id != row[0] and e != 1:

					#generate negative features
					if "has_bought_company" not in features:
						features['never_bought_company'] = 1

					if "has_bought_category" not in features:
						features['never_bought_category'] = 1

					if "has_bought_brand" not in features:
						features['never_bought_brand'] = 1

					if "has_bought_brand" in features and "has_bought_category" in features and "has_bought_company" in features:
						features['has_bought_brand_company_category'] = 1

					if "has_bought_brand" in features and "has_bought_category" in features:
						features['has_bought_brand_category'] = 1

					if "has_bought_brand" in features and "has_bought_company" in features:
						features['has_bought_brand_company'] = 1

					outline = ""
					test = False
					for k, v in features.items():

						if k == "label" and v == 0.5:
							#test
							outline = "1 '" + last_id + " |f" + outline
							test = True
						elif k == "label":
							outline = str(v) + " '" + last_id + " |f" + outline
						else:
							outline += " " + k+":"+str(v)
					outline += "\n"
					if test:
						out_test.write( outline )
					else:
						out_train.write( outline )
					#print "Writing features or storing them in an array"
					#reset features
					features = defaultdict(float)
				#generate features from transaction record
				#check if we have a test sample or train sample
				if row[0] in train_ids or row[0] in test_ids:
					#generate label and history
					if row[0] in train_ids:
						history = train_ids[row[0]]
						if train_ids[row[0]][5] == "t":
							features['label'] = 1
						else:
							features['label'] = 0
					else:
						history = test_ids[row[0]]
						features['label'] = 0.5

					#print "label", label
					#print "trainhistory", train_ids[row[0]]
					#print "transaction", row
					#print "offers", offers[ train_ids[row[0]][2] ]
					#print

					features['offer_value'] = offers[ history[2] ][4]
					features['offer_quantity'] = offers[ history[2] ][2]
					offervalue = offers[ history[2] ][4]

					features['total_spend'] += float( row[10] )

					if offers[ history[2] ][3] == row[4]:
						features['has_bought_company'] += 1.0
						features['has_bought_company_q'] += float( row[9] )
						features['has_bought_company_a'] += float( row[10] )

						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_company_30'] += 1.0
							features['has_bought_company_q_30'] += float( row[9] )
							features['has_bought_company_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_company_60'] += 1.0
							features['has_bought_company_q_60'] += float( row[9] )
							features['has_bought_company_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_company_90'] += 1.0
							features['has_bought_company_q_90'] += float( row[9] )
							features['has_bought_company_a_90'] += float( row[10] )
						if date_diff_days < 180:
							features['has_bought_company_180'] += 1.0
							features['has_bought_company_q_180'] += float( row[9] )
							features['has_bought_company_a_180'] += float( row[10] )

					if offers[ history[2] ][1] == row[3]:

						features['has_bought_category'] += 1.0
						features['has_bought_category_q'] += float( row[9] )
						features['has_bought_category_a'] += float( row[10] )
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_category_30'] += 1.0
							features['has_bought_category_q_30'] += float( row[9] )
							features['has_bought_category_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_category_60'] += 1.0
							features['has_bought_category_q_60'] += float( row[9] )
							features['has_bought_category_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_category_90'] += 1.0
							features['has_bought_category_q_90'] += float( row[9] )
							features['has_bought_category_a_90'] += float( row[10] )
						if date_diff_days < 180:
							features['has_bought_category_180'] += 1.0
							features['has_bought_category_q_180'] += float( row[9] )
							features['has_bought_category_a_180'] += float( row[10] )
					if offers[ history[2] ][5] == row[5]:
						features['has_bought_brand'] += 1.0
						features['has_bought_brand_q'] += float( row[9] )
						features['has_bought_brand_a'] += float( row[10] )
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_brand_30'] += 1.0
							features['has_bought_brand_q_30'] += float( row[9] )
							features['has_bought_brand_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_brand_60'] += 1.0
							features['has_bought_brand_q_60'] += float( row[9] )
							features['has_bought_brand_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_brand_90'] += 1.0
							features['has_bought_brand_q_90'] += float( row[9] )
							features['has_bought_brand_a_90'] += float( row[10] )
						if date_diff_days < 180:
							features['has_bought_brand_180'] += 1.0
							features['has_bought_brand_q_180'] += float( row[9] )
							features['has_bought_brand_a_180'] += float( row[10] )
				last_id = row[0]
				if e % 100000 == 0:
					print e
#generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test)
loc_preds = "kaggle_shop\\shop.preds.txt"
loc_test = "kaggle_shop\\testHistory.csv"
loc_submission = "kaggle_shop\\kaggle.submission2.csv"

def generate_submission(loc_preds, loc_test, loc_submission):
	preds = {}
	for e, line in enumerate( open(loc_preds) ):
		row = line.strip().split(" ")
		preds[ row[1] ] = row[0]


	with open(loc_submission, "wb") as outfile:
		for e, line in enumerate( open(loc_test) ):
			if e == 0:
				outfile.write( "id,repeatProbability\n" )
			else:
				row = line.strip().split(",")
				if row[0] not in preds:
					outfile.write(row[0]+",0\n")
				else:
					outfile.write(row[0]+","+preds[row[0]]+"\n")
#generate_submission(loc_preds, loc_test, loc_submission)






















In Python to reduce from 20GB to about 1GB (349.655.789 lines to 15.349.956 lines) or "the category subset" as BreakfastPirate calls it:

from datetime import datetime

loc_offers = "kaggle_shop\\offers.csv"
loc_transactions = "kaggle_shop\\transactions.csv"
loc_reduced = "kaggle_shop\\reduced2.csv" # will be created

def reduce_data(loc_offers, loc_transactions, loc_reduced):

  start = datetime.now()
  #get all categories on offer in a dict
  offers = {}
  for e, line in enumerate( open(loc_offers) ):
    offers[ line.split(",")[1] ] = 1
  #open output file
  with open(loc_reduced, "wb") as outfile:
    #go through transactions file and reduce
    reduced = 0
    for e, line in enumerate( open(loc_transactions) ):
      if e == 0:
        outfile.write( line ) #print header
      else:
        #only write when category in offers dict
          if line.split(",")[3] in offers:
            outfile.write( line )
            reduced += 1
      #progress
      if e % 5000000 == 0:
        print e, reduced, datetime.now() - start
  print e, reduced, datetime.now() - start

reduce_data(loc_offers, loc_transactions, loc_reduced)

if you want to reduce the data with company, change:

offers[ line.split(",")[1] ] = 1

to:

offers[ line.split(",")[3] ] = 1

and:

if line.split(",")[3] in offers

to:

if line.split(",")[4] in offers











































