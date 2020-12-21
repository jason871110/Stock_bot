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

<img src='https://i.imgur.com/QiLXZJq.jpg'>

### 貓咪圖片
