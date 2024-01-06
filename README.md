# akachat

あかちゃんチャット

# 要件

- 新しいローカルLLM(transformersで動くやつ)をすぐ試したい
- デジタルヒューマンに喋らせるためのWebAPIが欲しい
- playgroundの中から関数を呼び出したい

## 対応環境

CUDA必須です。
一通り動作確認していますが、今後の動作確認を保証するものではありません。

- WSL2 Ubuntu 22.04
- Windows 11
- Linux Ubuntu 22.04

# 導入

```bash
git clone https://github.com/aka7774/akachat
cd akachat
```

## Linux

```bash
bash venv.sh
```

## Windows

setup_windows.bat を実行

# 用語の定義

LLMごとに微妙に定義が違うのだけど、akachatでは次のように整理しています。

- prompt instruction と options のセット
- instruction LLMに指示するためのテキスト
  - Llama2系では<<SYS>>タグの中身
  - それ以外では ###指示: の中身とか
  - ChatGPTでは "role": "system" な content
- options model.generate() に入れるパラメタとその他の設定項目
- template LLMが求めるinstructionとinputを含む書式
- input ユーザーの入力文字列
- /api/llm/* promptを実行するエンドポイント
- /api/llmの引数dir promptのname

# gradio

```bash
venv/bin/python app.py
```

あるいは

```bash
GRADIO_SERVER_NAME="0.0.0.0" GRADIO_SERVER_PORT=50001 venv/bin/python app.py
```

## prompt

- 指示txt(instruction)と設定json(options)のペア
- prompt/{name}.txt prompt/{name}.json に save できる
  - save したものを WebAPI から呼び出せる
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

## instruction

{関数名(引数)} と書けば f-string によって解釈されて実行できる。

### comment(s)

何も出力しない。プロンプトにコメントを入れるためのもの。

### test(s)

settings で is_test が ON の場合に限り s を出力する。
RAG やログなどの仮当てをしてプロンプト編集作業をするのに使える。
WebAPIで推論する際には常に OFF とみなされる。

### msgf(v: str | list)

以下のようなコロン区切りの書式のstrを ChatGPT messages 形式のlistに変換する。

```
user: こんにちは、お元気ですか?
ai: はい、私は元気です
```

### iif(expr, t, f = '')

return t if expr else f

if文を関数として実行できるようにしたもの。使うとややこしくなる。

### rag(dir, query)

RAGタブで設置したzipを検索する。

### llm(dir, **kwargs)

他のpromptを呼び出す。

### var

varタグで保存したkeyに対応するvalueを {var.key} で埋め込める。

## RAG

- FAISS検索機能
- rag_dir を決めて zipをアップロードするとテキストにしてくれる
  - langchain.document_loaders.generic.GenericLoader に対応
- instruction から {rag('dir', 'query')} で呼び出せる

## var

- key-value型の変数機能
- key を決めて value を保存する
- instruction から {var.key} で呼び出せる

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
venv/bin/python -m uvicorn main:app
```

あるいは

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
