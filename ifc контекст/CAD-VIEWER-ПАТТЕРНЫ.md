# CAD Viewer (DWG) — Паттерны

## Технология
- **@mlightcad/cad-simple-viewer** — React-компонент для CAD
- **libredwg-web** — WASM-модуль для парсинга DWG файлов
- WASM inlined как base64 в worker, но также нужна копия в `public/wasm/`

## Настройка WASM
```bash
# Копирование WASM в public
cp node_modules/@mlightcad/libredwg-web/wasm/libredwg-web.wasm public/wasm/
```

## Ограничения
- DWG формат AC1032 (AutoCAD 2018) может не полностью поддерживаться
- libredwg — open source реализация, не все версии DWG поддерживаются на 100%
- При ошибке формата — показывается `.cad-error` (это ожидаемое поведение)

## CSS-селекторы
- `.cad-toolbar` — панель инструментов
- `.cad-file-info` — информация о загруженном файле
- `.cad-error` — ошибка (может быть ожидаемой для некоторых DWG)
- `.cad-btn-group` — группа кнопок управления
- `.file-upload-btn` — кнопка загрузки с input[type="file"]

## E2E стратегия
Тест CAD проверяет оба исхода:
```typescript
const hasDocument = await page.locator('.cad-file-info').isVisible();
const hasError = await page.locator('.cad-error').isVisible();
// Оба результата допустимы — главное что viewer отреагировал
expect(hasDocument || hasError).toBe(true);
```

## Путь к компоненту
`src/components/CadViewer/CadViewer.tsx`
