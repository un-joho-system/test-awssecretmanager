#!/usr/bin/env python3
"""
AWS Secrets Manager移行対応版アプリケーション
環境変数とAWS Secrets Managerから設定値を読み込み、データベース接続とAPI呼び出しをシミュレートする
"""
import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from typing import Optional, Dict

class SecretsManager:
    """AWS Secrets Manager統合クラス"""
    
    def __init__(self, region_name: str = 'ap-northeast-1'):
        """
        Secrets Manager クライアントを初期化
        
        Args:
            region_name: AWSリージョン
        """
        try:
            self.client = boto3.client('secretsmanager', region_name=region_name)
            self.region = region_name
        except Exception as e:
            print(f"⚠️  AWS Secrets Manager接続エラー: {e}")
            self.client = None
    
    def get_secret(self, secret_name: str) -> Optional[Dict[str, str]]:
        """
        シークレットを取得してJSONとして返す
        
        Args:
            secret_name: シークレット名
            
        Returns:
            シークレット内容（辞書）またはNone
        """
        if not self.client:
            print(f"⚠️  Secrets Managerクライアントが利用できません")
            return None
            
        try:
            print(f"🔐 Secrets Manager からシークレットを取得中: {secret_name}")
            response = self.client.get_secret_value(SecretId=secret_name)
            
            # シークレット文字列をJSONとしてパース
            secret_string = response['SecretString']
            secret_dict = json.loads(secret_string)
            
            print(f"✅ シークレット取得成功: {len(secret_dict)} 項目")
            return secret_dict
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                print(f"⚠️  シークレットが見つかりません: {secret_name}")
            elif error_code == 'InvalidRequestException':
                print(f"⚠️  無効なリクエスト: {secret_name}")
            elif error_code == 'InvalidParameterException':
                print(f"⚠️  無効なパラメータ: {secret_name}")
            else:
                print(f"❌ Secrets Manager エラー: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析エラー: {e}")
            return None
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
            return None

