# セットアップガイド (macOS)

このガイドでは、macOS環境でのAWS Secrets Manager移行プロジェクトの完全なセットアップ手順を説明します。

## 📋 前提条件

### システム要件
- macOS 10.15 (Catalina) 以降
- Python 3.12+
- Git
- インターネット接続

### アカウント要件
- GitHubアカウント
- AWSアカウント（IAM権限必要）

## 🛠️ ツールのインストール

### 1. Homebrewのインストール（未インストールの場合）

まず、macOSのパッケージマネージャーであるHomebrewをインストールします：

```bash
# Homebrewをインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# パスを追加（M1/M2 Macの場合）
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# パスを追加（Intel Macの場合）
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile

# 動作確認
brew --version
```

### 2. GitHub CLIのインストール

GitHub CLIを使用することで、コマンドラインからリポジトリの作成やGitHub Secretsの管理が可能になります。

#### Homebrewを使用（推奨）
```bash
# GitHub CLIをインストール
brew install gh

# 動作確認
gh --version
```

#### 手動インストール（Homebrewが利用できない場合）
1. https://cli.github.com/ にアクセス
2. 「Download for macOS」をクリック
3. `.pkg` ファイルをダウンロードして実行
4. インストール後、新しいターミナルを開く

### 3. AWS CLIのインストール

```bash
# Homebrewを使用
brew install awscli

# または手動インストール用のダウンローダー
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# 動作確認
aws --version
```

### 4. Pythonの確認・インストール

```bash
# Pythonバージョンの確認（3.12以上必要）
python3 --version

# Python 3.12のインストール（必要に応じて）
brew install python@3.12

# pipの更新
python3 -m pip install --upgrade pip
```

### 5. Gitの確認・インストール

```bash
# Gitバージョンの確認
git --version

# Gitのインストール（必要に応じて）
brew install git
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

# 設定確認
aws sts get-caller-identity
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
python3 -m venv venv

# 仮想環境の有効化
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 3. 環境変数の設定
```bash
# .envファイルの作成
cp .env.example .env

# .envファイルを編集して適切な値を設定
nano .env
# または
vim .env
# または
code .env  # VS Code使用時

# 注意: このファイルは機密情報を含むため、Gitにコミットしない
```

## ✅ 動作確認

### ローカル環境での確認
```bash
# 仮想環境が有効化されていることを確認
which python  # venv/bin/python が表示されることを確認

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

### Homebrew関連
- **コマンドが見つからない**: パスが設定されていない可能性があります。ターミナルを再起動するか、適切なパスを設定してください
- **権限エラー**: `sudo` コマンドが必要な場合があります

### GitHub CLI関連
- **コマンドが見つからない**: Homebrewのパスが設定されているか確認してください
- **認証エラー**: `gh auth login` を再実行してください

### AWS CLI関連
- **認証エラー**: AWS認証情報を確認し、`aws configure` を再実行してください
- **権限エラー**: IAMユーザーに適切な権限が付与されているか確認してください

### Python関連
- **モジュールが見つからない**: 仮想環境が有効化されているか、依存関係が正しくインストールされているか確認してください
- **Pythonバージョンエラー**: `python3` コマンドを使用してください（macOSではデフォルトで `python` はPython 2系を指す場合があります）

### macOS固有の問題
- **Xcode Command Line Tools**: Gitやコンパイラが必要な場合は `xcode-select --install` でインストールしてください
- **セキュリティ警告**: 「開発元が未確認」の警告が出た場合は、システム環境設定 > セキュリティとプライバシーで許可してください

## 💡 macOS固有のヒント

### シェル設定
```bash
# 使用中のシェルを確認
echo $SHELL

# Zshの場合（macOS Catalina以降のデフォルト）
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Bashの場合
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

### 環境変数の永続化
```bash
# .zshrcまたは.bash_profileに追加
export AWS_DEFAULT_REGION=ap-northeast-1
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 📞 サポート

問題が発生した場合は、プロジェクトのIssueページでお問い合わせください：
https://github.com/un-joho-system/test-awssecretmanager/issues

---

**次のステップ**: [AWS Secrets Manager移行ガイド](migration-guide.md)