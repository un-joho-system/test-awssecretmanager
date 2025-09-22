# AWS Secrets Manager完全移行ガイド - AI読み込み用統合版

> 🤖 このファイルは Claude Code 等の AI ツールに読み込ませることを前提としています
> 
> **推奨使用法**: このファイル全体をAIに読み込ませてから質問
> 
> **質問例**: 
> - "Step 3で AWS認証エラーが出ました。どうすればいいですか？"
> - "実際のプロジェクトに適用する際の注意点は？"
> - "フォールバック機能の実装方法を詳しく教えて"

## 📋 目次
1. [前提条件と環境準備](#1-前提条件と環境準備)
2. [AWS環境セットアップ](#2-aws環境セットアップ) 
3. [プロジェクト取得と設定](#3-プロジェクト取得と設定)
4. [機密情報の移行](#4-機密情報の移行)
5. [テスト・検証](#5-テスト・検証)
6. [実際のプロジェクトへの適用](#6-実際のプロジェクトへの適用)
7. [トラブルシューティング](#7-トラブルシューティング)
8. [セキュリティベストプラクティス](#8-セキュリティベストプラクティス)

---

## 1. 前提条件と環境準備

### 📋 必要なもの
- **Python 3.12+** - メイン開発言語
- **Git** - バージョン管理
- **GitHub CLI** - GitHub Secrets管理用
- **AWS CLI** - AWS操作用
- **AWSアカウント** - クレジットカード登録済み
- **GitHubアカウント** - リポジトリ管理用

### 🖥️ Windows環境セットアップ
```powershell
# PowerShellを管理者として実行
winget install --id Git.Git
winget install --id GitHub.cli
winget install --id Amazon.AWSCLI
winget install --id Python.Python.3.12

# インストール確認
python --version
git --version
gh --version
aws --version
```

### 🍎 macOS環境セットアップ  
```bash
# Homebrewをインストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 必要ツールをインストール
brew install git gh awscli python@3.12

# インストール確認
python3 --version
git --version
gh --version
aws --version
```

---

## 2. AWS環境セットアップ

### 🔐 2.1 AWS CLI基本設定
```bash
# AWS認証情報を設定
aws configure

# 入力項目:
# AWS Access Key ID: [IAMユーザーのアクセスキー]
# AWS Secret Access Key: [IAMユーザーのシークレットキー] 
# Default region name: ap-northeast-1
# Default output format: json
```

### ✅ 2.2 認証テスト
```bash
# 設定が正しいか確認
aws sts get-caller-identity

# 成功例:
# {
#   "UserId": "AIDACKCEVSQ6C2EXAMPLE",
#   "Account": "123456789012", 
#   "Arn": "arn:aws:iam::123456789012:user/your-username"
# }
```

### 👤 2.3 CI/CD専用IAMユーザー作成
```bash
# CI/CD用IAMユーザーを作成
aws iam create-user --user-name "ci-cd-secrets-automation"

# 必要最小限の権限ポリシーをアタッチ
aws iam attach-user-policy \
  --user-name "ci-cd-secrets-automation" \
  --policy-arn "arn:aws:iam::aws:policy/SecretsManagerReadWrite"

# CI/CD用アクセスキーを作成
aws iam create-access-key --user-name "ci-cd-secrets-automation"

# ⚠️ 重要: 出力されたアクセスキーとシークレットキーを安全に保存
# {
#   "AccessKey": {
#     "AccessKeyId": "AKIA...",
#     "SecretAccessKey": "...",
#     "Status": "Active"
#   }
# }
```

---

## 3. プロジェクト取得と設定

### 📁 3.1 リポジトリセットアップ
```bash
# 1. リポジトリをクローン
git clone [このリポジトリのURL]
cd aws-secrets-migration-guide

# 2. Python仮想環境作成
python -m venv venv

# 3. 仮想環境有効化
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# 4. 依存関係インストール
pip install -r requirements.txt
```

### ⚙️ 3.2 環境変数設定
```bash
# テンプレートファイルをコピー
cp .env.example .env

# .envファイルを編集（例）
# DATABASE_URL=postgresql://testuser:testpass@localhost:5432/testdb
# API_KEY=test_api_key_12345
# SECRET_TOKEN=test_secret_token_67890
# DEBUG_MODE=true
# AWS_ACCESS_KEY_ID=your_access_key
# AWS_SECRET_ACCESS_KEY=your_secret_key
# AWS_REGION=ap-northeast-1
```

---

## 4. 機密情報の移行

### 🔄 4.1 自動分類実行
```bash
# 環境変数を自動分類
python classify_secrets.py

# 出力ファイル:
# - aws-secrets.json: AWS Secrets Manager用の機密情報
# - github-secrets.sh: GitHub Secrets用の認証情報
# - コンソール: 分類結果の表示
```

### ☁️ 4.2 AWS Secrets Manager登録
```bash
# シークレットを作成
aws secretsmanager create-secret \
  --name "your-project-name/app-config" \
  --description "Application configuration secrets" \
  --secret-string file://aws-secrets.json \
  --region ap-northeast-1

# 作成確認
aws secretsmanager describe-secret \
  --secret-id "your-project-name/app-config" \
  --region ap-northeast-1
```

### 🔑 4.3 GitHub Secrets設定
```bash
# GitHub CLIでログイン
gh auth login
# → ブラウザで認証を完了

# GitHub Secretsに認証情報を設定
gh secret set AWS_ACCESS_KEY_ID --body "your_ci_cd_access_key_id"
gh secret set AWS_SECRET_ACCESS_KEY --body "your_ci_cd_secret_access_key"  
gh secret set AWS_REGION --body "ap-northeast-1"

# 設定確認
gh secret list
```

---

## 5. テスト・検証

### 🧪 5.1 ローカル動作テスト
```bash
# 1. 従来版アプリケーションのテスト
echo "=== 従来版テスト ==="
python app.py

# 2. Secrets Manager統合版のテスト
echo "=== Secrets Manager統合版テスト ==="
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"  
export AWS_DEFAULT_REGION="ap-northeast-1"
python app_with_secrets_manager.py

# 3. 自動分類ツールのテスト
echo "=== 自動分類テスト ==="
python classify_secrets.py
```

### 🔍 5.2 AWS接続確認
```bash
# AWS認証確認
aws sts get-caller-identity

# Secrets Manager直接アクセステスト
aws secretsmanager get-secret-value \
  --secret-id "your-project-name/app-config" \
  --region ap-northeast-1 \
  --query SecretString --output text
```

### 🚀 5.3 CI/CDパイプライン確認
```bash
# GitHub Actionsワークフローの実行
git add .
git commit -m "Setup complete - trigger CI/CD pipeline"
git push origin main

# ワークフロー実行状況を確認
gh workflow list
gh run list --limit 5

# 実行ログを確認（最新のワークフロー）
gh run view --log
```

---

## 6. 実際のプロジェクトへの適用

### 📊 6.1 現状分析・計画立案

#### 機密情報の分類
```python
# classify_secrets.py を参考に環境変数を分類
# 分類基準:
# 1. AWS Secrets Manager用: アプリケーション実行時の機密情報
#    - DATABASE_URL, API_KEY, SECRET_TOKEN等
# 2. GitHub Secrets用: CI/CD認証情報
#    - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY等  
# 3. ローカル専用: 開発時のみ使用
#    - DEBUG_MODE, LOCAL_FILE_PATH等
```

### 🛠️ 6.2 コード改修

#### SecretsManager統合クラスの実装
```python
import boto3
import json
import os
from botocore.exceptions import ClientError

class SecretsManager:
    def __init__(self, secret_name, region='ap-northeast-1'):
        self.secret_name = secret_name
        self.region = region
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self):
        """AWS Secrets Managerから機密情報を取得"""
        try:
            response = self.client.get_secret_value(SecretId=self.secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            print(f"Secrets Manager access error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None

class ConfigManager:
    def __init__(self, secret_name=None):
        self.secrets_manager = SecretsManager(secret_name) if secret_name else None
    
    def get_config_value(self, key, default=None):
        """設定値を優先度順で取得: AWS Secrets Manager → 環境変数 → デフォルト値"""
        
        # 1. AWS Secrets Manager
        if self.secrets_manager:
            secrets = self.secrets_manager.get_secret()
            if secrets and key in secrets:
                return secrets[key]
        
        # 2. 環境変数
        env_value = os.environ.get(key)
        if env_value:
            return env_value
        
        # 3. デフォルト値
        return default
```

#### 既存コードの改修例
```python
# Before: 従来の環境変数直接取得
database_url = os.environ.get('DATABASE_URL')
api_key = os.environ.get('API_KEY')

# After: ConfigManager経由での取得
config = ConfigManager('your-project/app-config')
database_url = config.get_config_value('DATABASE_URL')
api_key = config.get_config_value('API_KEY')
```

### 🔄 6.3 段階的移行戦略

#### Phase 1: フォールバック機能実装
- Secrets Manager統合コードを実装
- 環境変数フォールバック機能付き
- テスト環境での動作確認

#### Phase 2: 機密情報移行
- 重要度の低い設定から段階的にSecrets Managerに移行
- 各段階での動作確認とロールバック準備

#### Phase 3: CI/CD統合  
- GitHub Secrets設定
- CI/CDパイプラインでの動作確認

#### Phase 4: 完全移行
- 環境変数依存の段階的削除
- 最終テスト・検証

### ⚙️ 6.4 CI/CD設定
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Set AWS credentials
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        AWS_DEFAULT_REGION: ${{ secrets.AWS_REGION }}
      run: |
        # アプリケーションテスト
        python app_with_secrets_manager.py
```

---

## 7. トラブルシューティング

### ❌ よくあるエラーと解決法

#### 7.1 AWS認証エラー
```
Error: Unable to locate credentials
```
**原因**: AWS認証情報が正しく設定されていない
**解決法**: 
```bash
# 認証情報を再設定
aws configure

# 設定確認
aws sts get-caller-identity

# 環境変数で直接設定（一時的）
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="ap-northeast-1"
```

#### 7.2 Python依存関係エラー
```
ModuleNotFoundError: No module named 'boto3'
```
**解決法**:
```bash
# 仮想環境が有効化されているか確認
which python

# 依存関係を再インストール
pip install -r requirements.txt

# 個別インストール
pip install boto3 python-dotenv
```

#### 7.3 GitHub認証エラー
```
Error: Not logged in
```
**解決法**:
```bash  
# GitHub CLIでログイン
gh auth login

# 認証状況確認
gh auth status

# トークンを手動設定（必要に応じて）
gh auth login --with-token < your_token_file
```

#### 7.4 Secrets Manager アクセス権エラー
```
AccessDenied: User is not authorized to perform: secretsmanager:GetSecretValue
```
**解決法**:
```bash
# 現在のユーザーのポリシー確認
aws iam list-attached-user-policies --user-name your-username

# 必要なポリシーをアタッチ
aws iam attach-user-policy \
  --user-name your-username \
  --policy-arn "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
```

#### 7.5 JSON形式エラー
```
json.JSONDecodeError: Expecting ',' delimiter
```
**原因**: Secrets ManagerのJSON形式が不正
**解決法**:
```bash
# 現在の値を確認
aws secretsmanager get-secret-value \
  --secret-id "your-secret-name" \
  --query SecretString --output text

# 正しいJSON形式で更新
aws secretsmanager update-secret \
  --secret-id "your-secret-name" \
  --secret-string '{"DATABASE_URL":"...","API_KEY":"..."}'
```

### 🔍 診断手順

#### 問題切り分けフローチャート
```
エラー発生
    ↓
AWS認証はOK？
    No → aws configure で設定
    Yes ↓
Python環境はOK？  
    No → pip install -r requirements.txt
    Yes ↓
Secrets Managerアクセス権はOK？
    No → IAMポリシー確認・アタッチ
    Yes ↓
JSON形式は正しい？
    No → JSON形式を修正
    Yes ↓
個別調査が必要
```

---

## 8. セキュリティベストプラクティス

### 🔒 実装時の重要ポイント

#### 8.1 Git管理の除外
```bash
# .gitignore に必須項目を追加
.env
.env.local
.env.production
aws-secrets.json
github-secrets.sh
*.pem
*.key
```

#### 8.2 ログ出力の注意
```python
# ❌ 悪い例: 機密情報をログ出力
logger.info(f"Database URL: {database_url}")

# ✅ 良い例: 機密情報をマスク
logger.info(f"Database URL: {database_url[:10]}***")

# ✅ より良い例: ログ出力しない
logger.info("Database connection established")
```

#### 8.3 エラーハンドリング
```python
def get_secret_safe(secret_name):
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        # ❌ 悪い例: 詳細エラーをログ出力
        # logger.error(f"Secret access failed: {e}")
        
        # ✅ 良い例: 一般的なエラーメッセージ
        logger.error("Failed to access application configuration")
        return None
```

### 🛡️ 運用時のセキュリティ対策

#### 8.4 定期的なアクセスキーローテーション
```bash
# 古いアクセスキーの確認
aws iam list-access-keys --user-name your-username

# 新しいアクセスキー作成
aws iam create-access-key --user-name your-username

# GitHub Secrets更新
gh secret set AWS_ACCESS_KEY_ID --body "new_access_key"
gh secret set AWS_SECRET_ACCESS_KEY --body "new_secret_key"

# 古いアクセスキー削除（動作確認後）
aws iam delete-access-key --user-name your-username --access-key-id "old_key"
```

#### 8.5 最小権限の原則
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:ap-northeast-1:ACCOUNT-ID:secret:your-project/*"
    }
  ]
}
```

#### 8.6 監査ログの活用
```bash
# Secrets Managerアクセスログ確認
aws logs filter-log-events \
  --log-group-name /aws/secretsmanager/your-secret \
  --start-time 1609459200000

# 不審なアクセスの監視設定
# CloudWatch Alarms, AWS Config Rules 等を活用
```

### 📋 セキュリティチェックリスト

運用開始前に以下を確認：

#### 開発環境
- [ ] `.env`ファイルが`.gitignore`に追加済み
- [ ] 機密情報がGit履歴に含まれていない
- [ ] ログ出力で機密情報が漏れていない
- [ ] エラーハンドリングが適切に実装済み

#### AWS環境
- [ ] IAMユーザーが最小権限で設定済み
- [ ] Secrets Managerのアクセス権限が適切
- [ ] 不要なアクセスキーが削除済み
- [ ] リージョンが適切に設定済み

#### CI/CD環境
- [ ] GitHub Secretsが適切に設定済み
- [ ] ワークフローで機密情報が漏れていない  
- [ ] テスト用・本番用の環境分離済み
- [ ] デプロイ権限が適切に制限済み

#### チーム運用
- [ ] チーム全体でセキュリティルール共有済み
- [ ] アクセスキーローテーション計画策定済み
- [ ] インシデント対応手順文書化済み
- [ ] 定期的なセキュリティレビュー計画済み

---

## 🎯 成功指標・完了確認

### ✅ 移行成功の確認指標

以下がすべて達成できれば移行完了：

#### 技術的指標
- [ ] **AWS認証**: `aws sts get-caller-identity` が正常動作
- [ ] **Secrets Manager**: 機密情報が適切に格納・取得可能
- [ ] **アプリケーション**: Secrets Manager版が正常動作
- [ ] **フォールバック**: AWS障害時も環境変数で継続動作
- [ ] **CI/CD**: パイプラインが正常実行・テスト通過
- [ ] **GitHub Secrets**: 認証情報が適切に設定済み

#### セキュリティ指標  
- [ ] **Git管理**: 機密情報が完全にGit管理から除外済み
- [ ] **権限管理**: IAMユーザーが最小権限で設定済み
- [ ] **ログ安全性**: 機密情報がログ出力されない
- [ ] **監査体制**: アクセスログ監視体制構築済み

#### チーム指標
- [ ] **知識共有**: チーム全体で移行内容・手順を理解
- [ ] **運用準備**: 日常運用・トラブル対応手順が整備済み  
- [ ] **改善計画**: 継続的改善・セキュリティ強化計画策定済み

### 🔄 継続的改善ポイント

移行完了後も以下を定期的に実施：

1. **月次**: アクセスキーローテーション
2. **四半期**: セキュリティレビュー・監査
3. **年次**: 権限見直し・アーキテクチャ改善
4. **随時**: 新機能・ベストプラクティスの導入検討

---

**💡 重要な最終メッセージ**: 

この移行は単なる技術的変更ではなく、**セキュリティ文化の向上**です。チーム全体で継続的にセキュリティ意識を高め、安全な開発・運用体制を築いていきましょう。

**🎉 AWS Secrets Managerでより安全で管理しやすい開発環境を実現してください！**