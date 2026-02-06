# Univer Spreadsheet v0.15.x — Паттерны и подводные камни

## Критические правила

### 1. Используй ТОЛЬКО presets API
```typescript
// ПРАВИЛЬНО ✅
import { createUniver } from '@univerjs/presets';
import { UniverSheetsCorePreset } from '@univerjs/presets/preset-sheets-core';

// НЕПРАВИЛЬНО ❌ (рендерит UI но НЕ canvas)
import { Univer } from '@univerjs/core';
new Univer(); // + registerPlugin + createUnit
```

### 2. Container — СТРОКА (не DOM-элемент)
```typescript
// ПРАВИЛЬНО ✅
UniverSheetsCorePreset({ container: 'my-container-id' })

// НЕПРАВИЛЬНО ❌
UniverSheetsCorePreset({ container: document.getElementById('my-container') })
UniverSheetsCorePreset({ container: ref.current })
```

### 3. createWorkbook() вызывается ОТДЕЛЬНО
```typescript
// ПРАВИЛЬНО ✅
const { univerAPI } = createUniver({ presets: [...] });
univerAPI.createWorkbook(workbookData);

// НЕПРАВИЛЬНО ❌ (передача workbook в createUniver конфиг)
createUniver({ presets: [...], workbook: workbookData });
```

### 4. CSS обязателен
```typescript
import '@univerjs/presets/lib/styles/preset-sheets-core.css';
```

### 5. Локали
```typescript
import { mergeLocales, LocaleType } from '@univerjs/presets';
import sheetsEnUS from '@univerjs/presets/preset-sheets-core/locales/en-US';

createUniver({
  locale: LocaleType.EN_US,
  locales: { [LocaleType.EN_US]: mergeLocales(sheetsEnUS) },
  presets: [...]
});
```

## React-интеграция — избегай DOM-конфликтов

### Проблема
React и Univer оба управляют DOM. При реинициализации (новый файл) — ошибка `removeChild`.

### Решение: Wrapper + Manual Child
```tsx
const wrapperRef = useRef<HTMLDivElement>(null);
const univerContainerRef = useRef<HTMLDivElement | null>(null);

function initializeUniver(data?: IWorkbookData) {
  // 1. Dispose старый instance
  if (univerInstanceRef.current) {
    univerInstanceRef.current.univerAPI.dispose();
  }

  // 2. Удалить старый контейнер ВРУЧНУЮ
  if (univerContainerRef.current?.parentNode) {
    univerContainerRef.current.parentNode.removeChild(univerContainerRef.current);
  }

  // 3. Создать НОВЫЙ div с уникальным ID
  const containerId = `univer-container-${++counter}`;
  const div = document.createElement('div');
  div.id = containerId;
  div.style.width = '100%';
  div.style.height = '100%';
  wrapperRef.current.appendChild(div);
  univerContainerRef.current = div;

  // 4. Инициализировать Univer в новом контейнере
  const { univerAPI } = createUniver({
    presets: [UniverSheetsCorePreset({ container: containerId })],
    ...
  });
  univerAPI.createWorkbook(data || defaultWorkbook);
}

// JSX: wrapper div с React ref, Univer рендерит внутрь
<div ref={wrapperRef} className="excel-container" data-testid="excel-container" />
```

## Конвертация XLSX → Univer

### Зависимости
```typescript
import * as XLSX from 'xlsx';
import { IWorkbookData, ICellData, IObjectMatrixPrimitiveType } from '@univerjs/presets';
```

### Формат IWorkbookData
```typescript
{
  id: 'workbook-imported',
  name: 'Imported Workbook',
  sheetOrder: ['sheet-0', 'sheet-1'],
  sheets: {
    'sheet-0': {
      id: 'sheet-0',
      name: 'Sheet 1',
      rowCount: 100,    // Math.max(range.e.r + 1, 100)
      columnCount: 26,  // Math.max(range.e.c + 1, 26)
      cellData: {
        0: { 0: { v: 'Hello' }, 1: { v: 42 } },
        1: { 0: { v: 'World', f: '=A1' } }
      }
    }
  }
}
```

### Типы ячеек XLSX → Univer
- `cell.t === 'n'` → `{ v: number }`
- `cell.t === 's'` → `{ v: string }`
- `cell.t === 'b'` → `{ v: 0 | 1 }`
- `cell.t === 'd'` → `{ v: cell.w || String(cell.v) }`
- `cell.f` → `{ f: formula }`

## Canvas появляется не мгновенно
- После `createWorkbook()` canvas-элементы появляются через ~2-5 секунд
- В тестах: `page.waitForTimeout(5000)` перед проверкой canvas
