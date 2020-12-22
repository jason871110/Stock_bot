# TOC Project 2020
> Linebot實作
> Due date: 2020/12/27

## 創立主旨
現在坊間有許多打著機器學習自動交易、AI大數據股票，等各種不同有關股票結合AI的課程或是各類商用服務。而剛好我對股票有點興趣，且這學期也接觸到了機器學習。所以我想打造一支屬於我的股票交易機器人。


## 基本資訊
**名稱 : stock_bot**

![](https://i.imgur.com/2MEEs7T.gif)

## 安裝
> 基本上直接pip install -r requirements.txt即可完成安裝。

**注意:Ta-Lib在windows安裝應該會出現問題所以可以參考這篇[教學](https://blog.csdn.net/brucewong0516/article/details/79245471)來安裝即可安裝成功。**
## 功能
主要功能會分成以下三種，分別是股票(main feature)、FSM graph獲取、貓咪圖片。下面會依序做介紹。
### 股票
這邊主要會是股票機器學習模型的實際使用，並未實作股價即時報價等股票相關資料的拿取主要考量是目前股票資料收尋相當方便，以及3秒內對TWSE發超過3次requests就會被鎖1~2小時(經實測)。

1. **基礎選單**:進入到stock_bot聊天機器人後輸入stock就會進入到股票模型選單。。會看到主選單內有兩個模型分別是**ML Tw50**和**RL model** 這兩項股票模型，如下圖。

<img src='https://imgur.com/rXHVgme.jpg' width='500'>

2. **模型選取**:在上一步選取了所要的模型後即可進入股票模型的選單，這裡的選單可以讓你查看一些關於模型的資訊，當然也包含了**今日選股**這樣經典的股票機器人功能。

<img src='https://imgur.com/ZchJHVU.jpg' width='500'>

3.**模型詳細資訊**
- **今日選股**:如標題，這邊就是我的模型今天預測出可以買的股票以及價格和停損/利點。


- **介紹**:這邊會簡單以文字的方式介紹我訓練模型的方式和輸入。
- **績效**:短期股票測狀況。

**投資一定有風險，AI投資有賺有賠，使用前應詳閱模型介紹。**

<img src='https://imgur.com/qbhDvlI.jpg' width='1200'>

### FSM

<img src='https://imgur.com/ZKm9ZF2.jpg'>

### 貓咪圖片
這邊主要是想作股票交易壓力都會很大所以實作一個可以回傳許多貓咪圖片和辨識貓狗的舒壓功能。

1.  **基礎選單**:進入到聊天機器人後輸入cat就會進入到貓咪服務選單。會看到主選單內有兩個功能分別是**拿貓咪圖片**及**貓狗辨識器**。

<img src='https://imgur.com/rXHVgme.jpg' width='600'>

2.  **貓咪圖片拿取功能**:這邊是透過串接別人開法好的貓咪restful API來去作貓咪圖片的抓取，基本上使用方法如下圖，點擊**拿一張貓咪圖片**或是**再一張貓咪**的按鈕就可以拿取貓咪的圖片。

<img src='https://imgur.com/iBakNXZ.jpg' width='800'>

3.  **貓狗辨識功能**:這邊是我用[Resnet50](https://keras.io/api/applications/resnet/)去吃Kaggle上[貓狗辨識資料集](https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip) Train 出來的結果，使用的方式如下，進入貓狗辨識器後，按照指示上傳圖片等待模型跑一段時間就會拿到辨識的結果。

<img src='https://imgur.com/I9Xlgw9.jpg' width='800'>

- 當然除了正常辨識之外，壓力大的時候也可以拿來消費朋友，紓壓。

<img src='https://imgur.com/3ypB7M4.jpg' width='200'>

- 模型的部分，這便就簡單展示一下訓練出時accuracy和loss，可以看到其實train一個epoch就會有不錯的表現。以我目前訓練到5個epoch 也不會出現overfitting的問題，只是由於Resnet50不太好訓練所以就沒有在往下增加epoch 去看是否能再增加準確度。

<img src='https://imgur.com/qvfnSgT.jpg' width='800'>



