# セットアップガイド

このプロジェクトは Windows と macOS の両方でサポートされています。お使いの環境に応じて、適切なガイドを選択してください。

## 🖥️ オペレーティングシステム別ガイド

### Windows
Windows 10/11 ユーザーはこちら：
**[Windows セットアップガイド](setup-guide-windows.md)**

**特徴:**
- Windows Package Manager (winget) を使用
- PowerShell/Command Prompt/Git Bash での作業
- Windows固有のパス設定

### macOS  
macOS ユーザーはこちら：
**[macOS セットアップガイド](setup-guide-macos.md)**

**特徴:**
- Homebrew パッケージマネージャーを使用
- Terminal/Zsh での作業
- macOS固有のセキュリティ設定

## 📋 共通前提条件

両環境で共通して必要なものです：

### アカウント要件
- ✅ **GitHubアカウント** - リポジトリ管理用
- ✅ **AWSアカウント** - Secrets Manager利用用（IAM権限必要）

### 必要なツール
- ✅ **Python 3.12+** - アプリケーション実行用
- ✅ **Git** - バージョン管理用
- ✅ **GitHub CLI** - GitHub操作自動化用
- ✅ **AWS CLI** - AWS操作自動化用

## 🚀 インストール後の共通手順

どちらのOSでも、ツールインストール後は以下の手順で進めます：

1. **認証設定**
   - GitHub CLIでのログイン
   - AWS CLIでの認証設定

2. **プロジェクトセットアップ**  
   - リポジトリのクローン
   - Python仮想環境の作成
   - 依存関係のインストール

3. **動作確認**
   - ローカル環境での実行テスト
   - AWS/GitHub接続確認

## 💡 選択に迷った場合

- **普段Windowsを使用**: → [Windows ガイド](setup-guide-windows.md)
- **普段macを使用**: → [macOS ガイド](setup-guide-macos.md)  
- **両方の環境で作業する**: 両方のガイドを参照してください

## 🔄 次のステップ

セットアップ完了後は、以下のドキュメントに進んでください：

- [AWS Secrets Manager移行ガイド](migration-guide.md)
- [CI/CD自動化セットアップ](automation-setup.md)

## 📞 サポート

セットアップで問題が発生した場合：
- まず該当OS固有のトラブルシューティング章を確認
- 解決しない場合はプロジェクトのIssueでお問い合わせください

---

**⚠️ 重要**: どちらのOSでも、機密情報（`.env`ファイル等）は絶対にGitにコミットしないでください。