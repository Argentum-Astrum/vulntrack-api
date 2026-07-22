# Матрица соответствия заданию

Статусы: **выполнено**, **в процессе**, **ограничение**, **осознанное
отклонение**. Матрица фиксирует проверяемое состояние, а не намерение.

| Требование | Статус | Доказательство | Комментарий/ограничение |
|---|---|---|---|
| Новый проект `Baumanka` | осознанное отклонение | README описывает Baumanka Findings API | пользователь прямо попросил выполнить работу в уже существующем репозитории; repository name не переименован |
| Работающий API и архитектура | выполнено | `src/vulntrack`, `docs/architecture.md`, PR #16/#30/#31 | FastAPI + Pydantic + SQLite repository |
| README, LICENSE, `.gitignore` | выполнено | файлы в корне | MIT — явно зафиксированное допущение |
| ≥30 осмысленных commits | выполнено | `git rev-list`, `docs/evidence.md` | на `v1.1.0`: 64 total, 52 non-merge |
| Conventional Commits | выполнено | `git log`, `.githooks/commit-msg` | GitHub-generated merge subjects — документированное исключение |
| ≥3 реально использованных branches, целевое ≥5 | выполнено | PR #3, #16, #30–#37 | 10 issue/release branches до final evidence branch |
| 2 реальных конфликта | выполнено | `docs/conflict-resolution.md`, remote merges `11144a7` и `9142801` | оба two-parent commits проверяемы на GitHub |
| tags/releases v1.0.0 и v1.1.0 | выполнено | release URLs, runs 29885871737/29886550409 | оба tag target проверены, у каждого wheel + sdist |
| GitHub Flow обоснован | выполнено | `docs/git-workflow.md` | короткоживущие issue branches + PR |
| ≥5 GitHub PR | выполнено | PR #3/#16/#30–#37 | 10 merged PR до final evidence PR |
| ≥5 GitLab MR | ограничение | `.gitlab-ci.yml` | GitLab не подключён; пользователь разрешил завершить эту часть самостоятельно |
| У PR есть issue и проверки | выполнено | PR descriptions, checks, evidence register | закрывающие keywords использованы в новых PR |
| Inline review comments | выполнено | PR #30 review/discussion | содержательное SQL замечание |
| Исправление после review + rerun | выполнено | commit `547b67c`, PR #30, run #14 | thread разрешён только после success |
| Независимый reviewer | ограничение | disclosure в evidence | self-review не выдан за независимое approval |
| Защита `main` | ограничение | `CODEOWNERS`, `docs/evidence.md` | connector не предоставляет изменение branch rule; required checks не заявлены |
| ≥10 GitHub issues | выполнено | issues #1/#2/#17–#29/#38 | 16 issues, labels, assignee, acceptance criteria |
| ≥10 GitLab issues | ограничение | — | GitLab не подключён |
| Отдельная research issue | выполнено | issue #29 | platform comparison |
| Issue → PR links | выполнено | `Closes #...` в PR #30–#37 | automatically closed issues and evidence comment for cross-PR #21 |
| CI на push и PR | выполнено | `.github/workflows/ci.yml`, Actions runs | также branch/tag/manual triggers |
| lint/test/build/security/release | выполнено | runs #37/#45 | все пять sequential jobs success в обоих releases |
| coverage + machine-readable report | выполнено | run #45 quality artifact | 97.67% branch coverage, Cobertura + JUnit |
| downloadable build artifact | выполнено | releases v1.0.0/v1.1.0 | wheel + sdist с GitHub digest; CI retention 30 days |
| отдельный release/tag pipeline | выполнено | main runs #37/#45 и `v*` trigger | release job реально исполнился дважды |
| ≥15 unit tests | выполнено | `tests/unit`, run #45 | 51 unit test cases |
| ≥3 integration tests | выполнено | `tests/integration`, run #45 | 13 integration + 1 health smoke |
| coverage ≥70% | выполнено | run #45 | 97.67% branch, enforced ≥80% |
| pre-commit hook | выполнено | `.githooks/pre-commit`, tests | Ruff format + lint |
| commit-msg hook | выполнено | `.githooks/commit-msg`, tests | Conventional Commits regex |
| pre-push hook | выполнено | `.githooks/pre-push`, tests | pytest |
| Обязательные документы | выполнено | README, CONTRIBUTING, CHANGELOG, SECURITY, `docs/*` | полный editable report в PR #34 |
| Полный GitHub-сценарий | выполнено | issues → PR → review → Actions → artifacts → releases | два versioned release lifecycle завершены |
| GitLab/Bitbucket configs | выполнено как переносимый пример | `.gitlab-ci.yml`, `bitbucket-pipelines.yml` | явно не выдаются за запущенные |
| Общее сравнение 3 платформ | выполнено | `docs/platform-comparison.md` | official docs + GitHub measurements |
| ≥3 успешных GitHub runs и медиана | выполнено | runs #24/#27/#30, `docs/ci-cd.md` | mandatory-span median ≈103 s |
| ≥3 успешных GitLab runs | ограничение | — | нет GitLab project/runner доступа |
| Тарифные ограничения | выполнено | platform comparison | сведения датированы и снабжены official URLs |
| Нет сфабрикованных действий | выполнено | disclosures во всех evidence docs | отсутствующие approvals/runs/settings явно помечены |

## Необходимые внешние действия для полного буквального соответствия

Они не могут быть честно заменены файлами в GitHub-репозитории:

1. создать/импортировать эквивалентный GitLab project;
2. создать минимум 10 GitLab issues и 5 MR, назначить реального reviewer;
3. выполнить минимум три GitLab pipelines на сопоставимом runner;
4. настроить protected `main` и required checks/approval в UI/API доступного
   тарифа на обеих практически исследуемых платформах;
5. при необходимости приложить обезличенные screenshots интерфейса.

До выполнения этих действий матрица сохраняет статус **ограничение**, а не
создаёт фиктивные evidence.
