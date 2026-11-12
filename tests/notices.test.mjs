import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { runInNewContext } from 'node:vm';
import { hinweise } from '../src/data/hinweise.ts';

const html = readFileSync(new URL('../dist/index.html', import.meta.url), 'utf8');
const script = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)]
  .map((match) => match[1]).find((source) => source.includes("'[data-hinweise]'"));
assert.ok(script, 'Built page must include notice filtering');

// Execute the shipped script with a controllable clock and minimal DOM.
function notices(start, ranges) {
  let now = Date.parse(start);
  let nextId = 0;
  const timers = new Map();
  const window = new EventTarget();
  const document = new EventTarget();
  const items = ranges.map(([from, until]) => ({
    hidden: false,
    getAttribute: (name) => name === 'data-sichtbar-ab' ? from : until,
    toggleAttribute(name, hidden) { this.hidden = hidden; }
  }));
  const section = {
    hidden: false,
    querySelectorAll: () => items,
    toggleAttribute(name, hidden) { this.hidden = hidden; }
  };
  document.querySelector = () => section;
  runInNewContext(script, {
    window, document,
    Date: class extends Date { static now() { return now; } },
    setTimeout(callback, delay) {
      const id = ++nextId;
      timers.set(id, { callback, due: now + delay });
      return id;
    },
    clearTimeout: (id) => timers.delete(id)
  });
  return {
    visible: () => items.map((item) => !section.hidden && !item.hidden),
    advance(time, event) {
      const target = Date.parse(time);
      if (event) {
        now = target; // A suspended tab skips timers until it resumes.
        (event === 'visibilitychange' ? document : window).dispatchEvent(new Event(event));
      } else {
        let count = 0;
        while (true) {
          const next = [...timers].sort((a, b) => a[1].due - b[1].due)[0];
          if (!next || next[1].due > target) break;
          assert.ok(++count < 100, 'Timer must not spin or overflow');
          now = next[1].due;
          timers.delete(next[0]);
          next[1].callback();
        }
        now = target;
      }
    }
  };
}

test('notices start inclusively and expire exclusively in an already-open tab', () => {
  const page = notices('2026-11-01T22:59:59Z', [
    ['2026-11-02T00:00:00+01:00', '2026-11-02T00:02:00+01:00'],
    ['2026-11-02T00:01:00+01:00', '2026-11-02T00:03:00+01:00']
  ]);
  assert.deepEqual(page.visible(), [false, false]);
  for (const [time, expected] of [
    ['23:00:00', [true, false]], ['23:00:59.999', [true, false]],
    ['23:01:00', [true, true]], ['23:02:00', [false, true]],
    ['23:03:00', [false, false]]
  ]) {
    page.advance(`2026-11-01T${time}Z`);
    assert.deepEqual(page.visible(), expected);
  }
});

test('suspended/restored tabs and clock corrections refresh without a reload', () => {
  for (const event of ['focus', 'pageshow', 'visibilitychange']) {
    const page = notices('2026-10-01T00:00:00Z', [
      ['2026-10-25T02:30:00+02:00', '2026-10-25T02:30:00+01:00']
    ]);
    page.advance('2026-10-25T00:30:00Z', event);
    assert.deepEqual(page.visible(), [true]);
    page.advance('2026-10-25T01:30:00Z', event);
    assert.deepEqual(page.visible(), [false]);
    page.advance('2026-10-25T00:45:00Z', event);
    assert.deepEqual(page.visible(), [true]);
  }
});

test('no-JavaScript output explains filtering and leaves dated notices readable', () => {
  const section = html.match(/<section\b[^>]*data-hinweise[^>]*>[\s\S]*?<\/section>/)[0];
  assert.match(section, /<noscript>[\s\S]*Ohne JavaScript/);
  if (hinweise.length) assert.doesNotMatch(section, /\shidden(?:[\s=>])/);
  assert.equal([...section.matchAll(/<article\b/g)].length, hinweise.length);
});
