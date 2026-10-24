/* Copyright (c) 2026 Weblate Community UI contributors.
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Only filters cards already present in the current pagination page.
 */
(() => {
  'use strict';
  document.addEventListener('DOMContentLoaded', () => {
    const field = document.getElementById('community-project-filter');
    const grid = document.getElementById('community-project-grid');
    const status = document.getElementById('community-filter-status');
    if (!field || !grid || !status) return;
    const empty = document.getElementById('community-filter-empty');
    const cards = [...grid.querySelectorAll('.community-project-card')];
    const applyFilter = () => {
      const query = field.value.trim().toLocaleLowerCase();
      let visible = 0;
      for (const card of cards) {
        const matched = card.querySelector('h3')?.textContent.toLocaleLowerCase().includes(query) ?? false;
        card.hidden = !matched;
        if (matched) visible++;
      }
      status.textContent = `${visible} ${field.dataset.countLabel || ''}`;
      if (empty) empty.hidden = visible !== 0;
    };
    field.addEventListener('input', applyFilter);
    applyFilter();
  });
})();
