#!/bin/bash
# GitHub Secrets 設定用コマンド
# 実行前に適切な値に置き換えてください

gh secret set AWS_ACCESS_KEY_ID --body "AKIA1234567890EXAMPLE"
gh secret set AWS_SECRET_ACCESS_KEY --body "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
gh secret set AWS_REGION --body "ap-northeast-1"

# 設定確認
gh secret list
