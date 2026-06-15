---
name: execute-plan
description: issue番号を引数に指定し、対応するplan.mdのチェックリストを順番に実行する。進捗をissueコメントで報告し、完了後にPRを作成する。
allowed-tools: Bash, Read, Write, Edit
effort: high
---

# execute-plan

issue番号に対応する `.claude/plan/Issue-{番号}-*.md` を読み込み、
チェックリストを順番に実行する。各ステップ完了後にissueへコメントで進捗を報告し、
全完了後に `/commit-push-pr {issue番号}` でPRを作成する。

**使用例**: `/execute-plan 17`

---

## ステップ 1: issue・plan ファイルの読み込み

引数から issue 番号を取得し、内容と対応する plan ファイルを読み込む。

```bash
# issue の内容を取得
gh issue view {番号} --json title,body,state

# 対応する plan ファイルを探す
ls .claude/plan/Issue-{番号}-*.md 2>/dev/null
```

- issue が `closed` の場合、その旨をユーザーに伝えて処理を中断する
- plan ファイルが見つからない場合、`/create-plan` でplan.mdを先に作成するよう促す
- 両方確認できたらユーザーに概要を提示して実行開始を確認する

> issue #17「{タイトル}」の実装を開始します。
> plan: `.claude/plan/Issue-17-{タイトル}.md`（{N}ステップ）
> 進めてよいですか？

---

## ステップ 2: チェックリストを順番に実行

plan.md の「完了条件」チェックリストを上から1つずつ実行する。

各チェックリストアイテムの処理:

1. アイテムの内容を確認し、実装作業を行う
2. 完了したら plan.md のチェックボックスを `- [x]` に更新する
3. issue にコメントで進捗を報告する

```bash
gh issue comment {番号} --body "✅ ステップ{N}完了: {アイテムの内容}"
```

エラーが発生した場合:

- エラー内容をユーザーに伝える
- 自動リトライせず、ユーザーの判断を仰ぐ

---

## ステップ 3: 全完了後の報告

全チェックリストが完了したら issue にコメントする。

```bash
gh issue comment {番号} --body "🎉 全ステップ完了。PRを作成します。"
```

---

## ステップ 4: plan ファイルを done/ へ移動

実装済みの plan ファイルを `done/` サブディレクトリへ移動する。

```bash
mkdir -p .claude/plan/done
mv .claude/plan/Issue-{番号}-*.md .claude/plan/done/ 2>/dev/null || true
```

- `done/` が存在しない場合は `mkdir -p` で自動作成する
- `mv` 失敗時（ファイルが既に移動済み等）はエラーを無視して継続する

---

## ステップ 5: PR 作成

`/commit-push-pr {issue番号}` を実行するようユーザーに促す。
（PRの `Closes #{番号}` でマージ時に issue が自動クローズされる）

> 実装完了です。`/commit-push-pr {番号}` でPRを作成してください。
