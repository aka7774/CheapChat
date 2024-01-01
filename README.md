# akachat

あかちゃんチャット

# 要件

- 新しいローカルLLM(transformersで動くやつ)をすぐ試したい
- AI VTuberに喋らせるためのWebAPIが欲しい
- playgroundの中から関数を呼び出したい

## 対応環境

CUDA必須です。

- WSL2 Ubuntu 22.04 動作確認済み
- Windows 導入できれば動く
- Linux たぶん動くけど動作未確認

# 導入

```bash
git clone https://github.com/aka7774/akachat
cd akachat
```

# gradio

```bash
bash venv.sh
```

```bash
venv/bin/python app.py
```

## prompt

- プロンプトtxtと設定jsonのペア
- prompt/{name}.txt prompt/{name}.json に save できる
  - save したものを WebAPI から呼び出せる
- instruction は Llama2 や ChatGPT の system と同じ意味
- input はユーザーの入力文字列

### Prompt Options

- Location ローカルLLMかWebサービス(今はOpenAIだけ)を指定する
- model モデル名 Huggingface形式
- dtype Bitsandbytesで量子化する場合int4かint8を指定できる
- template LLM用の書式を記述する {instruction}と{input}を含む
- is_messages いわゆるChatGPT互換の書式 うまく機能してないかも

以下は model.generate() に渡すパラメタ Local専用

- max_new_tokens
- temperature
- top_p
- top_k
- repetition_penalty

## RAG

- FAISS検索機能
- rag_dir を決めて zipをアップロードするとテキストにしてくれる
  - langchain.document_loaders.generic.GenericLoader に対応
- instruction から {rag('dir', 'query')} で呼び出せる

## var

- key-value型の変数機能
- key を決めて value を保存する
- instruction から {var('key')} で呼び出せる

## messages

- log/messages.jsonl に改行区切りの ChatGPT互換の message json を保存する
- instruction から {msg(limit)} で呼び出せる limit は最新からの件数

## settings

- akachat全体の設定
- is_test が ON なら instruction で {test('文字列')} に入れた文字列は有効
- OpenAI API Key はここに入れる

## batch

- LLMの比較用
- prompt/ に保存されているすべてのプロンプトが対象
- 指定した model とスペース区切りの temperature で推論を実行する

# WebAPI

```bash
bash run.sh 50000
```

- 初回起動時にvenv作ってくれる
- 引数にはポート番号を入れる

http://127.0.0.1:50000/docs

# 制限事項

- 複数モデルのロードはVRAM足らんので対応しない
- streamingには対応しません(同じGPUで即座に音声合成やるから)
- 非セキュアです(サーバ公開や複数人での同時使用は対象外)

# 似たようなツール

- text-generation-webui
- llama-cpp-python
- ollama
  - https://github.com/jmorganca/ollama
  - Modelfileに設定やプロンプトをまとめて定義する仕組み
  - 日本語モデルが登録されてないので、使う前に GGUF に変換が必要
  - GGUF に変換できなければ(calm2とか)動作できなさそう
- llama.cppのserver
  - https://github.com/ggerganov/llama.cpp
  - OpenAI API互換
  - どうせ GGUF 作って細かく調整して動かすならこっちでいい気がする
