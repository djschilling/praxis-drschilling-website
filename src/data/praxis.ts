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
  website: 'https://praxis-dr-schilling.de',
  /** Träger / Anbieter im Sinne des DDG */
  provider: 'MED-GO e.G.',
  legalForm: 'eingetragene Genossenschaft (e.G.)',
  seat: 'Gomaringen',
  registerCourt: 'Amtsgericht Stuttgart',
  registerNumber: 'GnR 720231',
  vatExemptNote:
    'Die ärztlichen Leistungen sind gemäß § 4 Nr. 14 UStG von der Umsatzsteuer befreit. Eine Umsatzsteuer-Identifikationsnummer wird daher nicht geführt.',
  responsibleContent: 'Dr. med. univ. Bernd Schilling',
  medicalChamber: {
    name: 'Landesärztekammer Baden-Württemberg',
    street: 'Jahnstraße 40',
    zipCity: '70597 Stuttgart',
    websiteHref: 'https://www.aerztekammer-bw.de',
    websiteLabel: 'www.aerztekammer-bw.de'
  },
  districtChamber: {
    name: 'Bezirksärztekammer Südwürttemberg',
    street: 'Haldenhaustraße 11',
    zipCity: '72770 Reutlingen-Betzingen',
    phoneDisplay: '07121 / 9170',
    phoneTel: '+4971219170',
    websiteHref: 'https://www.aerztekammer-bw.de/baek-sw',
    websiteLabel: 'www.aerztekammer-bw.de'
  },
  kv: 'Kassenärztliche Vereinigung Baden-Württemberg',
  professionalTitle: 'Arzt / Ärztin',
  professionalRules: [
    'Berufsordnung der Landesärztekammer Baden-Württemberg',
    'Heilberufe-Kammergesetz Baden-Württemberg (HBKG)'
  ]
} as const;
