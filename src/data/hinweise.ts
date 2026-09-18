export interface Hinweis {
  id: string;
  titel: string;
  text: string;
  sichtbarAb: string;
  sichtbarBis: string;
}

export const hinweise: Hinweis[] = [
  {
    id: 'praxisschliessung-september-2026',
    titel: 'Praxis geschlossen',
    text:
      'Am Freitag, 25. September 2026, bleibt unsere Praxis geschlossen. Am Donnerstag, 24. September, und ab Montag, 28. September, sind wir wie gewohnt für Sie da.',
    sichtbarAb: '2026-09-16T00:00:00+02:00',
    sichtbarBis: '2026-09-28T00:00:00+02:00'
  }
];
