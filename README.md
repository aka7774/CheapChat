# CheapChat
Server to run new LLM for transformers with fastapi

# 使途

新しい日本語LLMが出ましたー！　早速Colabで動かしてみましたー！　まではいいけど、ローカルで使うのがめんどくさいよね

AI VTuberに喋らせるためのWebAPIが欲しいし、モデルは起動時にロードしといて、返事はすぐにして欲しい

# 使い方

```bash
git clone https://github.com/aka7774/CheapChat
cd CheapChat
```

## gradio

プロンプトいじるテスト用なので運用では使わない。

```bash
bash venv.sh
```

```bash
venv/bin/python app.py
```

## WebAPI

- 初回起動時にvenv作ってくれる
- 引数にはポート番号を入れる
- 最初から読んで欲しいモデルがあったらmain.pyの末尾に書く

```bash
bash run.sh 50000
```

### /api/chat

POST json

- input 必須 ユーザーの発言
- model_name 任意 hugのリポジトリ
  - あとは config ファイルを読み込んだりPOSTで上書きしたり
  - template, system, prompt
- dtype int4 int8 fp16 BnBで量子化します

エンドポイントは一個だけ

# 制限事項

- WSL2しか対応する気ないけどWindowsでも動くかもしれない
- transformersで簡単に動かせるサンプルコードつきのものしか対応する気は無い
- 複数モデルのロードは必要になったら対応するかも
- CPUには対応しません(正確な回答を長時間待つ使い方は対象外)
- streamingには対応しません(同じGPUで即座に音声合成やるから)
- 非セキュアです(サーバ公開や複数人での同時使用は対象外)

# 競合(上位版)

ollama
- https://github.com/jmorganca/ollama
- Modelfileに設定やプロンプトをまとめて定義する仕組み
- 日本語モデルが登録されてないので、使う前に GGUF に変換が必要
- GGUF に変換できなければ(calm2とか)動作できなさそう

llama.cppのserver
- https://github.com/ggerganov/llama.cpp
- OpenAI API互換
- どうせ GGUF 作って細かく調整して動かすならこっちでいい気がする

