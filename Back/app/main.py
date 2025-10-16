def check_in_db(dict):
    from base_sql import DatabaseManager
    db = DatabaseManager("fraud_detection.db")
    if dict['contains_url']:
        for url in dict['found_urls']:
            if db.check_url_in_db(url):
                return True
    if dict['contains_phone']:
        for phone in dict['found_phones']:
            if db.check_phone_in_db(phone):
                return True
    if dict['contains_iban']:
        for iban in dict['found_ibans']:
            if db.check_iban_in_db(iban):
                return True
    return False
def insert_message(dict):
    from base_sql import DatabaseManager
    db = DatabaseManager("fraud_detection.db")
    if dict['contains_url']:
        for url in dict['found_urls']:
    
            db.insert_url(url)
    if dict['contains_phone']:
        for phone in dict['found_phones']:
            
            db.insert_phone(phone)
    if dict['contains_iban']:
        for iban in dict['found_ibans']:
                db.insert_iban(iban)
from catboost import CatBoostClassifier
class Message_analyzer:
    def __init__(self, message: str):
        self.message = message
        self.explanation_url = ""
        self.explanation_sentiment = ""
    
    def analyse(self): 
        from sms_analyzer import SmsAnalyzer
        from utils.sentiment_detection import sentiment_detection
        from utils.url_detection import url_detection
        #model = CatBoostClassifier()
        analyzer = SmsAnalyzer()
        #model.load_model("catboost.json", format="json")

        if analyzer.is_suspicious(analyzer.analyze_sms(self.message)):
            ##print("Le message est potentiellement frauduleux.")
            label_sentiment_detection , explanation_sentiment = sentiment_detection(self.message) # low | medium | high | critical
            label_url_detection , explanation_url  = url_detection(self.message) # safe" | "unknown" | "weird" | "fraud"
            self.explanation_url = explanation_url
            self.explanation_sentiment = explanation_sentiment
            try:
                #requete base de donnée pour url/iban/phone
                sms_analyse = analyzer.analyze_sms(self.message)
                data_base = check_in_db(sms_analyse)
                x=[ sms_analyse["contains_url"], sms_analyse["contains_iban"], sms_analyse["contains_phone"], sms_analyse["contains_amount"], label_url_detection,label_sentiment_detection,data_base]
            except Exception as e:
                print(f"Erreur lors de la requête à la base de données: {str(e)}")
            if label_sentiment_detection in ["medium" ,"high" , "critical"]  or label_url_detection in ["weird" , "fraud"] or data_base :
            #pred = model.predict([x])
            #if pred[0] == 'spam':
                insert_message(sms_analyse)
                return "spam"
            else : 
                return "ham"
                #créer une fonction pour alerter le client
            
    

        else:
            return "ham"
    def analyse_data_set(self): 
        from sms_analyzer import SmsAnalyzer
        from utils.sentiment_detection import sentiment_detection
        from utils.url_detection import url_detection
        
        analyzer = SmsAnalyzer()
        sms_analyse = analyzer.analyze_sms(self.message)
        if analyzer.is_suspicious(analyzer.analyze_sms(self.message)):
            ##print("Le message est potentiellement frauduleux.")
            label_sentiment_detection , explanation_sentiment = sentiment_detection(self.message) # low | medium | high | critical
            label_url_detection, explanation_url = url_detection(self.message) # safe" | "unknown" | "weird" | "fraud"
            self.explanation_url = explanation_url
            self.explanation_sentiment = explanation_sentiment
            try:
                #requete base de donnée pour url/iban/phone
                
                data_base = check_in_db(sms_analyse)
                
            except Exception as e:
                print(f"Erreur lors de la requête à la base de données: {str(e)}")
            if label_sentiment_detection in ["medium" ,"high" , "critical"]  or label_url_detection in ["weird" , "fraud"] or data_base :
                insert_message(sms_analyse)
                return [ sms_analyse["contains_url"], sms_analyse["contains_iban"], sms_analyse["contains_phone"], sms_analyse["contains_amount"], label_url_detection,label_sentiment_detection,data_base]
                #créer une fonction pour alerter le client
            else : 
                return [ sms_analyse["contains_url"], sms_analyse["contains_iban"], sms_analyse["contains_phone"], sms_analyse["contains_amount"], label_url_detection,label_sentiment_detection,data_base]
            
    

        else:
            return [ sms_analyse["contains_url"], sms_analyse["contains_iban"], sms_analyse["contains_phone"], sms_analyse["contains_amount"], "nothing","nothing",False]
    
       
if __name__ == "__main__":
    from tqdm import tqdm
    from sms_analyzer import SmsDatasetAnalyzer
    import pandas as pd
    dataset = pd.read_csv("dataset_sms.csv", header=0, low_memory=False)
    stat = [['good ham','bad ham','good spam','bad spam'],[0,0,0,0]]
    if False : 
        for index, row in tqdm(dataset.iterrows()):
            analyzer = Message_analyzer(row['text'])
            result = analyzer.analyse()
            if row['label'] == 'ham' and result == 'ham':
                stat[1][0] += 1
            elif row['label'] == 'ham' and result == 'spam':
                stat[1][1] += 1
            elif row['label'] == 'spam' and result == 'spam':
                stat[1][2] += 1
            elif row['label'] == 'spam' and result == 'ham':
                stat[1][3] += 1
            else:
                    print("#print")
        
        import numpy as np
        np.save(stat)
            #print("Analysis result:", result)
    if True :
        df = pd.DataFrame(columns=["id", "url", "iban", "phone", "montant", "url_sentiment","sentiment_detection","data_base","label"])
        for index, row in tqdm(dataset.iterrows()):
            if len(df)<=1000:
                analyzer = Message_analyzer(row['text'])
                result = analyzer.analyse_data_set()
                df.loc[len(df)] = [len(df)] + result + [row['label']]
                print(len(df))
        df.to_csv("dataset_sms_analyzed.csv", index=False)


        
    

