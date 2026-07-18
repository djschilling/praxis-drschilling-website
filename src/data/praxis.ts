/** Zentrale Praxisdaten für Meta, Impressum und Datenschutz. */
export const praxis = {
  legalName: 'MVZ Gomaringen der MED-GO e.G.',
  shortName: 'MVZ Gomaringen',
  street: 'Lindenstraße 84/1',
  zip: '72810',
  city: 'Gomaringen',
  phoneDisplay: '07072 / 7031',
  phoneTel: '+4970727031',
  faxDisplay: '07072 / 912690',
  /** Bitte durch die echte Praxis-E-Mail ersetzen (Pflichtangabe Impressum). */
  email: 'info@praxis-dr-schilling.de',
  website: 'https://praxis-dr-schilling.de',
  /** Träger / Anbieter im Sinne des DDG */
  provider: 'MED-GO e.G.',
  /** Bitte um Registergericht und Registernummer ergänzen, sobald bekannt. */
  register: 'Genossenschaftsregister (Angaben bitte ergänzen)',
  responsibleContent: 'Dr. med. Bernd Schilling',
  medicalChamber: 'Landesärztekammer Baden-Württemberg',
  kv: 'Kassenärztliche Vereinigung Baden-Württemberg',
  professionalTitle: 'Arzt / Ärztin',
  professionalRules: [
    'Berufsordnung der Landesärztekammer Baden-Württemberg',
    'Heilberufe-Kammergesetz Baden-Württemberg (HBKG)'
  ]
} as const;
