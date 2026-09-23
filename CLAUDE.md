# CLAUDE.md — guidance for Claude Code

<!-- ckit:skills:begin -->
## 🚨 Rules always-on → `~/.omp/agent/APPEND_SYSTEM.md`

Code-intel-first (codegraph · codebase-memory-mcp · serena TRƯỚC grep/read) · headroom cho output dài · memory + `agents/STATE.md` · loop C/D/E · doc-hygiene — **định nghĩa đầy đủ, KHÔNG lặp ở đây**: omp nhúng `~/.omp/agent/APPEND_SYSTEM.md` vào MỌI system prompt (không compact). Đọc file đó là luật bất biến.

## 🧩 Skills — CORE đọc ngay · SPECIALIST + on-demand đọc khi task khớp

Mỗi skill = 1 directory (Agent Skills open standard) có `SKILL.md` (frontmatter `name`+`description`). Project-local: `.omp/skills/<name>/`; global: `~/.omp/skills/<name>/`. Mỗi skill liệt kê 1 lần.

### ⛔ CORE always-on — mở `SKILL.md` NGAY, trước tool call đầu tiên (thứ tự = ưu tiên, đọc top-down)

  1. `/Users/nguyencongba/.omp/skills/codegraph/SKILL.md`
  2. `/Users/nguyencongba/.omp/skills/karpathy-guidelines/SKILL.md`
  3. `/Users/nguyencongba/.omp/skills/ponytail/SKILL.md`
  4. `/Users/nguyencongba/.omp/skills/8sync-cli/SKILL.md`

### 🧩 SPECIALIST always-on — biết khả năng, đọc body KHI task khớp

`impeccable` BẮT BUỘC mở body ngay khi có việc UI/design/redesign/audit (kèm `references/house/*`); `assp` copy/offer; `taste` chống slop; `image-routing` ảnh/diff/PDF.

- `assp-skill` — `/Users/nguyencongba/.omp/skills/assp-skill/SKILL.md`
- `impeccable` — `/Users/nguyencongba/.omp/skills/impeccable/SKILL.md`
- `design-taste-frontend` — `/Users/nguyencongba/.omp/skills/taste-skill/SKILL.md`
- `image-routing` — `/Users/nguyencongba/.omp/skills/image-routing/SKILL.md`
- `locate-anything` — `/Users/nguyencongba/.omp/skills/locate-anything/SKILL.md`

### 🔎 On-demand — tên = trigger; mở `SKILL.md` khi description khớp task

- `api-and-interface-design` — `~/.omp/skills/api-and-interface-design/SKILL.md`
- `browser-testing-with-devtools` — `~/.omp/skills/browser-testing-with-devtools/SKILL.md`
- `ci-cd-and-automation` — `~/.omp/skills/ci-cd-and-automation/SKILL.md`
- `code-review-and-quality` — `~/.omp/skills/code-review-and-quality/SKILL.md`
- `code-simplification` — `~/.omp/skills/code-simplification/SKILL.md`
- `constraint-driven-development` — `~/.omp/skills/constraint-driven-development/SKILL.md`
- `context-engineering` — `~/.omp/skills/context-engineering/SKILL.md`
- `debugging-and-error-recovery` — `~/.omp/skills/debugging-and-error-recovery/SKILL.md`
- `deprecation-and-migration` — `~/.omp/skills/deprecation-and-migration/SKILL.md`
- `documentation-and-adrs` — `~/.omp/skills/documentation-and-adrs/SKILL.md`
- `doubt-driven-development` — `~/.omp/skills/doubt-driven-development/SKILL.md`
- `feature` — `~/.omp/skills/feature/SKILL.md`
- `frontend-ui-engineering` — `~/.omp/skills/frontend-ui-engineering/SKILL.md`
- `full-flow` — `~/.omp/skills/full-flow/SKILL.md`
- `git-workflow-and-versioning` — `~/.omp/skills/git-workflow-and-versioning/SKILL.md`
- `idea-refine` — `~/.omp/skills/idea-refine/SKILL.md`
- `incremental-implementation` — `~/.omp/skills/incremental-implementation/SKILL.md`
- `interview-me` — `~/.omp/skills/interview-me/SKILL.md`
- `last30days` — `~/.omp/skills/last30days/SKILL.md`
- `observability-and-instrumentation` — `~/.omp/skills/observability-and-instrumentation/SKILL.md`
- `performance-optimization` — `~/.omp/skills/performance-optimization/SKILL.md`
- `planning-and-task-breakdown` — `~/.omp/skills/planning-and-task-breakdown/SKILL.md`
- `ponytail-audit` — `~/.omp/skills/ponytail-audit/SKILL.md`
- `ponytail-debt` — `~/.omp/skills/ponytail-debt/SKILL.md`
- `ponytail-gain` — `~/.omp/skills/ponytail-gain/SKILL.md`
- `ponytail-help` — `~/.omp/skills/ponytail-help/SKILL.md`
- `ponytail-review` — `~/.omp/skills/ponytail-review/SKILL.md`
- `security-and-hardening` — `~/.omp/skills/security-and-hardening/SKILL.md`
- `senior-frontend` — `~/.omp/skills/senior-frontend/SKILL.md`
- `senior-security` — `~/.omp/skills/senior-security/SKILL.md`
- `shipping-and-launch` — `~/.omp/skills/shipping-and-launch/SKILL.md`
- `source-driven-development` — `~/.omp/skills/source-driven-development/SKILL.md`
- `spec-driven-development` — `~/.omp/skills/spec-driven-development/SKILL.md`
- `test-driven-development` — `~/.omp/skills/test-driven-development/SKILL.md`
- `token-bench` — `~/.omp/skills/token-bench/SKILL.md`
- `using-agent-skills` — `~/.omp/skills/using-agent-skills/SKILL.md`
<!-- ckit:skills:end -->
