# 🚀 AWS Secrets Manager移行 - クイックスタート

## 📖 学習の進め方

### 🎯 **このリポジトリの使い方**
1. **5分理解**: このファイルを読む
2. **30分学習**: [AI-FRIENDLY-GUIDE.md](./AI-FRIENDLY-GUIDE.md) をClaude等に読み込ませて質問
3. **1-2時間実践**: 実際にコードを動かしてテスト
4. **実プロジェクト適用**: 理解できたら実際のプロジェクトに適用

## ⚡ 5分で理解する移行フロー

```bash
# 1. このリポジトリをクローン
git clone [このリポジトリURL]
cd aws-secrets-migration-guide

# 2. 環境構築
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. 設定ファイル作成
cp .env.example .env
# .envファイルを適切な値で編集

# 4. サンプル動作確認
python app.py  # 従来版
python app_with_secrets_manager.py  # 移行版

# 5. 自動分類ツール体験
python classify_secrets.py
```

## 🎪 体験デモ - ファイルの役割

| ファイル | 説明 | 学習ポイント |
|---------|------|-------------|
| `app.py` | 従来の.env方式アプリ | 現在の実装パターン |
| `app_with_secrets_manager.py` | Secrets Manager統合版 | 移行後の実装パターン |
| `classify_secrets.py` | 自動振り分けツール | 機密情報の安全な分離方法 |

## 🎯 移行で解決される課題

### ❌ **Before（従来の問題）**
- 機密情報が`.env`ファイルに平文で保存
- チーム間での機密情報共有が煩雑
- 本番/開発環境での設定管理が複雑
- 機密情報の誤コミットリスク

### ✅ **After（移行後の利点）**
- 機密情報はAWSで暗号化管理
- IAMによる適切なアクセス制御
- 環境別の設定が一元管理
- Git履歴から機密情報を完全排除

## 🤖 AIツールでの学習法

**推奨方法**: [AI-FRIENDLY-GUIDE.md](./AI-FRIENDLY-GUIDE.md) をClaude Code/ChatGPT等に読み込ませる

**質問例**:
```
"AWS認証でエラーが出ました。解決方法を教えて"
"実際のプロジェクトに適用する手順は？"
"セキュリティ面で注意すべき点は？"
"フォールバック機能の仕組みを説明して"
```

## 🔒 重要なセキュリティ事項

- ⚠️ **このリポジトリは学習専用** - 実際の機密情報は入れない
- ⚠️ **AWS認証情報の適切な管理** - アクセスキーの定期ローテーション
- ⚠️ **最小権限の原則** - 必要最小限のIAMポリシー設定
- ⚠️ **実運用前のセキュリティレビュー** - チームでの確認必須

## 🆘 困ったときのサポート

1. **まずは自己解決を試す**: エラーメッセージをAIツールに相談
2. **ドキュメント確認**: AI-FRIENDLY-GUIDE.md で詳細手順確認
3. **質問・相談**: GitHubのIssuesで質問投稿

## ✅ 学習完了チェック

学習完了の目安として以下を確認：

- [ ] AWS Secrets Managerの基本概念を理解
- [ ] 機密情報の分類方法を理解（AWS vs GitHub vs ローカル）
- [ ] フォールバック機能の重要性を理解
- [ ] 実際のプロジェクトへの適用イメージができる
- [ ] セキュリティリスクと対策を理解

---

**🎉 次は AI-FRIENDLY-GUIDE.md でより詳しく学習しましょう！**