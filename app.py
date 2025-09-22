#!/usr/bin/env python3
"""
AWS Secrets Manager移行テスト用のサンプルアプリケーション
環境変数から設定値を読み込み、データベース接続とAPI呼び出しをシミュレートする
"""
import os
import json
from dotenv import load_dotenv
from typing import Optional

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

class Application:
    """メインアプリケーションクラス"""
    
    def __init__(self):
        # 環境変数の読み込み
        self.database_url = self._get_env_var("DATABASE_URL")
        self.api_key = self._get_env_var("API_KEY")
        self.secret_token = self._get_env_var("SECRET_TOKEN")
        self.debug_mode = self._get_env_var("DEBUG_MODE", "false").lower() == "true"
        
        # コンポーネントの初期化
        self.db = DatabaseConnection(self.database_url)
        self.api_client = APIClient(self.api_key, self.secret_token)
    
    def _get_env_var(self, key: str, default: Optional[str] = None) -> str:
        """環境変数を取得（デフォルト値対応）"""
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"必須環境変数 '{key}' が設定されていません")
        return value
    
    def startup(self):
        """アプリケーション開始処理"""
        print("🚀 アプリケーション開始")
        print(f"🔧 デバッグモード: {'ON' if self.debug_mode else 'OFF'}")
        
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
        print(f"  DATABASE_URL: {self.database_url[:20]}..." if len(self.database_url) > 20 else f"  DATABASE_URL: {self.database_url}")
        print(f"  API_KEY: {self.api_key[:8]}...")
        print(f"  SECRET_TOKEN: {self.secret_token[:8]}...")
        print(f"  DEBUG_MODE: {self.debug_mode}")

def main():
    """メイン関数"""
    print("=" * 60)
    print("🔐 AWS Secrets Manager 移行テスト アプリケーション")
    print("=" * 60)
    
    try:
        # .envファイルから環境変数を読み込み
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