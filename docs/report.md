# Отчёт: Git, платформы совместной разработки и CI/CD

**Проект:** Baumanka Findings API (`Argentum-Astrum/vulntrack-api`)  
**Работа:** полный процесс разработки программного продукта  
**Дата эксперимента:** 21 июля 2026 года  
**Автор / группа:** заполняется обучающимся перед сдачей

## 1. Цель и задачи

Цель — на работающем программном продукте проверить полный lifecycle:
планирование через issues, короткоживущие Git-ветви, review, конфликты,
автоматические quality/security gates, artifacts и Semantic Versioning
releases. Дополнительная цель — сравнить GitHub, GitLab и Bitbucket Cloud по
заранее установленным критериям, отделив наблюдения от документации.

Задачи: реализовать API учёта результатов ИБ-проверок, обеспечить тестируемую
архитектуру и ≥70% покрытия, построить переносимый pipeline, пройти review с
исправлением, документировать два конфликта и выпустить `v1.0.0`/`v1.1.0`.

## 2. Исследовательские вопросы

1. Сколько платформенной конфигурации требуется для одинаковых стадий?
2. Насколько прозрачен цикл issue → code review → CI → artifact → release?
3. Какие controls встроены, какие требуют тарифа, а какие являются внешними?
4. Что можно заключить из малой серии сопоставимых pipeline runs?
5. Какая платформа лучше подходит разным типам проекта?

## 3. Проект

VulnTrack, также называемый в работе Baumanka Findings API, хранит результаты
проверок безопасности. API предоставляет health check, CRUD, валидацию,
фильтры по `severity`/`status` и статистику серьёзности. Имя существующего
репозитория сохранено по прямому запросу пользователя; это осознанное
отклонение от исходного требования создать новый репозиторий `Baumanka`.

## 4. Архитектура

Поток запроса: HTTP client → FastAPI route → Pydantic schema → repository →
SQLite. `create_app()` принимает database path, что изолирует интеграционные
тесты. Domain enums задают допустимые severity/status, schema отвечает за
boundary validation, repository использует parameterized SQL.

Ключевые решения, trade-offs и будущие направления изложены в
[`architecture.md`](architecture.md).

## 5. Организация Git-репозитория

Исходный код размещён в `src/`, тесты разделены на `tests/unit` и
`tests/integration`, общие команды — в `Makefile`, CI — в platform YAML,
локальные hooks — в `.githooks`, инженерные материалы — в `docs`. Generated
reports, package artifacts, virtual environments, databases и credentials не
коммитятся.

## 6. Стратегия ветвления

Выбран GitHub Flow: issue определяет проверяемый результат; branch получает
короткое имя с номером issue; commits малы и используют Conventional Commits;
PR содержит `Closes #N`, checks и review; после merge ветвь удаляется или
перестаёт использоваться. Для небольшого API и частых безопасных изменений
это проще Git Flow с долгоживущими release/develop ветвями. Подробности:
[`git-workflow.md`](git-workflow.md).

## 7. История commits

На теге `v1.1.0` — 64 commits: 52 non-merge и 12 merge. Обычные subjects
следуют Conventional Commits (`feat`, `fix`, `test`, `docs`, `ci`, `build`,
`security`, `chore`, `refactor`). Ранние GitHub-generated merge subjects
сохранены, потому что они доказывают topology реальных PR.

История развивалась по слоям: bootstrap → domain → SQLite → CRUD → CI →
security/hooks → docs → release → v1.1 feature → release. Commit hashes
перечислены в [`evidence.md`](evidence.md).

## 8. Issues и трассируемость

Создано 16 GitHub issues, включая bootstrap, domain/storage/CRUD, bug,
unit/integration tests, CI, security, hooks, docs, два releases и отдельное
исследование/final audit. Issues имеют labels, assignee, описание и acceptance
criteria. `Closes #...` связывает merged PR с задачей; Actions и release затем
связываются с merge commit/tag.

Milestones не создавались: доступный GitHub connector позволяет назначить
существующий milestone, но не предоставляет его создание. Это не скрывается.

## 9. Pull requests и code review

Финальный evidence PR #39 доводит проверяемое число PR до 11: #3, #16,
#30–#37 и #39. Каждый крупный слой и release прошёл отдельным PR с checks; у
#39 успешен run 29887024547. В PR #30 опубликован inline
comment о динамической SQL-строке. Commit `547b67c` заменил её статическим
parameterized update и добавил regression test; CI повторно прошёл, автор
ответил и разрешил discussion.

Review выполнен тем же аккаунтом, поэтому доказывает интерфейсный процесс, но
не независимое approval. Выдуманный reviewer не создавался.

## 10. Защита `main`

Фактическая дисциплина: изменения проводятся через PR, CI запускается на PR и
push, force push не использовался, release получает write permission только в
своём job. В репозитории есть `CODEOWNERS`, но required checks/reviews и запрет
direct push через доступный connector включить нельзя. Поэтому UI setting не
заявляется выполненным. Для production следует создать branch rule: запретить
direct/force push, потребовать CI и минимум одно независимое approval.

## 11. CI/CD

Pipeline: `lint → test → build → security → release`. GitHub Actions реально
исполнен; GitLab и Bitbucket конфигурации вызывают те же Make targets и
помечены как unexecuted. Python фиксирован на 3.12, runtime dependency roots для
аудита имеют точные версии. Quality, package и security artifacts разделены.

Release запускается только по `v*` tag или документированному
`chore(release):` merge
context в `main`; все предшествующие gates обязательны. Подробная схема,
retention и timestamps: [`ci-cd.md`](ci-cd.md).

## 12. Тестирование и покрытие

