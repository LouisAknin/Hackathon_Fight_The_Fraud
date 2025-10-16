import re
import pandas as pd 
class SmsAnalyzer:
    def __init__(self):
        # Regex patterns
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.phone_pattern = r'(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'
        self.iban_pattern = r'[A-Z]{2}\d{2}(?:\s*\d{4}){4,7}\s*'
        # New pattern for monetary amounts
        self.amount_pattern = r'(?:(?:\d{1,3}(?:\s*\d{3})*(?:[.,]\d{2})?)|(?:\d+[.,]\d{2}))\s*(?:€|EUR|euros?)?'

    def analyze_sms(self, message: str) -> dict:
        """
        Analyze SMS content for suspicious elements
        Args:
            message (str): The SMS content to analyze
        Returns:
            dict: Dictionary containing analysis results
        """
        return {
            "contains_url": bool(re.search(self.url_pattern, message)),
            "contains_phone": bool(re.search(self.phone_pattern, message)),
            "contains_iban": bool(re.search(self.iban_pattern, message)),
            "contains_amount": bool(re.search(self.amount_pattern, message)),
            "found_urls": re.findall(self.url_pattern, message),
            "found_phones": re.findall(self.phone_pattern, message),
            "found_ibans": re.findall(self.iban_pattern, message),
            "found_amounts": re.findall(self.amount_pattern, message)
        }
    def is_suspicious(self, analysis: dict) -> bool:
        """
        Determine if the SMS is suspicious based on analysis results
        Args:
            analysis (dict): The analysis results from analyze_sms
        Returns:
            bool: True if suspicious, False otherwise
        """
        return any([
            analysis["contains_url"],
            analysis["contains_phone"],
            analysis["contains_iban"],
            analysis["contains_amount"]
        ])

class SmsDatasetAnalyzer:
    def __init__(self, dataset_path: str):
        """
        Initialize the SMS dataset analyzer
        Args:
            dataset_path (str): Path to the CSV file
        """
        self.dataset_path = dataset_path
        
        self.data = pd.read_csv(dataset_path, header=0, low_memory=False)
        
        
        
        
        # Convert text column to string, replacing NaN with empty string
        self.data['text'] = self.data['text'].fillna('').astype(str)
        
        self.analyzer = SmsAnalyzer()
        # Add try-except for analysis
        def safe_analyze(message):
            try:
                return self.analyzer.analyze_sms(message)
            except Exception as e:
                print(f"Error analyzing message: {message[:50]}... Error: {str(e)}")
                return {
                    "contains_url": False,
                    "contains_phone": False,
                    "contains_iban": False,
                    "contains_amount": False,
                    "found_urls": [],
                    "found_phones": [],
                    "found_ibans": [],
                    "found_amounts": []
                }
        
        self.data['analysis'] = self.data['text'].apply(safe_analyze)
        self.data['is_suspicious'] = self.data['analysis'].apply(self.analyzer.is_suspicious)
    
    def dataset(self) -> pd.DataFrame:
        """
        Get the entire dataset with analysis results
        Returns:
            pd.DataFrame: DataFrame containing the dataset and analysis results
        """
        return self.data
    
    def get_suspicious_messages(self) -> pd.DataFrame:
        """
        Get all suspicious messages from the dataset
        Returns:
            pd.DataFrame: DataFrame containing suspicious messages
        """
        return self.data[self.data['is_suspicious']]

def visualisation_dataset(dataset): 
    import matplotlib.pyplot as plt
    import seaborn as sns
    print("Visualizing dataset...")
    print ('label', dataset['label'].value_counts())
    print('label',dataset['URL'].value_counts())
    print('label',dataset['PHONE'].value_counts())
    
# Example usage
if __name__ == "__main__":
    analyzer = SmsAnalyzer()
    
    # Test message
    if False : 
        test_sms = """Bonjour, vérifiez votre compte sur http://mabanque.fr
        Contactez nous au 06 12 34 56 78
        IBAN: FR76 1234 5678 9012 3456 7890 123
        Montant: 1 234,56 €"""
        
        result = analyzer.analyze_sms(test_sms)
        
        print("Analysis results:")
        print( analyzer.is_suspicious(result))
        for key, value in result.items():
            print(f"{key}: {value}")
        test_sms = """Bonjour louis, c'est ulysse."""
        result = analyzer.analyze_sms(test_sms)
        print("Analysis results:")
        print( analyzer.is_suspicious(result))
        for key, value in result.items():
            print(f"{key}: {value}")
    
    if True : 
        print("Running dataset analysis...")
        dataset_analyzer = SmsDatasetAnalyzer("dataset_sms.csv")
        df = dataset_analyzer.dataset()
        visualisation_dataset(df)
        print(f"Spam dans le data set{df['label'].value_counts()}")
        suspicious_messages = dataset_analyzer.get_suspicious_messages()
        print(f"Found {len(suspicious_messages)} suspicious messages out of {len(dataset_analyzer.data)} total messages.")
        


