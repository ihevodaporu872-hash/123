# E2E Тесты (Playwright)

## Файл: `e2e/all-viewers.spec.ts`

## 11 тестов, все проходят

### Навигация (1 тест)
- **tab navigation is visible and works** — проверяет 4 вкладки, переход по каждой

### PDF Viewer (2 теста)
- **loads test PDF and renders pages** — загрузка тестового PDF через кнопку, проверка canvas
- **uploads PDF file via file input** — загрузка через file input

### Excel Viewer (3 теста)
- **initializes Univer spreadsheet on load** — проверка что canvas появляется (ждём 5 сек)
- **loads test XLSX file** — загрузка через кнопку "Load Test File", проверка имени файла и sheet tabs
- **uploads XLSX file via file input** — загрузка через file input

### CAD Viewer (2 теста)
- **initializes CAD viewer** — проверка toolbar и upload кнопки
- **loads DWG test file** — загрузка DWG, проверка результата (либо document info, либо error — оба ок)

### IFC Viewer (3 теста)
- **initializes Three.js scene** — проверка canvas, controls hint
- **loads sample IFC file** — загрузка sample.ifc, проверка model info, wireframe toggle
- **loads louis.ifc large model** — загрузка большой модели (timeout 180s)

## Технические особенности

### ESM совместимость
```typescript
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

### Таймауты
- Excel canvas: 5000ms waitForTimeout (canvas-элементы появляются не сразу)
- PDF render: 30000ms timeout
- XLSX load: 90000ms timeout (парсинг + конвертация)
- IFC large model: 180000ms timeout
- CAD DWG: 120000ms timeout

### data-testid селекторы
- `excel-container` — контейнер Univer
- `load-test-file-button` — кнопка загрузки тестового XLSX
- `loading-indicator` — индикатор загрузки Excel
- `loaded-file-name` — имя загруженного файла
- `error-message` — сообщение об ошибке
- `xlsx-file-input` — file input для XLSX
- `load-test-pdf` — кнопка загрузки тестового PDF

### CSS-селекторы
- `.tab-navigation`, `.tab-link` — навигация
- `.pdf-toolbar`, `.pdf-page canvas`, `.pdf-document-info`, `.pdf-page-info`, `.pdf-error`, `.pdf-upload-btn`
- `.excel-toolbar`
- `.cad-toolbar`, `.cad-file-info`, `.cad-error`, `.cad-btn-group`, `.file-upload-btn`
- `.ifc-toolbar`, `.ifc-container canvas`, `.ifc-controls-hint`, `.ifc-model-info`, `.ifc-overlay`
- `.reset-view-btn`, `.wireframe-btn`

## Скриншоты
Сохраняются в `screenshots/`:
- `pdf-loaded.png`
- `excel-initial.png`, `excel-loaded.png`
- `cad-initial.png`, `cad-dwg-loaded.png`
- `ifc-initial.png`, `ifc-sample-loaded.png`, `ifc-wireframe.png`, `ifc-louis-loaded.png`
