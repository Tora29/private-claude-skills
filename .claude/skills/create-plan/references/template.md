# plan.md テンプレート

以下をそのままコピーして、`{...}` の箇所を埋める。

---

````markdown
# 計画書: {タスク名}

## タスク概要

{何を・なぜ作るか。3行以内で記述。}

## スコープ

### やること

- {具体的な実装項目}

### やらないこと（明示的除外）

- {スコープ外の項目・後回しにするもの}

## 対象ファイル一覧

| パス                                                    | 種別 | 役割                          |
| ------------------------------------------------------- | ---- | ----------------------------- |
| `src/routes/{feature}/_lib/schema.ts`                   | 新規 | Zod バリデーションスキーマ    |
| `src/routes/{feature}/_lib/service.ts`                  | 新規 | DB 操作・ビジネスロジック     |
| `src/routes/{feature}/+server.ts`                       | 新規 | API ハンドラ                  |
| `src/routes/{feature}/+page.svelte`                     | 新規 | 画面コンポーネント            |
| `src/routes/{feature}/_lib/schema.test.ts`              | 新規 | Zod スキーマ Unit テスト      |
| `src/routes/{feature}/_lib/service.integration.test.ts` | 新規 | サービス層 Integration テスト |
| `e2e/{feature}.e2e.ts`                                  | 新規 | E2E テスト                    |

## 実装順序

依存関係を考慮した番号付き順序。

1. `{ファイルパス}` — {何をするか}
2. `{ファイルパス}` — {何をするか}（依存: 1が完了後）
3. `{ファイルパス}` — {何をするか}

## 各タスク詳細

### 1. {タスク名}

**ファイル**: `{パス}`
**種別**: 新規 / 変更 / 削除

**主要な関数・型**:

```typescript
export async function functionName(
	db: DrizzleD1Database,
	userId: string,
	data: EntityCreate
): Promise<Entity>;
```
````

**入出力**:

- 入力: `{型と意味}`
- 出力: `{型と意味}`

**エラー・境界値の扱い**:

- `{条件}` のとき `AppError('{ErrorCode}', {status}, '{メッセージ}')` を throw
- `{条件}` のとき `{返却値や動作}`

**実装上の制約・注意**:

- {ルールファイルへの参照など}

---

### 2. {タスク名}

（同様に記述）

---

## テスト方針

`.claude/rules/testing.md` に準拠する。

| テストファイル                                          | 対象           | テスト種別  | 検証内容（AC）             |
| ------------------------------------------------------- | -------------- | ----------- | -------------------------- |
| `src/routes/{feature}/_lib/schema.test.ts`              | `schema.ts`    | Unit        | AC-101〜199 バリデーション |
| `src/routes/{feature}/_lib/service.integration.test.ts` | `service.ts`   | Integration | AC-001〜099 DB操作         |
| `e2e/{feature}.e2e.ts`                                  | ユーザーフロー | E2E         | AC-001, AC-002             |

### テストケース概要

- 正常系（Integration）: {入力} → {期待出力}
- 異常系（Unit/schema）: {不正入力} → `VALIDATION_ERROR` が返ること
- 境界値（Unit/schema）: {境界条件} → {期待動作}

## 実装後の期待状態

### システム・動作の変化

- {変更前}: {現状の動作}
- {変更後}: {実装後の動作}

### ユーザー・利用者から見た変化

- {誰が}: {何をしたとき}: {どう変わるか}

### 運用・インフラへの影響

- {D1 マイグレーション・R2 バケット・環境変数など。変化なしなら「なし」と明記}

---

## 完了条件

- [ ] `npm run test` が全テスト通過（unit + integration + e2e）
- [ ] `npm run check` TypeScript 型チェックがエラーなし
- [ ] `npm run lint` Lint がエラーなし
- [ ] `npm run build` ビルドが成功
- [ ] 全ファイルに `.claude/rules/file-headers.md` のヘッダーが付与されている
- [ ] エラーハンドリングが `.claude/rules/error-handling.md` に準拠している
- [ ] {機能固有の確認項目}

## 関連ルール・参照

- `.claude/rules/api-patterns.md` — API 設計・ハンドラパターン
- `.claude/rules/schemas.md` — Zod バリデーションスキーマ
- `.claude/rules/error-handling.md` — エラーハンドリング
- `.claude/rules/file-headers.md` — ファイルヘッダー
- `.claude/rules/testing.md` — テスト方針
- `.claude/rules/svelte.md` — Svelte 5 Runes モード規約
- `.claude/rules/data-testid.md` — テストセレクタ規約

```

```
