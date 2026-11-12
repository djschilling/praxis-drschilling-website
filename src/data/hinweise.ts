export interface Hinweis {
  id: string;
  titel: string;
  text: string;
  sichtbarAb: string;
  sichtbarBis: string;
  geschlossenAm?: string[];
}

export const hinweise: Hinweis[] = [
  {
    id: 'praxisschliessung-buss-und-bettag-2026',
    titel: 'Praxis geschlossen',
    text:
      'Am Mittwoch, 18. November 2026, bleibt unsere Praxis wegen Buß- und Bettag geschlossen.',
    sichtbarAb: '2026-11-02T00:00:00+01:00',
    sichtbarBis: '2026-11-19T00:00:00+01:00',
    geschlossenAm: ['2026-11-18']
  }
];
