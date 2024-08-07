# otenkisan
時計＆天気予報＆カレンダーを表示する。  

## 使用するもの
- キオスク化には以下のアプリを使用。  
[Fully Kiosk Browser & Lockdown](https://play.google.com/store/apps/details?id=de.ozerov.fully&hl=ja&gl=US)  

- 天気情報  
天気情報は[天気予報 API](https://weather.tsukumijima.net/)から取得。  

- カレンダー  
[FullCalendar](https://fullcalendar.io/)を使用。


## イメージ
![otenkisan_image](https://user-images.githubusercontent.com/47170845/158050074-c0923f56-7726-4785-b599-bec760af7c78.png)  


## Project setup
`git clone https://github.com/showgayaki/otenkisan.git`  
`cd otenkisan`  

#### .evn.local準備
.env.sampleを.env.localにリネーム。  
- FORECAST_API_URL  
  天気情報を取得したいAPIのURL(.env.sampleに記載されているURLは、東京都のURL)  
- FORECAST_ACQUISITION_MINUTE  
  毎時何分に天気予報APIを叩くか
- SWITCHBOT_API_URL  
  SwichBotのAPI URL
- SWITCHBOT_ACCESS_TOKEN  
  SwichBotのaccess token
- VUE_APP_FETCH_API_MINUTES  
  jsonから、天気情報を何分(00秒)に取得するかの設定。1時間に一回を想定。後述のsystemd timer設定を考慮する必要あり。  
- HOLIDAY_URL  
  祝日情報のURL

### Dockerの場合
#### 初回
`docker compose up -d`  

#### 更新時
`docker compose down && docker compose build --no-cache && docker compose up -d`  

#### systemd timer設定
`sudo vi /lib/systemd/system/otenkisan.service`  
```
[Unit]
Description=otenkisan

[Service]
Type=simple
User=[user name]
ExecStart=/usr/bin/docker exec otenkisan_backend python /var/otenkisan/backend/otenkisan/core.py

[Install]
WantedBy=multi-user.target
```

### timer 
`sudo vi /lib/systemd/system/otenkisan.timer`  
```
[Unit]
Description=backtan-timer

[Timer]
OnCalendar=*:0/5

[Install]
WantedBy=timers.target
```

`sudo systemctl daemon-reload`  
`sudo systemctl enable otenkisan.timer`  
`sudo systemctl start otenkisan.timer`  


### Dockerじゃない場合
#### npm
nodeとかのインストールとか。  
参考：https://qiita.com/seibe/items/36cef7df85fe2cefa3ea  

`sudo apt install -y nodejs npm`  
`sudo npm install n -g`  
`sudo n stable`  
`sudo apt purge -y nodejs npm`  
`exec $SHELL -l`  

`npm install`  


#### python
`python3 -m venv .venv`  
`source .venv/bin/activate`  
`pip install -r requirements.txt`  


#### .evn.local準備
.env.sampleを.env.localにリネーム。  
- TARGET_URL  
  天気情報を取得したいURL(市区町村のページ)  
  ※.env.sampleに記載されているURLは、品川区のURL
- TARGET_ATTRTARGET_ATTR  
  TARGET_URLページの当日の天気情報箇所のclass名(基本変更しない)
- VUE_APP_FETCH_API_MINUTES  
  jsonから、天気情報を何分(00秒)に取得するかの設定。1時間に一回を想定。後述のcron設定を考慮する必要あり。  

#### Compiles and hot-reloads for development
`npm run serve`  

#### Compiles and minifies for production
`npm run build`  

#### nginx設定
`sudo apt install nginx -y`  

`sudo vi /etc/nginx/conf.d/otenkisan.conf`  

以下を記載。  
[path_to]箇所は（ry  
server_name箇所も（ry  

```
server {
    listen 80;
    server_name 192.168.1.12;
    index index.html index.php;

    access_log /var/log/nginx/otenkisan_access.log;
    error_log  /var/log/nginx/otenkisan_error.log;

    location /otenkisan {
        alias [path_to]/otenkisan/dist/;
    }

    location ^~ /otenkisan/json/ {
        alias [path_to]/otenkisan/public/json/;
    }
}
```

設定反映  
`sudo nginx -s reload`　 


#### cron設定
`sudo vi /etc/cron.d/my-cron`  

my-cronは任意の名前でよい。以下を記載して保存。  
```
*/5 * * * * root [path_to]/otenkisan/backend/run.sh >> [path_to]/cron/otenkisan_cron.log 2>&1
```

[path_to]箇所は、環境によって置き換え。  
「>>」以降はログ出力場所なので、どこでもいい。  

上記だと毎時５分に実行。  
[.evn.local準備](#.evn.local準備)で設定した、VUE_APP_FETCH_API_MINUTESの直前に実行されるようにするとよい。  

1. 天気予報 APIから天気情報取得してjsonに保存
2. 保存したjsonから情報取得
の流れ。  
