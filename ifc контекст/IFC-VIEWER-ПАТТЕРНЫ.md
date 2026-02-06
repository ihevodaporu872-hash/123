# IFC Viewer (BIM 3D) — Паттерны

## Технологии
- **web-ifc** — парсинг IFC файлов (WASM)
- **Three.js** — 3D-рендеринг
- Локальные WASM файлы в `packages/web-ifc`

## Функциональность
- Загрузка IFC файлов (Industry Foundation Classes — формат BIM)
- 3D-рендеринг зданий и конструкций
- Wireframe режим (toggle)
- Reset View
- Информация о модели: Schema, количество Elements, имя файла
- Overlay при загрузке
- Controls hint (управление камерой)

## Тестовые файлы
- `public/sample.ifc` — маленькая модель (быстрая загрузка)
- `public/louis.ifc` — большая модель (до 120 сек загрузки)

## CSS-селекторы
- `.ifc-toolbar` — панель инструментов
- `.ifc-container canvas` — Three.js canvas
- `.ifc-controls-hint` — подсказка управления
- `.ifc-model-info` — информация о модели (Schema, Elements)
- `.ifc-overlay` — оверлей загрузки (disappears when done)
- `.ifc-error` — ошибка
- `.file-upload-btn` — кнопка загрузки файла
- `.reset-view-btn` — кнопка сброса вида
- `.wireframe-btn` — кнопка wireframe

## Статус
IFC Viewer — наиболее стабильный из всех четырёх вьюверов.
Работал изначально, не требовал исправлений.

## Путь к компоненту
`src/components/IfcViewer/IfcViewer.tsx`
