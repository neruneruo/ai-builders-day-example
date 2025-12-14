# AI Builders Day AIエージェントサンプル

## 動作環境
- GNU Make 4.2.1
- Terraform 1.14.0
- uv 0.7.2
- Python 3.12
- lefthook 1.7.14 ※必須ではない

## 準備

### 環境設定する
```bash
make bootstrap
```

### AWSリソース作成

CloudWatch Logs のロググループ以外を作成

```bash
make terraform ARG="apply -var initial_apply=true"
```

Bedrock AgentCore Runtime が自動で作成する CloudWatch Logs のロググループを import

```bash
make terraform ARG="apply"
```

## 実行

```bash
make streamlit-local-run
```

## 後片付け

```bash
make clean
```

※ clean 対象から除外したいファイルがある場合は、Makefile の `CLEAN_EXCLUDES` を修正する
