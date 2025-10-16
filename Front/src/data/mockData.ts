export interface Client {
  id: string;
  name: string;
  email: string;
  phone: string;
  branch: string;
  riskScore: number;
  totalAssets: number;
  avatar?: string;
}

export interface Account {
  id: string;
  clientId: string;
  type: string;
  balance: number;
  productName: string;
  accountNumber: string;
}

export interface Transaction {
  id: string;
  clientId: string;
  date: string;
  amount: number;
  type: string;
  merchant: string;
  status: string;
}

export interface FraudData {
  id: string;
  clientId: string;
  scammerNumber: string;
  messageText: string;
  analysis: string;
  score: number;
  date: string;
  reviewed: boolean;
}

export const mockClients: Client[] = [
  {
    id: "C001",
    name: "Marie Dubois",
    email: "marie.dubois@email.fr",
    phone: "+33 6 12 34 56 78",
    branch: "Paris Opéra",
    riskScore: 0.15,
    totalAssets: 125000,
  },
  {
    id: "C002",
    name: "Jean Martin",
    email: "jean.martin@email.fr",
    phone: "+33 6 23 45 67 89",
    branch: "Lyon Part-Dieu",
    riskScore: 0.82,
    totalAssets: 87500,
  },
  {
    id: "C003",
    name: "Pierre-Elie Laval",
    email: "pe.laval@gmail.com",
    phone: "+33 6 34 56 78 90",
    branch: "Ecully",
    riskScore: 0.45,
    totalAssets: 210000,
  },
  {
    id: "C004",
    name: "Pierre Leroy",
    email: "pierre.leroy@email.fr",
    phone: "+33 6 45 67 89 01",
    branch: "Paris Opéra",
    riskScore: 0.08,
    totalAssets: 450000,
  },
  {
    id: "C005",
    name: "Isabelle Moreau",
    email: "isabelle.moreau@email.fr",
    phone: "+33 6 56 78 90 12",
    branch: "Toulouse Capitole",
    riskScore: 0.92,
    totalAssets: 65000,
  },
];

export const mockAccounts: Account[] = [
  { id: "A001", clientId: "C001", type: "Compte Courant", balance: 12500, productName: "Compte Courant Plus", accountNumber: "FR76 1234 5678 9012 3456 7890 123" },
  { id: "A002", clientId: "C001", type: "Livret A", balance: 22800, productName: "Livret A", accountNumber: "FR76 1234 5678 9012 3456 7890 124" },
  { id: "A003", clientId: "C001", type: "Assurance Vie", balance: 89700, productName: "Patrimoine Avenir", accountNumber: "FR76 1234 5678 9012 3456 7890 125" },
  { id: "A004", clientId: "C002", type: "Compte Courant", balance: 4500, productName: "Compte Courant", accountNumber: "FR76 1234 5678 9012 3456 7890 126" },
  { id: "A005", clientId: "C002", type: "PEL", balance: 83000, productName: "Plan Épargne Logement", accountNumber: "FR76 1234 5678 9012 3456 7890 127" },
  { id: "A006", clientId: "C003", type: "Compte Courant", balance: 28000, productName: "Compte Courant Premium", accountNumber: "FR76 1234 5678 9012 3456 7890 128" },
  { id: "A007", clientId: "C003", type: "PEA", balance: 182000, productName: "Plan Épargne Actions", accountNumber: "FR76 1234 5678 9012 3456 7890 129" },
];

export const mockTransactions: Transaction[] = [
  { id: "T001", clientId: "C001", date: "2025-10-10", amount: -45.50, type: "Débit", merchant: "Carrefour Lyon", status: "Validée" },
  { id: "T002", clientId: "C001", date: "2025-10-09", amount: -120.00, type: "Débit", merchant: "SNCF Voyages", status: "Validée" },
  { id: "T003", clientId: "C001", date: "2025-10-08", amount: 2500.00, type: "Virement", merchant: "Salaire - Entreprise XYZ", status: "Validée" },
  { id: "T004", clientId: "C001", date: "2025-10-07", amount: -89.90, type: "Débit", merchant: "Amazon.fr", status: "Validée" },
  { id: "T005", clientId: "C002", date: "2025-10-10", amount: -15.20, type: "Débit", merchant: "Boulangerie Paul", status: "Validée" },
  { id: "T006", clientId: "C002", date: "2025-10-09", amount: -450.00, type: "Prélèvement", merchant: "EDF Électricité", status: "Validée" },
  { id: "T007", clientId: "C002", date: "2025-10-08", amount: 1800.00, type: "Virement", merchant: "Salaire - Société ABC", status: "Validée" },
];

export const mockFraudData: FraudData[] = [
  {
    id: "F001",
    clientId: "C002",
    scammerNumber: "+33 6 98 76 54 32",
    messageText: "URGENT: Votre compte Crédit Agricole a été suspendu. Cliquez sur ce lien pour le réactiver: http://ca-secure-login.xyz/verify",
    analysis: "Lien suspect détecté • Demande urgente de clic • Domaine non-officiel",
    score: 0.95,
    date: "2025-10-09",
    reviewed: false,
  },
  {
    id: "F002",
    clientId: "C002",
    scammerNumber: "+33 7 12 34 56 78",
    messageText: "Bonjour, votre carte bancaire expire bientôt. Merci de confirmer vos informations ici: http://ca-update.com/card",
    analysis: "Tentative de phishing • Demande d'informations sensibles • URL frauduleuse",
    score: 0.88,
    date: "2025-10-08",
    reviewed: false,
  },
  {
    id: "F003",
    clientId: "C005",
    scammerNumber: "+33 6 45 67 89 12",
    messageText: "Alerte sécurité: Transaction suspecte détectée sur votre compte. Appelez le 01 23 45 67 89 immédiatement.",
    analysis: "Faux numéro de service client • Urgence artificielle • Tentative d'escroquerie vocale",
    score: 0.92,
    date: "2025-10-10",
    reviewed: false,
  },
  {
    id: "F004",
    clientId: "C003",
    scammerNumber: "+33 6 78 90 12 34",
    messageText: "Vous avez gagné 5000€ dans un tirage au sort Crédit Agricole! Réclamez votre prix sur: http://gain-ca.net/claim",
    analysis: "Arnaque au gain fictif • Aucun concours en cours • Domaine suspect",
    score: 0.78,
    date: "2025-10-07",
    reviewed: true,
  },
  {
    id: "F1760280475",
    clientId: "C003",
    scammerNumber: "+33679657851",
    messageText: "Bonjour, le colis ne rentre pas dans la boîte aux lettres, envoyez vos coordonnées bancaires au 0652715735, dans les plus brefs délais.",
    analysis: "Demande de coordonnées bancaires pour un colis est une technique classique de fraude.",
    score: 0.91,
    date: "2025-10-12",
    reviewed: false,
  },
];