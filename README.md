# Simbir Practicum UI

E2E UI-автотесты для сайта [Automation Test Store](https://automationteststore.com/).

## Что в проекте

- `pytest` + `selenium`
- `Page Object`
- `Allure`-отчеты
- параллельный запуск через `pytest-xdist`
- запуск в GitHub Actions с публикацией Allure в GitHub Pages

## Структура

- [docs/test_cases.md](docs/test_cases.md) — тест-кейсы
- `config/` — конфигурация проекта
- `locators/` — локаторы страниц
- `pages/` — Page Object
- `data/` — тестовые данные и вспомогательные значения
- `test/` — UI-тесты

## Запуск тестов

Обычный запуск:

```bash
pytest
```

Headless-режим:

```bash
pytest test/ --headless
```

Параллельный запуск:

```bash
pytest test/ --headless -n auto
```

## Allure

Сгенерировать локальный отчет:

```bash
pytest test/ --headless --alluredir=allure-results
allure generate allure-results --clean -o allure-report
```

## CI

В GitHub Actions настроены:

- запуск тестов
- генерация Allure-отчета
- публикация отчета в GitHub Pages
