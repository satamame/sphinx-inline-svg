# 開発メモ

## 開始～公開

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

1. rye の build コマンドを実行。
    ```
    > rye build
    ```

### 公開

1. TestPyPI に公開する。
    ```
    > rye publish --repository testpypi --repository-url https://test.pypi.org/legacy/ --username __token__ --token pypi-ToKeN
    ```
1. PyPI に公開する。
    ```
    > rye publish --username __token__ --token pypi-ToKeN
    ```

## テスト

### テスト環境の準備

1. pytest をインストールした。
    ```
    > rye add --dev pytest
    ```
1. tests フォルダを作った。
1. グローバルの tox を更新した。
    ```
    > py -m pip install -U tox
    ```
1. tox.ini を書いた。
1. `py38` で依存関係が解決できなかったので、Python 3.9 以上を要求するようにした。
1. test_smoke.py を書いた。

### テストの実行

- 開発環境で実行
    ```
    > rye run pytest
    ```
- カバレッジつきで実行
    ```
    > rye run pytest --cov --cov-report=html
    ```
- tox で実行
    ```
    > tox
    ```
- Testing パネルから実行する場合
    - 設定 (*) により仮想環境の pytest を使うはずだが、だめならターミナルで仮想環境に入ってから実行してみる。
        - (*) settings.json の "python.testing.pytestPath"。
- tests フォルダをカバレッジから除外するために、pyproject.toml の "tool.coverage.run" セクションで `omit` を設定している。
    - これの代わりに settings.json の "python.testing.pytestArgs" で `--cov=xx` 等と設定すると、`Run Tests` や `Debug Tests` で coverage が走ってしまう。そして `Debug Tests` がブレークポイントで止まらないという問題がある。
