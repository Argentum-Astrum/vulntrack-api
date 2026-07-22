# Реестр доказательств

Актуальность: 21 июля 2026 года. Основной объект доказательства — публичный
репозиторий [Argentum-Astrum/vulntrack-api](https://github.com/Argentum-Astrum/vulntrack-api).
Прямые URL предпочтительнее скриншотов: они позволяют проверить состояние,
diff, timestamps и machine-readable данные без сокрытия контекста.

## Issues

| Issue | Назначение | Статус/доказательство |
|---|---|---|
| [#1](https://github.com/Argentum-Astrum/vulntrack-api/issues/1) | bootstrap | закрыта PR #3 |
| [#2](https://github.com/Argentum-Astrum/vulntrack-api/issues/2) | domain model | закрыта PR #16 |
| [#17](https://github.com/Argentum-Astrum/vulntrack-api/issues/17) | SQLite repository | закрыта PR #30 |
| [#18](https://github.com/Argentum-Astrum/vulntrack-api/issues/18) | validation bug | закрыта PR #31 |
| [#19](https://github.com/Argentum-Astrum/vulntrack-api/issues/19) | CRUD API | закрыта PR #31 |
| [#20](https://github.com/Argentum-Astrum/vulntrack-api/issues/20) | integration tests | закрыта PR #31 |
| [#21](https://github.com/Argentum-Astrum/vulntrack-api/issues/21) | unit-test suite | закрыта после evidence comment: PR #16/#30/#31/#33/#34 |
| [#22](https://github.com/Argentum-Astrum/vulntrack-api/issues/22) | security controls | закрыта PR #33 |
| [#23](https://github.com/Argentum-Astrum/vulntrack-api/issues/23) | CI/CD | закрыта PR #32 |
| [#24](https://github.com/Argentum-Astrum/vulntrack-api/issues/24) | engineering documentation | закрыта PR #34 |
| [#25](https://github.com/Argentum-Astrum/vulntrack-api/issues/25) | release v1.0.0 | закрыта PR #35, release run #37 успешен |
| [#26](https://github.com/Argentum-Astrum/vulntrack-api/issues/26) | filters and statistics | закрыта PR #36 |
| [#27](https://github.com/Argentum-Astrum/vulntrack-api/issues/27) | Git hooks | закрыта PR #33 |
| [#28](https://github.com/Argentum-Astrum/vulntrack-api/issues/28) | release v1.1.0 | закрыта PR #37, release run #45 успешен |
| [#29](https://github.com/Argentum-Astrum/vulntrack-api/issues/29) | platform research | закрыта PR #34 |
| [#38](https://github.com/Argentum-Astrum/vulntrack-api/issues/38) | final evidence reconciliation | PR #39 содержит `Closes #38` |

Итого создано 16 осмысленных issues; у каждой есть типовая label,
acceptance criteria и assignee. Создание milestones недоступно через
использованный connector и не заявляется как выполненное.

В существующем репозитории также был более ранний backlog #4–#15. После
сопоставления acceptance criteria issues #6, #11, #12 и #13 закрыты с
комментариями и ссылками на фактические PR/runs. Issues #4, #5, #7–#10, #14 и
#15 оставлены открытыми: их дополнительный service layer, controlled status
transitions, практический GitLab или annotated-tag детали выполнены не
полностью. Они не выдаются за завершённые требования текущего эксперимента.

## Pull requests и review

| PR | Изменение | Проверяемое свидетельство |
|---|---|---|
| [#3](https://github.com/Argentum-Astrum/vulntrack-api/pull/3) | bootstrap | merged, закрывает #1 |
| [#16](https://github.com/Argentum-Astrum/vulntrack-api/pull/16) | domain model | merged, CI успешен, закрывает #2 |
| [#30](https://github.com/Argentum-Astrum/vulntrack-api/pull/30) | SQLite repository | merged, review → fix → rerun → resolved |
| [#31](https://github.com/Argentum-Astrum/vulntrack-api/pull/31) | CRUD API | merged, 45 tests |
| [#32](https://github.com/Argentum-Astrum/vulntrack-api/pull/32) | staged CI | merged, run #24 |
| [#33](https://github.com/Argentum-Astrum/vulntrack-api/pull/33) | security and hooks | merged after real conflict, run #27 |
| [#34](https://github.com/Argentum-Astrum/vulntrack-api/pull/34) | docs, research, second conflict | merged, runs #30/#32 successful |
| [#35](https://github.com/Argentum-Astrum/vulntrack-api/pull/35) | release v1.0.0 | merged after run 29885778888 |
| [#36](https://github.com/Argentum-Astrum/vulntrack-api/pull/36) | filters and statistics | merged, 65 tests in run 29886233520 |
| [#37](https://github.com/Argentum-Astrum/vulntrack-api/pull/37) | release v1.1.0 | merged after run 29886462838 |
| [#39](https://github.com/Argentum-Astrum/vulntrack-api/pull/39) | final evidence audit | full run 29887024547 successful; closes #38 |

Review evidence for PR #30:

- [self-review with inline finding](https://github.com/Argentum-Astrum/vulntrack-api/pull/30#pullrequestreview-4750152471);
- [inline discussion](https://github.com/Argentum-Astrum/vulntrack-api/pull/30#discussion_r3626715924);
- [fix commit `547b67c`](https://github.com/Argentum-Astrum/vulntrack-api/commit/547b67c65b2c36df282019ae6c4b75614a3afe37);
- повторный run #14 успешен, после чего thread разрешён.

Автор review и автор исправления — один аккаунт. Это содержательная проверка
процесса и интерфейса, но **не независимое approval**.

## Основные commits

| Hash | Назначение |
|---|---|
| [`45a910e`](https://github.com/Argentum-Astrum/vulntrack-api/commit/45a910e) | merge bootstrap PR |
| [`b2223f1`](https://github.com/Argentum-Astrum/vulntrack-api/commit/b2223f1) | merge domain PR |
| [`547b67c`](https://github.com/Argentum-Astrum/vulntrack-api/commit/547b67c) | исправление после review |
| [`71d259e`](https://github.com/Argentum-Astrum/vulntrack-api/commit/71d259e) | merge storage PR |
| [`486a32c`](https://github.com/Argentum-Astrum/vulntrack-api/commit/486a32c) | merge CRUD PR |
| [`a8cebc4`](https://github.com/Argentum-Astrum/vulntrack-api/commit/a8cebc4) | merge CI PR |
| [`11144a7`](https://github.com/Argentum-Astrum/vulntrack-api/commit/11144a73413125cf83296347320739f7163b3c67) | первый двухродительский conflict-resolution commit |
| [`7d17523`](https://github.com/Argentum-Astrum/vulntrack-api/commit/7d17523120e0d7abad95212a8de810e40bccb791) | merge security/hooks PR |
| [`9142801`](https://github.com/Argentum-Astrum/vulntrack-api/commit/91428014ae234bcf9da0ab1afa2594c13514a945) | второй двухродительский conflict-resolution commit |
| [`f4f127b`](https://github.com/Argentum-Astrum/vulntrack-api/commit/f4f127b8a4732c0c01f61819396c4f53a5a4d580) | merge docs/research PR |
| [`0ac42b2`](https://github.com/Argentum-Astrum/vulntrack-api/commit/0ac42b2c111a5444428043a6381e057528d21963) | release v1.0.0 target |
| [`bf3e01d`](https://github.com/Argentum-Astrum/vulntrack-api/commit/bf3e01df49d9663381ecf774dc0d8c6e780b47ed) | merge v1.1 feature PR |
| [`0b203d1`](https://github.com/Argentum-Astrum/vulntrack-api/commit/0b203d19d124e650927316adc22413220758919a) | release v1.1.0 target |

На теге `v1.1.0` — 64 commits: 52 non-merge и 12 merge commits. Обычные
commits используют Conventional Commits; PR merge commits также получили
Conventional titles после настройки release flow. Ранние GitHub-generated
merge subjects сохранены как доказательство PR topology.

## CI runs и artifacts

| Run | Результат | Artifacts |
|---|---|---|
| [#24](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883052726) | lint/test/build/security success, release skipped | [quality 8515496840](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883052726/artifacts/8515496840), [package 8515504485](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883052726/artifacts/8515504485), [security 8515512321](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883052726/artifacts/8515512321) |
| [#27](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883765831) | 58 tests, 97.39% branch coverage, all mandatory jobs success | [quality 8515763554](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883765831/artifacts/8515763554), [package 8515770738](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883765831/artifacts/8515770738), [security 8515781279](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29883765831/artifacts/8515781279) |
| [#30](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885192578) | 58 tests, 97.39%, exact cache restored, all mandatory jobs success | [quality 8516264567](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885192578/artifacts/8516264567), [package 8516270696](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885192578/artifacts/8516270696), [security 8516279385](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885192578/artifacts/8516279385) |
| [v1.0 run #37](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885871737) | 59 tests, all five jobs including release success | [quality 8516483911](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885871737/artifacts/8516483911), [package 8516490665](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885871737/artifacts/8516490665), [security 8516497535](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885871737/artifacts/8516497535) |
| [v1.1 feature](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29886233520) | 65 tests, 97.67%, mandatory jobs success | quality, package, and security artifacts |
| [v1.1 run #45](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29886550409) | 65 tests, all five jobs including release success | [quality 8516712508](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29886550409/artifacts/8516712508), [package 8516716965](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29886550409/artifacts/8516716965), [security 8516723199](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29886550409/artifacts/8516723199) |
| [final audit](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29887024547) | 65 tests, 97.67%, all mandatory jobs success | final report/evidence content before PR #39 merge |

Machine-readable outputs: JUnit XML, Cobertura XML, Bandit JSON, pip-audit
JSON, detect-secrets JSON. Package artifact contains wheel and sdist. Artifact
IDs and digests are returned by GitHub; reports are intentionally not committed.

## Конфликты

Первый конфликт полностью описан в
[`docs/conflict-resolution.md`](conflict-resolution.md): параллельные CI и
security ветки конфликтовали в `Makefile`, `README.md`, `pyproject.toml` и
`requirements-audit.txt`. Remote merge commit `11144a7` имеет родителей
`09238aa` и `a8cebc4`, что машинно подтверждает настоящий merge.

Второй конфликт возник между docs и обновлённым `main` в `README.md` и
`SECURITY.md`. Local merge `98bc6a7` имеет родителей `6f430a3` и `7d17523`.
Remote merge [`9142801`](https://github.com/Argentum-Astrum/vulntrack-api/commit/91428014ae234bcf9da0ab1afa2594c13514a945)
имеет родителей `e1c0a95` и `7d17523`; ручное объединение подтверждено
успешным run #30 в PR #34.

## Releases

| Release | Tag target / workflow | Скачиваемые assets и SHA-256 |
|---|---|---|
| [v1.0.0](https://github.com/Argentum-Astrum/vulntrack-api/releases/tag/v1.0.0) | `0ac42b2`; [run 29885871737](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29885871737) | [`vulntrack_api-1.0.0-py3-none-any.whl`](https://github.com/Argentum-Astrum/vulntrack-api/releases/download/v1.0.0/vulntrack_api-1.0.0-py3-none-any.whl) `26bb2988…`; [`vulntrack_api-1.0.0.tar.gz`](https://github.com/Argentum-Astrum/vulntrack-api/releases/download/v1.0.0/vulntrack_api-1.0.0.tar.gz) `98da3193…` |
| [v1.1.0](https://github.com/Argentum-Astrum/vulntrack-api/releases/tag/v1.1.0) | `0b203d1`; [run 29886550409](https://github.com/Argentum-Astrum/vulntrack-api/actions/runs/29886550409) | [`vulntrack_api-1.1.0-py3-none-any.whl`](https://github.com/Argentum-Astrum/vulntrack-api/releases/download/v1.1.0/vulntrack_api-1.1.0-py3-none-any.whl) `528c0d39…`; [`vulntrack_api-1.1.0.tar.gz`](https://github.com/Argentum-Astrum/vulntrack-api/releases/download/v1.1.0/vulntrack_api-1.1.0.tar.gz) `71f40034…` |

Оба release jobs получили `contents: write` только после последовательного
успеха lint → test → build → security и использовали package artifact того же
run. Tag target, notes, asset names, sizes и digests проверены GitHub API.

## Защита `main` и ограничения

- Изменения фактически проводились через короткоживущие branches и PR.
- CI status виден в PR, но required check/approval rule через доступный
  connector не настроен и не заявляется.
- `CODEOWNERS` — декларативный owner, а не доказательство включённой защиты.
- GitLab и Bitbucket аккаунты не подключены. Их YAML и исследование не являются
  evidence реального MR/pipeline.
- Скриншоты не заменяют публичные URL; при сдаче можно снять интерфейсные кадры
  по перечисленным ссылкам, предварительно проверив отсутствие персональных
  данных. В репозиторий намеренно не добавлены изображения с данными сессии.
