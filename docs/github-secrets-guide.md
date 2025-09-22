# GitHub Secrets設定ガイド

このガイドでは、CI/CD用のAWS認証情報をGitHub Secretsに安全に格納し、GitHub Actionsで使用する方法を説明します。

## 🔑 GitHub Secretsとは

GitHub Secretsは、リポジトリに機密情報を安全に格納し、GitHub Actionsワークフローで使用できる機能です。

### 🛡️ セキュリティの特徴
- **暗号化**: すべてのシークレットは暗号化されて格納
- **アクセス制御**: リポジトリのコラボレーター権限が必要
- **マスキング**: ログ出力時に自動的にマスクされる
- **監査ログ**: アクセス履歴が記録される

## 📋 設定手順

### 1. 自動振り分けによる分類

まず、環境変数を自動分類します：

```bash
# 自動振り分けツールを実行
python scripts/classify_secrets.py
```

これにより以下が生成されます：
- `aws-secrets.json` - AWS Secrets Manager用
- `github-secrets.sh` - GitHub Secrets設定用コマンド

### 2. GitHub CLI での設定

GitHub CLIを使用してシークレットを設定：

```bash
# AWSリージョンを設定
gh secret set AWS_REGION --body "ap-northeast-1"

# AWS認証情報を設定（実際の値に置き換えてください）
gh secret set AWS_ACCESS_KEY_ID --body "your_actual_access_key_id"
gh secret set AWS_SECRET_ACCESS_KEY --body "your_actual_secret_access_key"

# 設定確認
gh secret list
```

### 3. Web UIでの設定（代替方法）

1. GitHubリポジトリページへ移動
2. **Settings** タブをクリック
3. サイドバーで **Secrets and variables** → **Actions** を選択
4. **New repository secret** をクリック
5. Name と Secret を入力して **Add secret**

## 🔐 推奨されるAWS認証情報の管理

### CI/CD専用IAMユーザーの作成

実運用では、CI/CD専用のIAMユーザーを作成することを強く推奨します：

```bash
# AWS CLI でIAMユーザーを作成
aws iam create-user --user-name "ci-cd-test-awssecretmanager"

# 必要最小限の権限ポリシーをアタッチ
aws iam attach-user-policy \
  --user-name "ci-cd-test-awssecretmanager" \
  --policy-arn "arn:aws:iam::aws:policy/SecretsManagerReadWrite"

# アクセスキーを作成
aws iam create-access-key --user-name "ci-cd-test-awssecretmanager"
```

### 必要な権限

CI/CDワークフローに必要な最小権限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:*:*:secret:test-awssecretmanager/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🚀 GitHub Actionsでの使用

GitHub Actionsワークフローでシークレットを使用する例：

```yaml
name: 'AWS Secrets Manager Test Pipeline'

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: 'Configure AWS Credentials'
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ secrets.AWS_REGION }}
    
    - name: 'Test Secrets Manager Access'
      run: |
        aws secretsmanager get-secret-value \
          --secret-id "test-awssecretmanager/app-config"
```

## 📊 設定されるシークレット一覧

| シークレット名 | 説明 | 使用箇所 |
|---|---|---|
| `AWS_ACCESS_KEY_ID` | AWSアクセスキーID | AWS認証 |
| `AWS_SECRET_ACCESS_KEY` | AWSシークレットアクセスキー | AWS認証 |
| `AWS_REGION` | AWSリージョン | AWS操作 |

## ✅ 設定確認方法

### 1. GitHub CLI での確認
```bash
# シークレット一覧表示
gh secret list

# 特定のシークレットの詳細（値は表示されません）
gh secret view AWS_REGION
```

### 2. ワークフロー実行での確認

GitHub Actionsワークフローを実行すると、以下が確認できます：
- AWS認証の成功/失敗
- Secrets Managerへのアクセス結果
- 環境変数の正常な設定

### 3. テスト実行
```bash
# ローカルでワークフローをテスト（act使用時）
act -s AWS_ACCESS_KEY_ID=your_key \
    -s AWS_SECRET_ACCESS_KEY=your_secret \
    -s AWS_REGION=ap-northeast-1
```

## 🚨 セキュリティのベストプラクティス

### ❌ やってはいけないこと
- 実際の認証情報をコードにハードコーディング
- .envファイルをGitにコミット
- プライベートキーをプレーンテキストで保存
- 過度に広範囲な権限を付与

### ✅ 推奨事項
- 必要最小限の権限原則を適用
- 定期的な認証情報のローテーション
- アクセスログの監視
- 複数環境での分離（開発・本番）

## 🔄 ローテーション手順

定期的にシークレットを更新：

```bash
# 新しいアクセスキーを作成
aws iam create-access-key --user-name "ci-cd-test-awssecretmanager"

# GitHub Secretsを更新
gh secret set AWS_ACCESS_KEY_ID --body "new_access_key_id"
gh secret set AWS_SECRET_ACCESS_KEY --body "new_secret_access_key"

# 古いアクセスキーを削除
aws iam delete-access-key --user-name "ci-cd-test-awssecretmanager" --access-key-id "old_access_key_id"
```

## 📞 トラブルシューティング

### よくある問題と解決方法

**問題**: AWS認証エラー
```
Error: The security token included in the request is invalid
```

**解決方法**:
1. シークレットの値を確認
2. IAMユーザーの権限を確認
3. リージョン設定を確認

**問題**: Secrets Managerアクセスエラー
```
AccessDeniedException: User is not authorized to perform secretsmanager:GetSecretValue
```

**解決方法**:
1. IAMポリシーを確認
2. シークレットのリソース名を確認
3. リージョンの一致を確認

## 📖 関連ドキュメント

- [GitHub Secrets公式ドキュメント](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [AWS IAMベストプラクティス](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Secrets Managerユーザーガイド](https://docs.aws.amazon.com/secretsmanager/latest/userguide/)

---

**⚠️ 重要**: このガイドのサンプル認証情報は例であり、実運用では絶対に使用しないでください。