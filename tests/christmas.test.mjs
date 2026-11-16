import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import test from 'node:test';

test('Christmas hat follows Advent and Epiphany in Berlin, independent of the build date', () => {
  for (const page of ['', 'impressum/', 'datenschutz/']) {
    const html = readFileSync(new URL(`../dist/${page}index.html`, import.meta.url), 'utf8');
    const script = html.match(/<script\b[^>]*data-christmas-script[^>]*>([\s\S]*?)<\/script>/)?.[1];
    assert.ok(script, `Christmas behaviour on /${page}`);
    for (const [instant, visible] of [
      ['2026-11-28T22:59:59Z', false],
      ['2026-11-28T23:00:00Z', true], // First Advent: November 29 in Berlin.
      ['2026-12-26T12:00:00Z', true],
      ['2027-01-06T22:59:59Z', true],
      ['2027-01-06T23:00:00Z', false],
      ['2027-07-01T12:00:00Z', false],
      ['2022-11-26T23:00:00Z', true], // Christmas falls on a Sunday.
      ['2023-12-01T23:00:00Z', false], // Latest possible first Advent: December 3.
      ['2023-12-02T23:00:00Z', true]
    ]) {
      const hat = { hidden: true, setAttribute() {}, addEventListener() {} };
      class Clock extends Date {
        constructor(...args) { super(...(args.length ? args : [instant])); }
      }
      runInNewContext(script, {
        Date: Clock,
        URLSearchParams,
        document: { querySelector: () => hat, addEventListener() {} },
        window: { location: { search: '' }, matchMedia: () => ({ matches: false, addEventListener() {} }) }
      });
      assert.equal(!hat.hidden, visible, `${page} at ${instant}`);
    }
  }
});

test('christmas=1 simulates Advent with snow only after clicking, respecting reduced motion', () => {
  const html = readFileSync(new URL('../dist/index.html', import.meta.url), 'utf8');
  const script = html.match(/<script\b[^>]*data-christmas-script[^>]*>([\s\S]*?)<\/script>/)[1];
  class Element extends EventTarget {
    hidden = true;
    children = [];
    attributes = {};
    style = {};
    setAttribute(name, value) { this.attributes[name] = value; }
    append(child) { this.children.push(child); child.parent = this; }
    remove() { this.parent.children = this.parent.children.filter((child) => child !== this); }
    click() { this.dispatchEvent(new Event('click')); }
  }
  class Clock extends Date {
    constructor(...args) { super(...(args.length ? args : ['2026-07-01T12:00:00Z'])); }
  }
  for (const [search, reduced, visible] of [
    ['?christmas=1', false, true],
    ['?other=value&christmas=1', false, true],
    ['?christmas=1', true, true],
    ['?christmas=0', false, false],
    ['?christmas', false, false],
    ['', false, false]
  ]) {
    const hat = new Element();
    const body = new Element();
    const document = Object.assign(new EventTarget(), {
      body, querySelector: () => hat, createElement: () => new Element()
    });
    runInNewContext(script, {
      Date: Clock, URLSearchParams, document,
      window: {
        location: { search },
        matchMedia: () => ({ matches: reduced, addEventListener() {} })
      }
    });
    assert.equal(!hat.hidden, visible, search);
    assert.equal(body.children.length, 0, 'Snow never starts automatically');
    if (visible) {
      assert.equal(hat.attributes['aria-pressed'], 'false');
      hat.click();
      assert.equal(body.children.length > 0, !reduced, 'Click starts snow unless motion is reduced');
    }
    if (visible && !reduced) {
      assert.equal(hat.attributes['aria-pressed'], 'true');
      hat.click();
      assert.equal(body.children.length, 0, 'Preview snow can be stopped by clicking');
      hat.click();
      document.dispatchEvent(Object.assign(new Event('keydown'), { key: 'Escape' }));
      assert.equal(body.children.length, 0, 'Preview snow can be stopped with Escape');
      assert.equal(hat.attributes['aria-pressed'], 'false');
    }
  }
});
