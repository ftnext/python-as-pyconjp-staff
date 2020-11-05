# Knowledge base helper script

PyCon JP 2020 ナレッジベースを可能な限り自動で作るためのスクリプト。

## 実現したいこと

JIRAの情報をコマンドラインで取得し、コピー&ペーストでナレッジベースを作成できる。  
※複数人が関わった作業や長期間かかる作業にJIRAが使われる傾向があった。  
このことから、JIRAの情報はナレッジベースとして引き継ぐ対象と重なると考えている。

## 前提

- Python 3系の環境がある (開発はPython 3.8.1)
- PyCon JPのスタッフのJIRAにアカウントを持っていて、ログインできる
- JIRAのアカウント（＝Atlassianアカウント）でAPIトークンを作成済みである
  - APIトークン作成手順：https://confluence.atlassian.com/cloud/api-tokens-938839638.html

## 使い方

### 環境構築

```
git clone https://github.com/ftnext/python-as-pyconjp-staff.git
cd python-as-pyconjp-staff/knowledge_base_helper

# お気に入りのツールで環境を分離してください（venv, poetry, pipenv, etc.）

pip install -r requirements.txt

export JIRA_EMAIL=... JIRA_API_TOKEN=...
```

### コマンド

詳しく知りたい場合は `-h` オプションを追加して、ヘルプメッセージを見てください。

```
# Epicの一覧を表示
python main.py list_epics コンポーネント名

# Epicに紐づくIssueを一覧で表示
python main.py list_epic_subissues コンポーネント名
```
