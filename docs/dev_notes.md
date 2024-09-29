# 開発メモ

## やったこと

### Rye のインストール

1. [インストーラ](https://rye.astral.sh/guide/installation/)をダウンロードして実行した。
1. 以下の質問には `Run the old default Python` を選択した。
    ```
    ? What should running `python` or `python3` do when you are not inside a Rye managed project?
    ❯ Run a Python installed and managed by Rye 
      Run the old default Python (provided by your OS, pyenv, etc.)
    ```
    - pylauncher で Python のバージョンを切り替えたりしていて、同じことが Rye で出来るか分からなかったので。

### プロジェクト作成

1. すでにこのフォルダ (sphinx-inlinle-svg) を作ってあったので以下を実行。
    ```
    > rye init
    > rye add --dev ruff
    > rye sync
    ```
1. pyproject.toml を編集した。

### ビルド

1. グローバルの Python で build を実行。
    ```
    > py -m build .
    ```