class DatabaseConnection:
    """データベース接続クラス"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connected = False
    
    def connect(self) -> bool:
        """データベース接続をシミュレート"""
        print(f"📊 データベースに接続中... {self.database_url}")
        # 実際のアプリでは本物のDB接続処理
        self.connected = True
        print("✅ データベース接続成功")
        return True
    
    def execute_query(self, query: str) -> dict:
        """クエリ実行をシミュレート"""
        if not self.connected:
            raise Exception("データベースに接続されていません")
        
        print(f"🔍 クエリ実行: {query}")
        # サンプルレスポンス
        return {"status": "success", "rows": 5, "query": query}

class APIClient:
    """外部API接続クラス"""
    
    def __init__(self, api_key: str, secret_token: str):
        self.api_key = api_key
        self.secret_token = secret_token
    
    def authenticate(self) -> bool:
        """API認証をシミュレート"""
        print(f"🔐 API認証中... (Key: {self.api_key[:8]}...)")
        # 実際のアプリでは本物のAPI認証処理
        print("✅ API認証成功")
        return True
    
    def fetch_user_data(self, user_id: str) -> dict:
        """ユーザーデータ取得をシミュレート"""
        print(f"👤 ユーザーデータ取得: {user_id}")
        # サンプルレスポンス
        return {
            "user_id": user_id,
            "name": "テストユーザー",
            "email": "test@example.com",
            "status": "active"
        }

class ConfigManager:
    """設定管理統合クラス"""
    
    def __init__(self):
        """設定管理システムを初期化"""
        self.secrets_manager = SecretsManager()
        self.config = {}
        self._load_configuration()
    
    def _load_configuration(self):
        """設定を複数のソースから読み込み"""
        print("⚙️  設定読み込み開始...")
        
        # 1. 環境変数から読み込み（優先度：低）
        print("📁 環境変数から設定を読み込み中...")
        env_config = {
            'DATABASE_URL': os.getenv('DATABASE_URL'),
            'API_KEY': os.getenv('API_KEY'),
            'SECRET_TOKEN': os.getenv('SECRET_TOKEN'),
            'DEBUG_MODE': os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        }
        
        # 2. AWS Secrets Manager から読み込み（優先度：高）
        secret_name = os.getenv('AWS_SECRET_NAME', 'test-awssecretmanager/app-config')
        aws_secrets = self.secrets_manager.get_secret(secret_name)
        
        # 3. 設定を統合（AWS Secrets Managerが優先）
        self.config = env_config.copy()
        if aws_secrets:
            print("🔐 AWS Secrets Manager の設定で上書きしています...")
            self.config.update(aws_secrets)
        else:
            print("⚠️  AWS Secrets Manager からの読み込みに失敗、環境変数を使用します")
        
        # 4. 必須項目の確認
        required_keys = ['DATABASE_URL', 'API_KEY', 'SECRET_TOKEN']
        missing_keys = [key for key in required_keys if not self.config.get(key)]
        
        if missing_keys:
            raise ValueError(f"必須設定が不足: {', '.join(missing_keys)}")
        
        print("✅ 設定読み込み完了")
    
    def get(self, key: str, default=None):
        """設定値を取得"""
        return self.config.get(key, default)
    
    def show_config_source(self):
        """設定ソースの情報を表示"""
        print("\n📊 設定ソース情報:")
        if self.secrets_manager.client:
            print("  🔐 AWS Secrets Manager: 利用可能")
        else:
            print("  ❌ AWS Secrets Manager: 利用不可（環境変数を使用）")
        
        for key in ['DATABASE_URL', 'API_KEY', 'SECRET_TOKEN']:
            if key in self.config and self.config[key]:
                source = "🔐 AWS Secrets Manager" if self.secrets_manager.client else "📁 環境変数"
                masked_value = self.config[key][:10] + "..." if len(self.config[key]) > 10 else "***"
                print(f"  {key}: {masked_value} ({source})")

class Application:
    """メインアプリケーションクラス"""
    
    def __init__(self):
        # 設定管理システムの初期化
        self.config_manager = ConfigManager()
        
        # 設定値の取得
        database_url = self.config_manager.get('DATABASE_URL')
        api_key = self.config_manager.get('API_KEY')
        secret_token = self.config_manager.get('SECRET_TOKEN')
        self.debug_mode = self.config_manager.get('DEBUG_MODE', False)
        
        # コンポーネントの初期化
        self.db = DatabaseConnection(database_url)
        self.api_client = APIClient(api_key, secret_token)
    
    def startup(self):
        """アプリケーション開始処理"""
        print("🚀 アプリケーション開始")
        print(f"🔧 デバッグモード: {'ON' if self.debug_mode else 'OFF'}")
        
        # 設定ソース情報表示
        self.config_manager.show_config_source()
        
        # データベース接続
        self.db.connect()
        
        # API認証
        self.api_client.authenticate()
        
        print("✨ 初期化完了")
    
    def run_sample_operations(self):
        """サンプル処理実行"""
        print("\n📋 サンプル処理を実行中...")
        
        try:
            # データベース操作
            query_result = self.db.execute_query("SELECT * FROM users LIMIT 5")
            if self.debug_mode:
                print(f"📊 クエリ結果: {json.dumps(query_result, indent=2, ensure_ascii=False)}")
            
            # API呼び出し
            user_data = self.api_client.fetch_user_data("user123")
            if self.debug_mode:
                print(f"👤 ユーザーデータ: {json.dumps(user_data, indent=2, ensure_ascii=False)}")
            
            print("✅ 全処理完了")
            
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            raise
    
    def show_config(self):
        """現在の設定を表示（機密情報はマスク）"""
        print("\n⚙️  現在の設定:")
        
        database_url = self.config_manager.get('DATABASE_URL')
        api_key = self.config_manager.get('API_KEY')
        secret_token = self.config_manager.get('SECRET_TOKEN')
        
        if database_url and len(database_url) > 20:
            print(f"  DATABASE_URL: {database_url[:20]}...")
        else:
            print(f"  DATABASE_URL: {database_url}")
            
        if api_key:
            print(f"  API_KEY: {api_key[:8]}...")
        if secret_token:
            print(f"  SECRET_TOKEN: {secret_token[:8]}...")
            
        print(f"  DEBUG_MODE: {self.debug_mode}")

def main():
    """メイン関数"""
    print("=" * 60)
    print("🔐 AWS Secrets Manager 統合アプリケーション")
    print("=" * 60)
    
    try:
        # .envファイルから環境変数を読み込み（フォールバック用）
        load_dotenv()
        
        # アプリケーション実行
        app = Application()
        app.show_config()
        app.startup()
        app.run_sample_operations()
        
        print("\n🎉 アプリケーション正常終了")
        
    except Exception as e:
        print(f"\n💥 アプリケーション実行エラー: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())