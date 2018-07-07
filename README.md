# Heroku Keep-Alive

10分おきに対象のURLにリクエストを送り，フリーのHerokuアプリがスリープするのを防ぎます．  
（AM0:00からAM8:00まではリクエストの送信をスキップします．）  
本アプリはAMとPM用にそれぞれ立ち上げて，交互に起動しあいながら動作することによって550 dyno hours以内に抑えます．

## Herokuの環境変数を設定

```console
$ heroku config:set KEEPALIVE_URL=対象のURL（';'区切りで複数登録可）
$ heroku config:set IS_AM(or IS_PM)=1
$ heroku config:set SELF_API_KEY=自身のAPI Key
$ heroku config:set ANOTHER_API_KEY=もう片方のAPI Key
```

## Clockプロセスの起動

```console
$ heroku ps:scale clock=1
```
