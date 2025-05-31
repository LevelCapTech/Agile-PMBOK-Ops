# さくらインターネットVPSサーバー初期構築手順

さくらインターネットのVPNサーバーに、[LevelCapTech/Agile-PMBOK-Opsリポジトリ](https://github.com/LevelCapTech/Agile-PMBOK-Ops)を初期展開する手順を解説します。

## 【初期設定手順】

### 1.専用グループとユーザーを作る

```sh
# グループ作成（system グループとして登録）
sudo groupadd -r agile_pmbok_ops
# ユーザー作成（ログイン不可・ホームを /opt/Agile-PMBOK-Ops に固定）
sudo useradd -r -d /opt/Agile-PMBOK-Ops -s /usr/sbin/nologin -g agile_pmbok_ops agile_pmbok
# 既存管理者を作業用に参加させる
sudo usermod -aG agile_pmbok_ops nishiyama
```

### 2.ディレクトリを用意し、オーナー権限を移す

```sh
# ディレクトリを用意する
sudo mkdir -p /opt/Agile-PMBOK-Ops
sudo chown agile_pmbok:agile_pmbok_ops /opt/Agile-PMBOK-Ops
# 以後このディレクトリで作られるファイルは同グループを継承
sudo chmod g+s /opt/Agile-PMBOK-Ops
```

### 3.デプロイ用 SSH 鍵を発行（1 回だけ）

```sh
sudo -u agile_pmbok ssh-keygen -t ed25519 -C "nishiyama@lvcap.jp"  -f /opt/Agile-PMBOK-Ops/.ssh/id_ed25519
sudo cat /opt/Agile-PMBOK-Ops/.ssh/id_ed25519.pub
#sudo pbcopy < /opt/Agile-PMBOK-Ops/.ssh/id_ed25519.pub
```

生成された 公開鍵 (id_ed25519.pub) を GitHub の
「Agile-PMBOK-Ops → Settings → Deploy keys」へ登録 (Read-only で可)。

### 4.初回クローン

```sh
# まだリポジトリでなければ初期化
sudo -u agile_pmbok git -C /opt/Agile-PMBOK-Ops init
# GitHub を origin として登録
sudo -u agile_pmbok git -C /opt/Agile-PMBOK-Ops remote add origin git@github.com:LevelCapTech/Agile-PMBOK-Ops.git
# sudo -u agile_pmbok git -C /opt/Agile-PMBOK-Ops switch -c main --track origin/main
sudo -u agile_pmbok git -C /opt/Agile-PMBOK-Ops fetch --depth 1
# リモートのmainブランチでまずはチェックスト
sudo -u agile_pmbok git -C /opt/Agile-PMBOK-Ops checkout -f origin/main
# mainブランチをローカルに作る場合
sudo -u agile_pmbok git -C /opt/Agile-PMBOK-Ops switch -c main --track origin/main
```

##　【リポジトリ運用手順】

リポジトリを更新する場合は、さくらVPSサーバーにSSHでログイン後下記コマンドでリポジトリをpullしてください。

```sh
sudo -u agile_pmbok git -C /opt/Agile-PMBOK-Ops pull --ff-only
```