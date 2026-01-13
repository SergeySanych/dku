
(() => {
  function pickMainEl(inner) {
    // Берём первый элемент (не текст) — обычно это iframe или div виджета
    return inner.firstElementChild;
  }

  function applyScale(container) {
    const targetH = parseFloat(container.dataset.targetH || "200");
    const inner = container.querySelector(".embed-fit__inner");
    if (!inner) return;

    const el = pickMainEl(inner);
    if (!el) return;

    // Сброс перед измерением (чтобы не мерить уже масштабированное)
    inner.style.transform = "none";

    // Иногда элемент ещё "0x0" (виджет не отрисовался) — тогда повторим позже
    const rect = el.getBoundingClientRect();
    const h = rect.height;
    const w = rect.width;

    if (!h || h < 2 || !w || w < 2) {
      requestAnimationFrame(() => applyScale(container));
      return;
    }

    const scale = targetH / h;

    inner.style.transform = `scale(${scale})`;
    container.style.height = `${targetH}px`;

    // Не обязательно, но удобно: контейнер по ширине станет пропорционален
    // (если контейнер в сетке/колонке — можно эту строку убрать)
    container.style.width = `${w * scale}px`;
  }

  function watch(container) {
    const inner = container.querySelector(".embed-fit__inner");
    if (!inner) return;

    // Пересчитываем при мутациях (скрипты часто добавляют DOM после вставки)
    const mo = new MutationObserver(() => applyScale(container));
    mo.observe(inner, { childList: true, subtree: true });

    // Пересчитываем при изменении размеров (виджет может менять высоту)
    const ro = new ResizeObserver(() => applyScale(container));
    ro.observe(inner);

    // Отдельно для iframe: пересчёт после load
    inner.addEventListener("load", (e) => {
      if (e.target && e.target.tagName === "IFRAME") applyScale(container);
    }, true);

    // Первый запуск
    applyScale(container);

    // И ещё один "контрольный" чуть позже (часто помогает с ленивыми виджетами)
    setTimeout(() => applyScale(container), 400);
    setTimeout(() => applyScale(container), 1200);
  }

  function init() {
    document.querySelectorAll(".embed-fit").forEach(watch);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
