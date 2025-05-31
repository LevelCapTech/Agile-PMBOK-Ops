# 本番環境Python実行環境整備

さくらインターネットのVPNサーバーに、Python3の実行環境を整備する手順を解説します。

## ■ pip環境の整備

### 1. root（または sudo 権限）で pip をインストールする

まずはホスト側（root または sudo 権限のあるユーザー）で以下を実行してください。Debian/Ubuntu 系であれば、python3-pip をインストールすると Python3 用の pip コマンドが使えるようになります。

```sh
# pipが使えるか確認
which pip3
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3.12-venv
```

これで、システム全体に pip3（および /usr/bin/pip3） がインストールされます。

### 2. agile_pmbok ユーザーで pip3 を使う

パッケージがインストールできたら、再度 agile_pmbok ユーザーのシェルを開き、pip3 が使えるか確認します。

```sh
sudo -u agile_pmbok /bin/bash
which pip3
# → /usr/bin/pip3 などが返ってくるはずです
pip3 --version
# → pip のバージョンが返ってくれば OK
```

もし pip3 で問題なくバージョンが表示されれば、requirements.txt を指定してインストールが可能です。

```sh
cd /opt/Agile-PMBOK-Ops
pip3 install -r requirements.txt
```

※ もし “コマンドが見つかりません” と出る場合は、システム側でのインストールが正しく行われていない可能性があります。再度 sudo apt install python3-pip を実行してください。

## ■ python仮想環境の整備

### 1. プロジェクト直下に仮想環境（venv）を作ってインストールする

/opt/Agile-PMBOK-Ops 下に venv フォルダを作り、その中に Python 仮想環境を構築します。
（この例では /opt/Agile-PMBOK-Ops/venv に作成）

```sh
# agile_pmbok ユーザー権限で仮想環境を作成
sudo -u agile_pmbok python3 -m venv /opt/Agile-PMBOK-Ops/venv
```

* もし /opt/Agile-PMBOK-Ops の下に書き込み権限がない場合は、先にオーナーを変えるか（例：sudo chown -R agile_pmbok:agile_pmbok_ops /opt/Agile-PMBOK-Ops）、root で venv を作成し、その後オーナーを agile_pmbok に変更してください。

### 2.	仮想環境をアクティベートして依存をインストールする

```sh
sudo -u agile_pmbok /bin/bash << 'EOF'
cd /opt/Agile-PMBOK-Ops
source venv/bin/activate
pip install -r requirements.txt
deactivate
EOF
```

### 3.	スクリプトを venv の Python で実行する

```sh
sudo -u agile_pmbok /opt/Agile-PMBOK-Ops/venv/bin/python /opt/Agile-PMBOK-Ops/app/slackapi/slack_presence_status.py
```