# Сравнение GitHub, GitLab и Bitbucket Cloud

Состояние исследования: 21 июля 2026 года. Объект сравнения — небольшой
публичный Python-проект с GitHub Flow, пятью последовательными CI-стадиями и
одним сопровождающим. Выводы относятся к этому контексту, а не объявляют
универсально лучшую платформу.

## Границы эксперимента и типы данных

| Платформа | Практический статус | Что допустимо считать фактом |
|---|---|---|
| GitHub | сценарий выполнен в `Argentum-Astrum/vulntrack-api` | PR, review thread, Actions, artifacts, issues, releases и времена по URL |
| GitLab | подготовлен `.gitlab-ci.yml`, аккаунт/runner не подключён | только анализ конфигурации и официальной документации; время pipeline не измерено |
| Bitbucket Cloud | подготовлен `bitbucket-pipelines.yml`, workspace не подключён | только анализ конфигурации и официальной документации; время pipeline не измерено |

В таблицах используются четыре метки:

- **измерено** — получено из конкретного запуска или файла репозитория;
- **наблюдение** — оценка автора по выполненному сценарию;
- **документация** — возможность подтверждена официальным источником;
- **не проверено** — конфигурация существует, но платформа её не исполняла.

## Методика оценки

Критерии и веса определены до выставления баллов. Оценка от 1 (плохо подходит)
до 5 (очень хорошо подходит) относится к заданному учебному проекту.

| Критерий | Вес | Почему важен |
|---|---:|---|
| CI/CD и воспроизводимость | 25% | центральный эксперимент задания |
| Review и совместная работа | 20% | защищает качество изменений |
| Безопасность и governance | 20% | объединяет проверки кода и контроль `main` |
| Issues и трассируемость | 15% | связывает требование с релизом |
| Доступность для малой команды | 10% | ограничения бесплатного тарифа влияют на результат |
| Экосистема и эксплуатация | 10% | интеграции, переносимость и сопровождение |

Итог: `Σ(балл × вес) / 100`.

| Платформа | CI | Review | Security | Trace | Cost | Ecosystem | Взвешенный итог |
|---|---:|---:|---:|---:|---:|---:|---:|
| GitHub | 4.8 | 4.6 | 4.5 | 4.6 | 4.8 | 4.8 | **4.67** |
| GitLab | 4.8 | 4.3 | 4.5 | 4.7 | 4.2 | 4.4 | **4.53** |
| Bitbucket Cloud | 4.0 | 4.3 | 3.6 | 4.2 | 4.2 | 4.1 | **4.04** |

GitHub получил небольшой контекстный перевес, потому что весь сценарий реально
проверен на нём и публичный репозиторий хорошо сочетается с доступными
возможностями. Разница с GitLab мала: при требовании единой DevSecOps-платформы,
self-managed установки или глубокой групповой governance веса изменятся и
GitLab может стать первым. Bitbucket особенно логичен для команды, чей основной
контур планирования уже находится в Jira.

## A. Настройка CI/CD

Все три YAML вызывают одинаковые команды из `Makefile`; это отделяет
платформенную оркестрацию от логики качества.

| Показатель | GitHub Actions | GitLab CI/CD | Bitbucket Pipelines |
|---|---:|---:|---:|
| конфигурационных файлов | 1 | 1 | 1 |
| строк платформенного YAML | 179 | 96 | 93 |
| основных jobs/stages | 5 | 5 | 5 для тега, 4 обычно |
| runner image | `ubuntu-latest` + Python 3.12 | `python:3.12-slim` | `python:3.12-slim` |
| push trigger | `push` | branch workflow rule | `default` |
| PR/MR trigger | `pull_request` | `merge_request_event` | `pull-requests: "**"` |
| tag trigger | `v*` | `$CI_COMMIT_TAG` | `tags: "v*"` |
| повторное использование | Make targets | те же Make targets | те же Make targets и YAML anchors |
| исполнение в эксперименте | **измерено** | **не проверено** | **не проверено** |

Количество строк измерено `wc -l`; комментарии и пустые строки сохранены,
поэтому это показатель обслуживаемого файла, а не сложности языка. Время
авторской настройки отдельно не хронометрировалось: указывать точные минуты
задним числом было бы выдуманным измерением. Наблюдение — GitLab оказался
короче благодаря встроенным `stages`, `reports` и `release`, а GitHub явнее
выражает permissions, dependencies и передачу artifacts.

