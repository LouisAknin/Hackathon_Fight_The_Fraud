import sqlite3
import re
from typing import List, Tuple, Optional
from contextlib import contextmanager

class DataValidator:
    """Classe pour valider les IBAN, URL et numéros de téléphone"""
    
    @staticmethod
    def valider_iban(iban: str) -> bool:
        """Valide un IBAN (format basique)"""
        iban = iban.replace(" ", "").upper()
        pattern = r'^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$'
        return bool(re.match(pattern, iban)) and len(iban) >= 15
    
    @staticmethod
    def valider_url(url: str) -> bool:
        """Valide une URL"""
        pattern = r'^http[s]?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def valider_telephone(telephone: str) -> bool:
        """Valide un numéro de téléphone"""
        telephone_clean = re.sub(r'[\s\-\.]', '', telephone)
        pattern = r'^\+?[0-9]{8,15}$'
        return bool(re.match(pattern, telephone_clean))
    
    @staticmethod
    def formater_iban(iban: str) -> str:
        """Formate un IBAN"""
        return iban.replace(" ", "").upper()
    
    @staticmethod
    def format_phone(telephone: str) -> str:
        """Formate un numéro de téléphone"""
        return re.sub(r'[\s\-\.]', '', telephone)


class DatabaseManager:
    """Classe pour gérer la base de données avec 3 tables : IBAN, URL, Téléphones"""
    
    def __init__(self, db_path: str = "ma_base.db"):
        self.db_path = db_path
        self.validator = DataValidator()
        self._initialiser_base()
    
    @contextmanager
    def get_connection(self):
        """Context manager pour gérer automatiquement les connexions"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _initialiser_base(self):
        """Initialise la structure de la base de données avec 3 tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # TABLE 1 : IBAN
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ibans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    iban TEXT NOT NULL UNIQUE,
                    nom_titulaire TEXT,
                    nom_banque TEXT,
                    pays TEXT,
                    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # TABLE 2 : URLs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    titre TEXT,
                    description TEXT,
                    categorie TEXT,
                    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # TABLE 3 : Téléphones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telephones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT NOT NULL UNIQUE,
                    type TEXT,
                    pays TEXT,
                    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            #print("✓ Base de données initialisée avec 3 tables")
    
    # ========== GESTION DES IBAN ==========
    
    def insert_iban(self, iban: str, nom_titulaire: str = None, 
                     nom_banque: str = None, pays: str = None) -> int:
        """Ajoute un IBAN dans la table ibans"""
        iban_formate = self.validator.formater_iban(iban)
        
        if not self.validator.valider_iban(iban_formate):
            raise ValueError(f"IBAN invalide: {iban}")
        
        query = "INSERT INTO ibans (iban, nom_titulaire, nom_banque, pays) VALUES (?, ?, ?, ?)"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (iban_formate, nom_titulaire, nom_banque, pays))
                iban_id = cursor.lastrowid
                #print(f"✓ IBAN ajouté avec l'ID: {iban_id}")
                return iban_id
            except sqlite3.IntegrityError:
                print(f"⚠ IBAN déjà existant: {iban_formate}")
                return None
    
    def lister_ibans(self) -> List[Tuple]:
        """Liste tous les IBAN"""
        query = "SELECT * FROM ibans ORDER BY date_ajout DESC"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    
    def rechercher_iban(self, iban: str) -> Optional[Tuple]:
        """Recherche un IBAN spécifique"""
        iban_formate = self.validator.formater_iban(iban)
        query = "SELECT * FROM ibans WHERE iban = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (iban_formate,))
            return cursor.fetchone()
    
    def supprimer_iban(self, iban_id: int) -> bool:
        """Supprime un IBAN par son ID"""
        query = "DELETE FROM ibans WHERE id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (iban_id,))
            if cursor.rowcount > 0:
                #print(f"✓ IBAN {iban_id} supprimé")
                return True
            return False
    
    # ========== GESTION DES URLs ==========
    
    def insert_url(self, url: str, titre: str = None, 
                    description: str = None, categorie: str = None) -> int:
        """Ajoute une URL dans la table urls"""
        if not self.validator.valider_url(url):
            raise ValueError(f"URL invalide: {url}")
        
        query = "INSERT INTO urls (url, titre, description, categorie) VALUES (?, ?, ?, ?)"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (url, titre, description, categorie))
                url_id = cursor.lastrowid
                #print(f"✓ URL ajoutée avec l'ID: {url_id}")
                return url_id
            except sqlite3.IntegrityError:
                print(f"⚠ URL déjà existante: {url}")
                return None
    
    def list_urls(self, categorie: str = None) -> List[Tuple]:
        """Liste toutes les URLs (optionnellement filtrées par catégorie)"""
        if categorie:
            query = "SELECT * FROM urls WHERE categorie = ? ORDER BY date_ajout DESC"
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (categorie,))
                return cursor.fetchall()
        else:
            query = "SELECT * FROM urls ORDER BY date_ajout DESC"
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
    
    def check_url_in_db(self, url: str) -> Optional[Tuple]:
        """Recherche une URL spécifique"""
        query = "SELECT * FROM urls WHERE url = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (url,))
            return cursor.fetchone()
    
    def delete_url(self, url_id: int) -> bool:
        """Supprime une URL par son ID"""
        query = "DELETE FROM urls WHERE id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (url_id,))
            if cursor.rowcount > 0:
                #print(f"✓ URL {url_id} supprimée")
                return True
            return False
    
    # ========== GESTION DES TÉLÉPHONES ==========
    
    def insert_phone(self, numero: str, nom_proprietaire: str = None,
                          type_tel: str = None, pays: str = None) -> int:
        """Ajoute un numéro de téléphone dans la table telephones"""
        numero_formate = self.validator.format_phone(numero)
        
        if not self.validator.valider_telephone(numero_formate):
            raise ValueError(f"Numéro de téléphone invalide: {numero}")
        
        query = "INSERT INTO telephones (numero, type, pays) VALUES (?, ?, ?)"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (numero_formate, type_tel, pays))
                tel_id = cursor.lastrowid
                #print(f"✓ Téléphone ajouté avec l'ID: {tel_id}")
                return tel_id
            except sqlite3.IntegrityError:
                print(f"⚠ Numéro déjà existant: {numero_formate}")
                return None
    
    def lister_telephones(self) -> List[Tuple]:
        """Liste tous les numéros de téléphone"""
        query = "SELECT * FROM telephones ORDER BY date_ajout DESC"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
    
    def check_phone_in_db(self, numero: str) -> Optional[Tuple]:
        """Recherche un numéro de téléphone spécifique"""
        numero_formate = self.validator.format_phone(numero)
        query = "SELECT * FROM telephones WHERE numero = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (numero_formate,))
            return cursor.fetchone()
    
    def delete_telephone(self, tel_id: int) -> bool:
        """Supprime un téléphone par son ID"""
        query = "DELETE FROM telephones WHERE id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tel_id,))
            if cursor.rowcount > 0:
                #print(f"✓ Téléphone {tel_id} supprimé")
                return True
            return False
    
    
    # ========== STATISTIQUES ==========
    
    def obtenir_statistiques(self) -> dict:
        """Retourne les statistiques de la base de données"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM ibans")
            nb_ibans = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM urls")
            nb_urls = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM telephones")
            nb_telephones = cursor.fetchone()[0]
            
            return {
                "ibans": nb_ibans,
                "urls": nb_urls,
                "telephones": nb_telephones,
                "total": nb_ibans + nb_urls + nb_telephones
            }


""" # ========== EXEMPLE D'UTILISATION ==========
if False:
    def exemple_utilisation():
        Démontre l'utilisation de la base de données
        
        db = DatabaseManager("ma_base.db")
        
        #print("\n" + "="*60)
        #print("=== AJOUT D'IBAN ===")
        #print("="*60)
        db.ajouter_iban("FR76 3000 6000 0112 3456 7890 189", "Marie Dupont", "Banque Populaire", "France")
        db.ajouter_iban("DE89 3704 0044 0532 0130 00", "Pierre Martin", "Deutsche Bank", "Allemagne")
        db.ajouter_iban("ES91 2100 0418 4502 0005 1332", "Sophie Bernard", "Banco Santander", "Espagne")
        db.ajouter_iban("IT60 X054 2811 1010 0000 0123 456", "Luca Rossi", "Intesa Sanpaolo", "Italie")
        
        #print("\n" + "="*60)
        #print("=== AJOUT D'URLS ===")
        #print("="*60)
        db.ajouter_url("https://www.github.com/mariedupont", "GitHub Marie", "Profil GitHub", "professionnel")
        db.ajouter_url("https://www.linkedin.com/in/pierremartin", "LinkedIn Pierre", "Profil LinkedIn", "professionnel")
        db.ajouter_url("https://www.example.com", "Site exemple", "Site de test", "test")
        db.ajouter_url("https://www.mon-blog.fr", "Mon Blog", "Blog personnel", "personnel")
        
        #print("\n" + "="*60)
        #print("=== AJOUT DE TÉLÉPHONES ===")
        #print("="*60)
        db.ajouter_telephone("+33 6 12 34 56 78", "Marie Dupont", "mobile", "France")
        db.ajouter_telephone("+49 151 12345678", "Pierre Martin", "mobile", "Allemagne")
        db.ajouter_telephone("+34 612 34 56 78", "Sophie Bernard", "mobile", "Espagne")
        db.ajouter_telephone("01 23 45 67 89", "Bureau Paris", "fixe", "France")
        
        #print("\n" + "="*60)
        #print("=== LISTE DE TOUS LES IBAN ===")
        #print("="*60)
        ibans = db.lister_ibans()
        for iban in ibans:
            #print(f"ID: {iban[0]} | IBAN: {iban[1]} | Titulaire: {iban[2]} | Banque: {iban[3]} | Pays: {iban[4]}")
        
        #print("\n" + "="*60)
        #print("=== LISTE DE TOUTES LES URLS ===")
        #print("="*60)
        urls = db.lister_urls()
        for url in urls:
            #print(f"ID: {url[0]} | URL: {url[1]} | Titre: {url[2]} | Catégorie: {url[4]}")
        
        #print("\n" + "="*60)
        #print("=== LISTE DE TOUS LES TÉLÉPHONES ===")
        #print("="*60)
        telephones = db.lister_telephones()
        for tel in telephones:
            #print(f"ID: {tel[0]} | Numéro: {tel[1]} | Propriétaire: {tel[2]} | Type: {tel[3]} | Pays: {tel[4]}")
        
        #print("\n" + "="*60)
        #print("=== RECHERCHE D'UN IBAN SPÉCIFIQUE ===")
        #print("="*60)
        iban_trouve = db.rechercher_iban("FR76 3000 6000 0112 3456 7890 189")
        if iban_trouve:
            #print(f"IBAN trouvé: {iban_trouve[1]} - Titulaire: {iban_trouve[2]}")
        
        #print("\n" + "="*60)
        #print("=== RECHERCHE D'UNE URL SPÉCIFIQUE ===")
        #print("="*60)
        url_trouve = db.rechercher_url("https://www.github.com/mariedupont")
        if url_trouve:
            #print(f"URL trouvée: {url_trouve[1]} - Titre: {url_trouve[2]}")
        
        #print("\n" + "="*60)
        #print("=== RECHERCHE D'UN TÉLÉPHONE SPÉCIFIQUE ===")
        #print("="*60)
        tel_trouve = db.rechercher_telephone("+33612345678")
        if tel_trouve:
            #print(f"Téléphone trouvé: {tel_trouve[1]} - Propriétaire: {tel_trouve[2]}")
        
        #print("\n" + "="*60)
        #print("=== STATISTIQUES DE LA BASE ===")
        #print("="*60)
        stats = db.obtenir_statistiques()
        #print(f"Nombre d'IBAN: {stats['ibans']}")
        #print(f"Nombre d'URLs: {stats['urls']}")
        #print(f"Nombre de téléphones: {stats['telephones']}")
        #print(f"Total d'enregistrements: {stats['total']}")
"""