# AWS Secrets Manager移行テストプロジェクト

このプロジェクトは、従来の `.env` ファイルベースの機密情報管理から **AWS Secrets Manager** への移行をテストするためのサンプルアプリケーションです。

## 🎯 プロジェクトの目的

- ローカル環境の機密情報をAWS Secrets Managerに安全に移行
- GitHub + AWS Secrets Manager + GitHub Secretsによるセキュアな運用体制構築
- 同僚が簡単に再現できる自動化手順書の作成

## 📋 機密情報の分離方針

### 🔒 AWS Secrets Manager
アプリケーション実行時の機密情報
- `DATABASE_URL`: データベース接続文字列
- `API_KEY`: 外部API認証キー
- `SECRET_TOKEN`: アプリケーション認証トークン
- その他アプリケーション固有の機密情報

### 🔑 GitHub Secrets
CI/CDパイプライン用の認証情報
- `AWS_ACCESS_KEY_ID`: AWSアクセスキーID
- `AWS_SECRET_ACCESS_KEY`: AWSシークレットアクセスキー
- `AWS_REGION`: AWS利用リージョン

## 🚀 クイックスタート

### 前提条件
- Python 3.12+
- AWS CLI
- Gitアカウント
- AWSアカウント

### ローカル実行
```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定（初回のみ）
cp .env.example .env
# .envファイルを編集して適切な値を設定

# アプリケーション実行
python app.py
```

## 📁 プロジェクト構造

```
aws-secret-test/
├── app.py                 # メインアプリケーション
├── requirements.txt       # Python依存関係
├── .env                   # 環境変数（Git管理外）
├── .env.example          # 環境変数テンプレート
├── .gitignore            # Git除外ファイル
└── README.md             # このファイル
```

## 🔐 セキュリティ

- `.env` ファイルは `.gitignore` により Git 管理から除外
- 機密情報は AWS Secrets Manager で暗号化管理
- CI/CD認証情報は GitHub Secrets で管理

## 📖 ドキュメント

詳細なセットアップと移行手順は以下のドキュメントを参照：
- [セットアップガイド](docs/setup-guide.md) - ツールのインストールと初期設定
- [AWS Secrets Manager移行ガイド](docs/migration-guide.md) - 機密情報の移行手順
- [自動化セットアップ手順](docs/automation-setup.md) - CI/CDパイプラインの構築

## 🤝 貢献

プロジェクトへの貢献を歓迎します。Pull Requestを送信する前に、以下を確認してください：
- コードが適切にテストされている
- 機密情報がコミットに含まれていない
- ドキュメントが更新されている

## 📞 サポート

質問やサポートが必要な場合は、Issueを作成してください。

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

---

**⚠️ 重要**: このプロジェクトはテスト・学習目的です。実運用環境では、適切なセキュリティ審査を実施してください。