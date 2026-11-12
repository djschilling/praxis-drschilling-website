import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const readPage = (path) => readFileSync(new URL(`../dist/${path}index.html`, import.meta.url), 'utf8');

test('all pages enable Web Vitals while retaining tracker privacy restrictions', () => {
  for (const path of ['', 'impressum/', 'datenschutz/']) {
    const html = readPage(path);
    const trackers = html.match(/<script\b[^>]*src="https:\/\/umami\.davidschilling\.de\/script\.js"[^>]*>/g);
    assert.equal(trackers?.length, 1);
    for (const attribute of ['performance', 'do-not-track', 'exclude-search', 'exclude-hash']) {
      assert.ok(trackers[0].includes(`data-${attribute}="true"`), attribute);
    }
    assert.ok(trackers[0].includes('data-domains="mvz-gomaringen.de,www.mvz-gomaringen.de"'));
  }
});

test('contact events distinguish actions, not treatments, and exclude emergency numbers', () => {
  const links = [...readPage('').matchAll(/<a\b[^>]*>/g)].map(([tag]) => tag);
  const phoneLinks = links.filter((tag) => tag.includes('href="tel:+4970727031"'));
  assert.ok(phoneLinks.length > 0);
  for (const tag of links) {
    const href = tag.match(/href="([^"]+)"/)?.[1];
    const expected = href === 'tel:+4970727031' ? 'kontakt-telefon'
      : href === '#oeffnungszeiten' ? 'kontakt-oeffnungszeiten'
      : href?.startsWith('https://www.google.de/maps/') ? 'kontakt-route' : undefined;
    assert.equal(tag.match(/data-umami-event="([^"]+)"/)?.[1], expected, href);
    assert.doesNotMatch(tag, /data-umami-event-[\w-]+=/, 'No additional event properties');
  }
  assert.ok(links.some((tag) => tag.includes('href="tel:112"')));
  assert.ok(links.some((tag) => tag.includes('data-umami-event="kontakt-route"')));
  assert.ok(links.some((tag) => tag.includes('data-umami-event="kontakt-oeffnungszeiten"')));
});
