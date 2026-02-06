# PDF Viewer — pdfjs-dist паттерны

## Почему НЕ SimplePDF
- `@simplepdf/react-embed-pdf` загружает iframe с `simplepdf.com`
- Без интернета или если сервис недоступен — не работает
- Кнопка Upload навсегда disabled

## Правильный подход: pdfjs-dist (Mozilla PDF.js)

### Установка
```bash
npm install pdfjs-dist
```

### Инициализация Worker
```typescript
import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();
```

### Загрузка PDF
```typescript
// Из File (upload/drag-drop)
const arrayBuffer = await file.arrayBuffer();
const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

// Из URL
const pdf = await pdfjsLib.getDocument(url).promise;
```

### Рендеринг страницы в canvas
```typescript
const page = await pdf.getPage(pageNumber); // 1-indexed
const viewport = page.getViewport({ scale: zoomLevel });

const canvas = document.createElement('canvas');
canvas.width = viewport.width;
canvas.height = viewport.height;

const context = canvas.getContext('2d');
await page.render({ canvasContext: context, viewport }).promise;
```

### Функции вьювера
- Навигация по страницам (prev/next)
- Зум (zoom in/out с шагом 0.25, range 0.25-5.0)
- Drag & Drop файлов
- Кнопка "Load Test PDF" для демо
- Upload через file input
- Отображение: номер страницы, количество страниц, имя файла

### CSS-классы
- `.pdf-toolbar` — панель управления
- `.pdf-container` — основной контейнер (overflow: auto)
- `.pdf-pages-container` — контейнер страниц
- `.pdf-page` — обёртка одной страницы
- `.pdf-page canvas` — canvas страницы
- `.pdf-page-label` — метка "Page N"
- `.pdf-document-info` — информация о документе
- `.pdf-page-info` — "Page X of Y"
- `.pdf-error` — сообщение об ошибке
- `.pdf-upload-btn` — кнопка загрузки
