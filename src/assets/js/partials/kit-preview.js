/**
 * Moment live kit preview.
 * Mirrors the product's name/number text options onto the shirt-back preview
 * while the customer types. Option ids come from data attributes set in
 * pages/product/single.twig.
 */
const MAX_NAME = 14;
const MAX_NUMBER = 2;

function findInput(form, optionId) {
  if (!optionId) return null;
  return form.querySelector(`[name="options[${optionId}]"]`);
}

function clean(value, kind) {
  const text = String(value || '').trim();
  if (kind === 'number') {
    return text.replace(/[^\d٠-٩]/g, '').slice(0, MAX_NUMBER);
  }
  return text.slice(0, MAX_NAME);
}

export function initKitPreview(root = document) {
  const kit = root.querySelector('[data-m-kit]');
  if (!kit) return;

  const form = kit.closest('form') || document.querySelector('.product-form');
  const nameEl = kit.querySelector('[data-kit-name]');
  const numberEl = kit.querySelector('[data-kit-number]');
  if (!form || !nameEl || !numberEl) return;

  const defaults = { name: nameEl.textContent, number: numberEl.textContent };
  const ids = { name: kit.dataset.nameOption, number: kit.dataset.numberOption };

  const render = () => {
    const nameInput = findInput(form, ids.name);
    const numberInput = findInput(form, ids.number);
    const name = clean(nameInput?.value, 'name');
    const number = clean(numberInput?.value, 'number');
    nameEl.textContent = name || defaults.name;
    numberEl.textContent = number || defaults.number;
    kit.classList.toggle('is-filled', Boolean(name || number));
    // shrink long names so they stay on the shirt
    nameEl.style.setProperty('--m-name-scale', name.length > 9 ? String(9 / name.length) : '1');
  };

  // salla-product-options renders asynchronously; listen on the form instead of the inputs
  form.addEventListener('input', event => {
    const target = event.target;
    if (!target || !target.name) return;
    if (target.name === `options[${ids.name}]` || target.name === `options[${ids.number}]`) render();
  });
  form.addEventListener('change', render);
  render();
}
