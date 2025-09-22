# セットアップガイド (Windows)

このガイドでは、Windows環境でのAWS Secrets Manager移行プロジェクトの完全なセットアップ手順を説明します。

## 📋 前提条件

### システム要件
- Windows 10/11
- Python 3.12+
- Git
- インターネット接続

### アカウント要件
- GitHubアカウント
- AWSアカウント（IAM権限必要）

## 🛠️ ツールのインストール

### 1. GitHub CLIのインストール

GitHub CLIを使用することで、コマンドラインからリポジトリの作成やGitHub Secretsの管理が可能になります。

#### Windows Package Manager (winget) を使用
```bash
# GitHub CLIをインストール
winget install --id GitHub.cli

# インストール後、新しいターミナルを開くか、パスを更新
export PATH="/c/Program Files/GitHub CLI:$PATH"

# 動作確認
gh --version
```

#### 手動インストール（wingetが利用できない場合）
1. https://cli.github.com/ にアクセス
2. 「Download for Windows」をクリック
3. MSIファイルをダウンロードして実行
4. インストール後、新しいターミナルを開く

### 2. AWS CLIのインストール

```bash
# AWS CLIをインストール
winget install --id Amazon.AWSCLI

# または手動ダウンロード: https://aws.amazon.com/cli/
```

### 3. Pythonの確認
```bash
# Pythonバージョンの確認（3.12以上必要）
python --version

# pipの更新
python -m pip install --upgrade pip
```

## 🔑 認証設定

### GitHub認証
```bash
# GitHub CLIでログイン
gh auth login

# 以下の選択肢を順に選択：
# 1. GitHub.com
# 2. HTTPS
# 3. Yes (Git認証)
# 4. Login with a web browser

# 認証確認
gh auth status
```

### AWS認証
```bash
# AWS CLIの設定
aws configure

# 以下を入力：
# - AWS Access Key ID: [AWSコンソールで取得]
# - AWS Secret Access Key: [AWSコンソールで取得]
# - Default region: ap-northeast-1
# - Default output format: json
```

## 📦 プロジェクトのセットアップ

### 1. リポジトリのクローン
```bash
# プロジェクトをクローン
git clone https://github.com/un-joho-system/test-awssecretmanager.git
cd test-awssecretmanager
```

### 2. Python環境の準備
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# Git Bash:
source venv/Scripts/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 3. 環境変数の設定
```bash
# .envファイルの作成
cp .env.example .env

# .envファイルを編集して適切な値を設定
# 注意: このファイルは機密情報を含むため、Gitにコミットしない
```

## ✅ 動作確認

### ローカル環境での確認
```bash
# アプリケーションの実行
python app.py
```

### AWS接続の確認
```bash
# AWS接続テスト
aws sts get-caller-identity
```

### GitHub接続の確認
```bash
# GitHub接続テスト
gh repo view
```

## 🚨 トラブルシューティング

### GitHub CLI関連
- **コマンドが見つからない**: パスが設定されていない可能性があります。新しいターミナルを開くか、パスを手動で設定してください
- **認証エラー**: `gh auth login` を再実行してください

### AWS CLI関連
- **認証エラー**: AWS認証情報を確認し、`aws configure` を再実行してください
- **権限エラー**: IAMユーザーに適切な権限が付与されているか確認してください

### Python関連
- **モジュールが見つからない**: 仮想環境が有効化されているか、依存関係が正しくインストールされているか確認してください

## 📞 サポート

問題が発生した場合は、プロジェクトのIssueページでお問い合わせください：
https://github.com/un-joho-system/test-awssecretmanager/issues

---

**次のステップ**: [AWS Secrets Manager移行ガイド](migration-guide.md)