Официальная документация подтверждает модель [GitHub workflow
syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[GitLab jobs и stages](https://docs.gitlab.com/ci/jobs/) и
[Bitbucket Pipelines](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/).

## B. Code review

| Возможность | GitHub | GitLab | Bitbucket Cloud |
|---|---|---|---|
| объект review | Pull Request | Merge Request | Pull Request |
| inline comments/threads | да; thread можно resolve | да; discussions можно resolve | да; inline comments и tasks |
| suggestion patch | да | да | да |
| формальный request changes | да | review/approval workflow | changes requested и tasks |
| CI рядом с diff | checks и summary | pipeline widget/reports | build status и Code Insights |
| required approvals на free | доступны для публичного GitHub-репозитория через protected branch/ruleset | approvals необязательны; required rules — Premium/Ultimate | checks рекомендуются; блокировка unresolved checks — Premium |
| CODEOWNERS | файл доступен; обязательность зависит от branch rule | required Code Owner approval — Premium/Ultimate | code owners поддерживаются; принудительные merge checks зависят от тарифа |

Практический GitHub-цикл выполнен в PR #30: inline-замечание к SQL,
исправляющий commit, повторный успешный CI, ответ и разрешение thread. Review
сделан тем же сопровождающим и поэтому обозначен как self-review, а не как
независимое одобрение.

Ограничения тарифов подтверждены документацией
[GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule),
[GitLab approvals](https://docs.gitlab.com/user/project/merge_requests/approvals/)
и [Bitbucket merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/).

## C. Pipeline

### Сопоставимые запуски GitHub

Команды, Python 3.12 и порядок стадий одинаковы. Время взято из timestamps
GitHub-hosted job logs. Оно включает установку зависимостей каждого job.

| Run | Условие | Queue | Lint | Test | Build | Security | Полный обязательный интервал |
|---|---|---:|---:|---:|---:|---:|---:|
| [#24](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883052726) | первая версия staged CI | ≈8 с | 18 с | 20 с | 24 с | 25 с | ≈103 с |
| [#27](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883765831) | hooks и secret scan | ≈6 с | 29 с | 17 с | 19 с | 28 с | ≈109 с |
| третий полный PR run | будет зафиксирован после docs PR | — | — | — | — | — | — |
| медиана трёх | после третьего run | — | — | — | — | — | — |

Кэш `setup-python` включён, но GitHub logs не дают достаточного основания
называть конкретный запуск гарантированно холодным или прогретым: ключ зависит
от зависимостей, а runner эфемерный. Поэтому это поле не домысливается.

Навигация GitHub по jobs и steps позволила локализовать стадию и получить логи
по отдельному job; rerun поддерживается на уровне run/failed jobs. Артефакты
quality и security хранятся 14 дней, package — 30 дней согласно YAML.

GitLab и Bitbucket не имеют трёх запусков в этом эксперименте, поэтому скорость
между платформами **не сравнивается**. GitLab-конфигурация задаёт `expire_in`,
JUnit и Cobertura; Bitbucket передаёт shared artifacts между steps. По
документации Bitbucket удаляет pipeline artifacts через 14 дней: [Pipeline
artifacts](https://support.atlassian.com/bitbucket-cloud/docs/use-artifacts-in-steps/).

Даже три GitHub-запуска — малая выборка одного публичного проекта. Медиана
описывает только этот сценарий и не является глобальным выводом о скорости.

## D. Права и безопасность

| Блок | GitHub | GitLab | Bitbucket Cloud |
|---|---|---|---|
| защита ветки | protected branches/rulesets, запрет push/force push, required checks/reviews | protected branches во всех tiers; granular group/Code Owner controls частично Premium/Ultimate | branch restrictions; принудительные unresolved merge checks Premium |
| SAST | CodeQL/code scanning для поддерживаемых условий; в проекте переносимый Bandit | native SAST/security reports, часть возможностей Ultimate; в проекте Bandit artifact | Code Insights принимает отчёты; сканер обычно pipe/app, в проекте Bandit artifact |
| dependency scanning | Dependabot/dependency graph по условиям продукта; здесь pip-audit | native Dependency Scanning — Ultimate; здесь pip-audit | Snyk/другая внешняя интеграция; здесь pip-audit |
| secret scanning | native secret scanning для public repositories и eligible plans; здесь дополнительно detect-secrets | native secret detection зависит от tier/настройки; здесь detect-secrets | внешняя интеграция или собственный step; здесь detect-secrets |
| PR/MR presentation | checks, annotations/security tabs в доступных режимах | MR widgets/security reports в доступных режимах | Code Insights reports/annotations требуют integration |

Принципиальное различие: Bitbucket Code Insights — интерфейс для reports и
annotations, а Snyk — устанавливаемый внешний security provider. Это не
называется встроенным SAST Bitbucket. Источники: [Code
Insights](https://support.atlassian.com/bitbucket-cloud/docs/code-insights/) и
[Snyk integration](https://support.atlassian.com/bitbucket-cloud/docs/add-and-configure-security-with-snyk/).

GitLab Free позволяет защищать ветви, но required approvals доступны в
Premium/Ultimate; [protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/)
и [dependency scanning](https://docs.gitlab.com/user/application_security/dependency_scanning/)
явно указывают tiers. Возможности GitHub зависят от visibility и тарифа;
[GitHub Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security)
различает public и private/internal repositories.

В текущем GitHub-репозитории CI имеет `contents: read`, а право
`contents: write` выдано только release job. Версионированный `CODEOWNERS`
указывает владельца, но настройка required approval/branch protection через
доступный connector не выполнялась. Это ограничение, а не успешный контроль.

## E. Issues и трассируемость

| Возможность | GitHub | GitLab | Bitbucket Cloud |
|---|---|---|---|
| базовые задачи | Issues, issue forms, labels, assignees, milestones | issues, types, labels, assignees, milestones, boards | встроенный простой issue tracker; глубокая работа через Jira integration |
| шаблоны | YAML issue forms/templates | issue templates | templates/work items зависят от Jira/workspace процесса |
| автозакрытие | closing keywords из merged PR | closing patterns из merged MR/default branch | resolve commands в commit messages; Jira Smart Commits отдельно |
| цепочка evidence | issue → branch → commit → PR → Actions → release | issue → branch → commit → MR → pipeline → release | issue/Jira → branch → commit → PR → Pipelines → downloads/deployments |
| поиск полного цикла | сильный единый поиск и cross-links | особенно цельная встроенная DevSecOps-модель | наиболее убедителен вместе с Jira |

В GitHub созданы issue forms и фактически пройдены связи через `Closes #...`.
Механизм документирован в [GitHub closing
keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).
GitLab предоставляет [issue boards](https://docs.gitlab.com/user/project/issue_board/),
а Bitbucket документирует [встроенные
issues](https://support.atlassian.com/bitbucket-cloud/docs/understand-bitbucket-issues/)
и отдельную [Jira
integration](https://support.atlassian.com/bitbucket-cloud/docs/connect-bitbucket-cloud-to-jira-cloud/).

## F. Применимость

- **Учебный проект:** GitHub — лучший выбор в данных условиях: минимальный
  вход, публичные evidence URL, знакомый PR/Actions lifecycle и реально
  проверенный free-сценарий.
- **Исследовательский проект:** GitLab предпочтителен, если нужны единая
  модель pipeline/security/release и воспроизводимый self-managed стенд;
  GitHub удобнее для открытого межорганизационного сотрудничества.
- **Небольшой промышленный проект:** GitHub подходит универсально; Bitbucket
  становится конкурентнее при уже оплаченной и глубоко используемой Jira;
  GitLab хорош для команды, желающей меньше отдельных DevOps-сервисов.
- **Крупная организация:** выбор определяется governance, identity, residency,
  self-managed требованиями и существующей экосистемой. GitLab силён цельным
  DevSecOps и self-managed вариантом, GitHub — экосистемой и enterprise
  collaboration, Bitbucket — связью с Atlassian stack. Нужен отдельный pilot,
  а не перенос оценок этого малого эксперимента.

## Тарифные и экспериментальные ограничения

- GitLab и Bitbucket не подключены: нет MR/PR, runner logs, artifacts, approval
  evidence и трёх измерений на этих платформах.
- GitHub self-review не заменяет независимого reviewer.
- Защита `main` не была включена через доступный GitHub connector; файл
  `CODEOWNERS` сам по себе её не включает.
- У Bitbucket Free до пяти пользователей, 50 build minutes и общий объём
  ресурсов workspace; принудительные merge checks относятся к Premium:
  [официальные цены](https://www.atlassian.com/software/bitbucket/pricing).
- Тарифы и продуктовые возможности меняются; перед промышленным решением
  источники необходимо проверить повторно.

## Официальные источники

### GitHub

- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
- [Pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning)
- [Secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning)

### GitLab

- [CI/CD YAML reference](https://docs.gitlab.com/ci/yaml/)
- [Jobs and stages](https://docs.gitlab.com/ci/jobs/)
- [Job artifacts](https://docs.gitlab.com/ci/jobs/job_artifacts/)
- [Merge request approvals](https://docs.gitlab.com/user/project/merge_requests/approvals/)
- [Protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/)
- [Security scanning results](https://docs.gitlab.com/user/application_security/detect/security_scanning_results/)
- [Release CI/CD examples](https://docs.gitlab.com/user/project/releases/release_cicd_examples/)

### Bitbucket Cloud

- [Pipelines](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)
- [Pipeline steps](https://support.atlassian.com/bitbucket-cloud/docs/step-options/)
- [Artifacts](https://support.atlassian.com/bitbucket-cloud/docs/use-artifacts-in-steps/)
- [Pull-request review](https://support.atlassian.com/bitbucket-cloud/docs/review-code-in-a-pull-request/)
- [Merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/)
- [Code Insights](https://support.atlassian.com/bitbucket-cloud/docs/code-insights/)
- [Snyk integration](https://support.atlassian.com/bitbucket-cloud/docs/add-and-configure-security-with-snyk/)
- [Pricing](https://www.atlassian.com/software/bitbucket/pricing)
