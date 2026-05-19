---
name: commit-push-pr
description: Git ワークフロー（ブランチ作成、コミット、PR 作成）を自動化する。
effort: low
---

# Git ワークフロー自動化

変更をコミットし、作業ブランチへプッシュして PR を作成するまでを自動化する。

## ワークフロー

### 1. 現状確認

```bash
git status
git diff --stat
```

### 2. 作業ブランチ作成

`main` へ直接 push しないこと。変更内容に応じたブランチ名を付けて作業ブランチを作成する。

例:

```bash
git switch -c fix/hogehoge
```

### 3. コミット

Conventional Commits 形式でコミットメッセージを生成:

- `feat(scope): 新機能の説明`
- `fix(scope): バグ修正の説明`
- `refactor(scope): リファクタリングの説明`
- `docs(scope): ドキュメント更新`
- `test(scope): テスト追加・修正`
- `chore(scope): その他の変更`

日本語で説明を記載すること。

### 4. 作業ブランチを push

```bash
git push -u origin <branch-name>
```

### 5. PR 作成

`gh` CLI を使って PR を作成する。base は通常 `main` とする。

**引数に issue 番号が指定されている場合**（例: `/commit-push-pr 17`）、PR 本文の末尾に `Closes #17` を追加する。
マージ時に issue が自動クローズされる。

```bash
# issue 番号なし
gh pr create --base main --head <branch-name> --title "<title>" --body "<body>"

# issue 番号あり（例: 17）
gh pr create --base main --head <branch-name> --title "<title>" --body "<body>

Closes #17"
```

PR タイトルはコミットメッセージと整合する内容にすること。本文には変更概要を簡潔に含めること。

PR URL を表示してユーザーに伝える。Codex レビューはユーザーが必要に応じて手動で行う。

### 6. マージ後のクリーンアップ（ユーザーが「完了」と言ったとき）

ユーザーが「完了」「マージした」等の合図を出したら、以下を実行する：

1. PR のマージ状態を確認する

```bash
gh pr view <pr-number-or-url> --json state,mergedAt
```

2. マージ済みであれば main に切り替え、pull、ローカルブランチを削除する

```bash
git switch main
git pull
git branch -d <branch-name>
```

マージされていない場合はその旨をユーザーに伝え、クリーンアップを行わない。

## 注意事項

- コミット前に `git diff` で変更内容を確認
- 機密情報（.env、credentials等）がないか確認
- `main` への直接 push は行わない
- `gh` CLI で GitHub にログイン済みであることを確認する
