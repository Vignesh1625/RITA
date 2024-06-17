import tkinter as tk
from AppOpener import open, close

class ResponseGPT:
    def open_applications(self,query):
        try:
            open(query,match_closest=True,output=False)
            return "Opening " + query
        except Exception as e :
            return "ERROR "+str(e)
    
    def close_applications(self,query):
        try:
            close(query,match_closest=True,output=False)
            return "closeing " + query
        except Exception as e :
            return "ERROR "+str(e)
        
    
        
class RitaGPT:
