# Как повторить эксперимент

Инструкция использует только публичный код. Не помещайте token в команды,
screenshots, `.env`, shell history или CI logs.

## 1. Локальная проверка

```bash
git clone https://github.com/Argentum-Astrum/vulntrack-api.git
cd vulntrack-api
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
make verify
```

Ожидается: Ruff clean, все tests green, branch coverage ≥80%, wheel/sdist в
`dist/`, Bandit/pip-audit/detect-secrets без blocking finding и hook syntax
valid. Сравните `reports/junit.xml` и `reports/coverage.xml` с CI artifacts.

## 2. GitHub

1. Fork/import repository или создайте новый public test repository.
2. Убедитесь, что Actions разрешены; дополнительных secrets pipeline не требует.
3. Создайте issue с acceptance criteria и branch `feat/<issue>-experiment`.
4. Сделайте Conventional Commit, push и PR с `Closes #<issue>`.
5. Запишите время создания run, старта первого job и завершения security job.
6. Скачайте quality/package/security artifacts и проверьте содержимое.
7. Оставьте реальный inline comment, исправьте код отдельным commit, дождитесь
   rerun и только затем resolve thread.
8. Для production включите branch rule: запрет direct/force push, required CI
   и независимое approval. Зафиксируйте фактические доступные настройки тарифа.
9. Повторите минимум три раза с неизменным runner/Python/commands и используйте
   медиану. Не выводите cache state только из времени.

## 3. GitLab

1. Импортируйте тот же commit SHA в новый GitLab project.
2. Не изменяйте `.gitlab-ci.yml`, Make targets или Python image между
   сравниваемыми runs.
3. Создайте эквивалентные issues и branches, затем минимум пять MR.
4. Проверьте branch/MR/tag pipeline rules, JUnit/Cobertura presentation,
   artifacts и tag release.
5. Запишите runner type, queue, timestamps каждого stage, cache result и total.
6. Настройте protected default branch в пределах доступного tier; required
   approvals и native security reports пометьте согласно фактическому тарифу.
7. Выполните не менее трёх successful runs и рассчитайте медиану отдельно от
   GitHub. Не смешивайте shared и self-managed runner measurements.

## 4. Bitbucket Cloud (необязательная практическая проверка)

1. Импортируйте тот же SHA и включите Pipelines.
2. Используйте committed `bitbucket-pipelines.yml` без изменения Make targets.
3. Проверьте default, pull-request и `v*` tag pipelines.
4. Зафиксируйте 14-day artifact retention, build minutes и фактический plan.
5. Отдельно пометьте встроенные функции, Code Insights presentation и внешние
   scanners/apps; Snyk не считать native scanner Bitbucket.

## 5. Шаблон измерения

| Platform | Run URL | Commit | Runner | Queue | Lint | Test | Build | Security | Total | Cache evidence |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| | | | | | | | | | | |

Храните raw job URLs и artifact IDs. Screenshot используйте только как
дополнение к URL и предварительно исключите credentials, private addresses и
лишние персональные данные.
