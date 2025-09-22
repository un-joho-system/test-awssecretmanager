#!/usr/bin/env python3
"""
環境変数自動振り分けツール

.envファイルの内容を分析し、以下のように自動振り分けします：
- AWS Secrets Manager: アプリケーション実行時の機密情報
- GitHub Secrets: CI/CD用のAWS認証情報とデプロイ設定
"""

import os
import json
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class SecretClassification:
    """シークレット分類結果"""
    aws_secrets: Dict[str, str]      # AWS Secrets Managerに格納
    github_secrets: Dict[str, str]   # GitHub Secretsに格納
    local_only: Dict[str, str]       # ローカル環境のみ（開発用）

class SecretClassifier:
    """環境変数を自動分類するクラス"""
    
    def __init__(self):
        # AWS Secrets Manager用パターン（アプリケーション実行時の機密情報）
        self.aws_patterns = [
            r'.*_URL$',           # DATABASE_URL, REDIS_URL等
            r'.*_PASSWORD$',      # SMTP_PASSWORD等
            r'.*_SECRET.*',       # JWT_SECRET, SECRET_TOKEN等
            r'API_KEY.*',         # API_KEY, API_KEY_EXTERNAL等
            r'.*_TOKEN$',         # SECRET_TOKEN, AUTH_TOKEN等
            r'.*_CONNECTION.*',   # CONNECTION_STRING等
            r'ENCRYPTION_.*',     # ENCRYPTION_KEY等
            r'PRIVATE_KEY.*',     # PRIVATE_KEY等
        ]
        
        # GitHub Secrets用パターン（CI/CD用認証情報）
        self.github_patterns = [
            r'^AWS_.*',           # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY等
            r'.*_DEPLOY_.*',      # DEPLOY_TOKEN, DEPLOY_KEY等
            r'CI_.*',             # CI_TOKEN等
            r'CD_.*',             # CD_WEBHOOK等
            r'DOCKER_.*',         # DOCKER_USERNAME, DOCKER_PASSWORD等
            r'REGISTRY_.*',       # REGISTRY_TOKEN等
        ]
        
        # ローカル環境のみ（開発・設定用）
        self.local_patterns = [
            r'DEBUG.*',           # DEBUG_MODE等
            r'.*_ENV.*',          # NODE_ENV, FLASK_ENV等
            r'LOG_.*',            # LOG_LEVEL等
            r'PORT$',             # PORT, APP_PORT等
            r'HOST$',             # HOST, DB_HOST等
            r'ENVIRONMENT$',      # ENVIRONMENT等
        ]
    
    def classify_secret(self, key: str, value: str) -> str:
        """
        環境変数を分類する
        
        Returns:
            'aws': AWS Secrets Manager
            'github': GitHub Secrets  
            'local': ローカル環境のみ
        """
        key_upper = key.upper()
        
        # GitHub Secrets パターンチェック（優先度高）
        for pattern in self.github_patterns:
            if re.match(pattern, key_upper):
                return 'github'
        
        # ローカル環境のみパターンチェック
        for pattern in self.local_patterns:
            if re.match(pattern, key_upper):
                return 'local'
        
        # AWS Secrets Manager パターンチェック
        for pattern in self.aws_patterns:
            if re.match(pattern, key_upper):
                return 'aws'
        
        # デフォルトは AWS Secrets Manager（安全側）
        return 'aws'
    
    def parse_env_file(self, env_file_path: str) -> SecretClassification:
        """
        .envファイルを解析して分類する
        """
        aws_secrets = {}
        github_secrets = {}
        local_only = {}
        
        try:
            with open(env_file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # コメント行や空行をスキップ
                    if not line or line.startswith('#'):
                        continue
                    
                    # KEY=VALUE 形式の解析
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # 値が空の場合はスキップ
                        if not value:
                            continue
                        
                        # 分類実行
                        classification = self.classify_secret(key, value)
                        
                        if classification == 'aws':
                            aws_secrets[key] = value
                        elif classification == 'github':
                            github_secrets[key] = value
                        elif classification == 'local':
                            local_only[key] = value
                            
        except FileNotFoundError:
            print(f"❌ .envファイルが見つかりません: {env_file_path}")
            return SecretClassification({}, {}, {})
        except Exception as e:
            print(f"❌ .envファイル解析エラー: {e}")
            return SecretClassification({}, {}, {})
        
        return SecretClassification(aws_secrets, github_secrets, local_only)
    
    def generate_reports(self, classification: SecretClassification) -> None:
        """
        分類結果のレポートを生成・表示
        """
        print("🔍 環境変数自動分類結果")
        print("=" * 60)
        
        print("\n🔐 AWS Secrets Manager (アプリケーション実行時)")
        if classification.aws_secrets:
            for key, value in classification.aws_secrets.items():
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"  {key} = {masked_value}")
        else:
            print("  (該当項目なし)")
        
        print("\n🔑 GitHub Secrets (CI/CD用)")
        if classification.github_secrets:
            for key, value in classification.github_secrets.items():
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"  {key} = {masked_value}")
        else:
            print("  (該当項目なし)")
            
        print("\n💻 ローカル環境のみ (開発設定)")
        if classification.local_only:
            for key, value in classification.local_only.items():
                print(f"  {key} = {value}")
        else:
            print("  (該当項目なし)")
        
        print("\n📊 統計")
        print(f"  AWS Secrets Manager: {len(classification.aws_secrets)} 項目")
        print(f"  GitHub Secrets: {len(classification.github_secrets)} 項目") 
        print(f"  ローカル環境のみ: {len(classification.local_only)} 項目")
    
    def export_aws_secrets_json(self, classification: SecretClassification, output_file: str) -> None:
        """
        AWS Secrets Manager用のJSONファイルを出力
        """
        if not classification.aws_secrets:
            print("⚠️  AWS Secrets Manager用のシークレットがありません")
            return
            
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(classification.aws_secrets, f, indent=2, ensure_ascii=False)
            print(f"✅ AWS Secrets Manager用JSONを出力: {output_file}")
        except Exception as e:
            print(f"❌ JSON出力エラー: {e}")
    
    def export_github_secrets_commands(self, classification: SecretClassification, output_file: str) -> None:
        """
        GitHub Secrets設定用のコマンドを出力
        """
        if not classification.github_secrets:
            print("⚠️  GitHub Secrets用の項目がありません")
            return
            
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("#!/bin/bash\n")
                f.write("# GitHub Secrets 設定用コマンド\n")
                f.write("# 実行前に適切な値に置き換えてください\n\n")
                
                for key, value in classification.github_secrets.items():
                    f.write(f'gh secret set {key} --body "{value}"\n')
                    
                f.write("\n# 設定確認\n")
                f.write("gh secret list\n")
                
            print(f"✅ GitHub Secrets設定コマンドを出力: {output_file}")
        except Exception as e:
            print(f"❌ コマンド出力エラー: {e}")

def main():
    """メイン処理"""
    print("🚀 環境変数自動振り分けツール")
    print("=" * 60)
    
    classifier = SecretClassifier()
    
    # .envファイルを解析
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ {env_file} ファイルが見つかりません")
        return 1
    
    classification = classifier.parse_env_file(env_file)
    
    # 結果表示
    classifier.generate_reports(classification)
    
    # ファイル出力
    classifier.export_aws_secrets_json(classification, "aws-secrets.json")
    classifier.export_github_secrets_commands(classification, "github-secrets.sh")
    
    print("\n🎯 次のステップ:")
    print("1. aws-secrets.json を確認してAWS Secrets Managerに登録")
    print("2. github-secrets.sh を確認してGitHub Secretsに登録") 
    print("3. アプリケーションコードをSecrets Manager対応に更新")
    
    return 0

if __name__ == "__main__":
    exit(main())