На `v1.1.0` собрано 65 test cases: 51 в `tests/unit`, 13 API integration и 1
health smoke. GitHub release run #45 показал 97.67% branch coverage;
pipeline требует не менее 80%, что строже задания. Результаты публикуются как
JUnit XML и Cobertura XML/HTML artifact.

Тесты проверяют Pydantic boundary cases, repository lifecycle и ошибки,
complete HTTP CRUD/validation, hook policies и отсутствие небезопасных
паттернов в scripts.

## 13. Security checks

- Ruff format и lint;
- Bandit SAST по `src`;
- pip-audit по изолированным exact runtime roots;
- detect-secrets по repository files;
- least-privilege workflow permissions;
- parameterized SQLite queries и input validation.

JSON-отчёты сохраняются как artifacts. Автоматический green result означает
прохождение заданных правил, а не отсутствие всех уязвимостей.

## 14. Git hooks

`scripts/install-hooks.sh` задаёт `core.hooksPath=.githooks` и поддерживает
uninstall. `pre-commit` запускает Ruff format/lint, `commit-msg` проверяет
Conventional Commits, `pre-push` запускает pytest. Hook scripts executable и
проверяются отдельными unit tests. Hooks можно обойти `--no-verify`, поэтому
CI повторяет обязательные проверки.

## 15. Конфликты

Конфликт 1 появился между параллельными CI и security/hooks ветвями в четырёх
файлах. Решение объединило команды обеих сторон; настоящий two-parent commit
`11144a7` и успешный PR #33 подтверждают результат.

Конфликт 2 появился при синхронизации независимо развивавшихся docs и
security ветвей. Причина, маркеры, parents, ручное решение и проверки
фиксируются в [`conflict-resolution.md`](conflict-resolution.md). `main` в
процессе не ломается.

## 16. Releases

[`v1.0.0`](https://github.com/Argentum-Astrum/vulntrack-api/releases/tag/v1.0.0)
фиксирует CRUD baseline, SQLite, tests, CI/security/hooks и документацию;
release run 29885871737 завершил все пять jobs.
[`v1.1.0`](https://github.com/Argentum-Astrum/vulntrack-api/releases/tag/v1.1.0)
добавляет filters/statistics; run 29886550409 также завершил все пять jobs.
Каждый Release содержит wheel/sdist из того же gated run и versioned notes.

## 17. Методика сравнения платформ

До оценки заданы веса: CI 25%, review 20%, security/governance 20%, traceability
15%, доступность для малой команды 10%, ecosystem 10%. Баллы 1–5 рассчитаны
для публичного учебного Python-проекта. Измерения, наблюдения, official docs и
непроверенные предположения разделены.

Полная методика и расчёт: [`platform-comparison.md`](platform-comparison.md).

## 18. Результаты GitHub и GitLab

На GitHub реально пройдены issue/branch/commit/PR/review/CI/artifact/merge
сценарии. Три сопоставимых mandatory spans — ≈103, ≈109 и ≈99 секунд;
медиана ≈103 секунды. Первый lint cache был cold, runs #27/#30 содержат restore
evidence. Это малая серия на GitHub-hosted runners, не общий speed benchmark.

Для GitLab подготовлен эквивалентный `.gitlab-ci.yml` с пятью stages, branch/MR/
tag rules, JUnit/Cobertura, artifacts и tag release через актуальный GitLab CLI.
Без GitLab project/runner нет MR, logs и measurements; они не фабрикуются.

## 19. GitHub, GitLab и Bitbucket — итоговая таблица

| Платформа | Взвешенная оценка | Сильная сторона в данном контексте | Главный caveat |
|---|---:|---|---|
| GitHub | 4.67/5 | проверенный public PR/Actions ecosystem | independent approval и branch rule не настроены |
| GitLab | 4.53/5 | цельный CI/reports/release/DevSecOps контур | required approvals/security features зависят от tier; сценарий не запущен |
| Bitbucket Cloud | 4.04/5 | Atlassian/Jira lifecycle и понятные Pipelines | security чаще external; enforced merge checks Premium; сценарий не запущен |

## 20. Тарифные и экспериментальные ограничения

GitLab и Bitbucket исследованы по официальной документации и валидным YAML, но
не по фактическим runs. GitHub review не независимый. `main` settings не
изменены. Cache temperature нельзя достоверно вывести только из elapsed time.
Три runs недостаточны для общего вывода о performance. Тарифы датированы и
могут измениться.

## 21. Применимость

Для данного учебного проекта выбран GitHub: минимальное трение, публичные
evidence и реально проверенный pipeline. Для self-managed исследовательского
стенда и единого DevSecOps процесса особенно силён GitLab. Для небольшой
команды в Jira-центричной организации Bitbucket может снизить организационные
издержки. Крупной организации нужен pilot с её identity, governance, residency,
security и cost constraints; баллы этого проекта переносить нельзя.

## 22. Соответствие требованиям

Проверяемая матрица со статусом, URL/hash и ограничениями находится в
[`assignment-compliance.md`](assignment-compliance.md). Основное осознанное
отклонение — использование существующего репозитория по запросу пользователя.
Главное внешнее ограничение — отсутствие GitLab доступа.

## 23. Источники и приложения

Официальные источники GitHub, GitLab и Atlassian перечислены рядом с каждым
сравниваемым утверждением в [`platform-comparison.md`](platform-comparison.md).
Ссылки на issues, PR, review, Actions, artifacts, commits, conflicts, tags и
releases собраны в [`evidence.md`](evidence.md). Инструкция повторения:
[`reproduce-experiment.md`](reproduce-experiment.md).

Markdown является редактируемой исходной версией отчёта и корректно
рендерится непосредственно в GitHub.
