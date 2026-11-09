export interface Hinweis {
  id: string;
  titel: string;
  text: string;
  sichtbarAb: string;
  sichtbarBis?: string;
}

export const hinweise: Hinweis[] = [
  {
    id: 'telefonstoerung',
    titel: 'Telefonanschluss gestört',
    text:
      'Unser Telefonanschluss funktioniert zurzeit leider nicht. Wir sind deshalb telefonisch nicht erreichbar. Wir bitten um Ihr Verständnis.',
    sichtbarAb: '2026-11-09T00:00:00+01:00'
  },
  {
    id: 'praxisschliessung-september-2026',
    titel: 'Praxis geschlossen',
    text:
      'Am Freitag, 25. September 2026, bleibt unsere Praxis geschlossen. Ab Montag, 28. September, sind wir wieder wie gewohnt für Sie da.',
    sichtbarAb: '2026-09-16T00:00:00+02:00',
    sichtbarBis: '2026-09-28T00:00:00+02:00'
  },
  {
    id: 'praxisschliessung-buss-und-bettag-2026',
    titel: 'Praxis geschlossen',
    text:
      'Am Mittwoch, 18. November 2026, bleibt unsere Praxis wegen Buß- und Bettag geschlossen.',
    sichtbarAb: '2026-11-02T00:00:00+01:00',
    sichtbarBis: '2026-11-19T00:00:00+01:00'
  }
];
