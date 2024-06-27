# akachat

あかちゃんチャット

# あかちゃんファミリー

https://huggingface.co/aka7774

- trllm ローカルLLM(transformersで動くやつ)をすぐ試せるツール
- faiss ベクトル検索に使える基礎的なRAGツール
- loapi AI VTuberとかの姿や声を出す支援をするAPIサーバ
- OneGAI Linuxで複数のサーバのインストールや起動終了を管理するwebui

akachatは、これらのサーバの起動を前提として動作するAPIサーバです。

text-generation-webui や Dify などと同ジャンルのアプリです。

OpenAI / Anthropic / GoogleAI にも対応してるけど、ローカルAIとの親和性が高いです。

## 対応環境

WSL2 / Windows 11 / Linux Ubuntu 22.04

- CUDA必須です。
- インターネットに公開する場合は nginx で https化とBASIC認証推奨です。
  - WSL2かLinuxであればOneGAIで簡単に設定できます。

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

install.bat をダウンロードして実行

# 用語の定義

LLMごとに微妙に定義が違うのだけど、akachatでは次のように整理しています。

- instruction LLMに指示するためのテキスト SYS とか system と呼ばれる
- options trllm に渡して model.generate() に入れるパラメタなど
- inst_template Llama2系で言う &lt;s&gt; [INST] から始まる文字列
- chat_template tokenizer.chat_template
- prompt 上記すべてのセット

# Run

- 初回起動時にvenv作ってくれる
- 引数にはポート番号を入れる

```bash
bash run.sh 50000
```

- http://127.0.0.1:50000/docs
- http://127.0.0.1:50000/gradio

あるいは

```bash
venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 50000
```

gradioだけ起動したい場合

```bash
GRADIO_SERVER_NAME="0.0.0.0" GRADIO_SERVER_PORT=50000 venv/bin/python app.py
```

# api

## /api/prompt/infer

promptを実行するエンドポイント

- name サーバに保存されているpromptの名前
- input ユーザーの入力文字列
- messages チャット履歴(OpenAI形式)

## /api/prompt/stream

inferの戻り値がstreamになったもの

# クラウドLLM互換

互換性は不完全です。

## ローカル(llama.cpp, vllm, ollamaなど)

- すべて OpenAI API互換サーバとして OpenAI を指定して動作させてください
- 各サーバごとに互換性が不足している可能性があります(が、akachatではサポートしません)

## OpenAI

- repetition_penalty の入力値を frequency_penalty に適用する
- instruction があれば messages の先頭に insert する
- input があれば messages の末尾に append する

## Anthropic

- penaltyは設定できないっぽい
- anthropic では system は別途指定する
- 誤って messages で指定されていたら system に集約してあげる

## GoogleAI

- どんなオプションが指定できるかわからない
- google では system と user を同時に使えない
- instruction が指定されていたら user に変換してあげる
- content じゃなくて parts[] なので変換する

## 

# prompt

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

## faiss

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
