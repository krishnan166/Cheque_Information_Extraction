#!/usr/bin/env python
# coding: utf-8

# In[35]:


from PIL import Image
from io import BytesIO
import cv2
import os
import numpy as np
import pytesseract as pyt
import matplotlib.pyplot as plt
import re
from skimage import data, filters


# In[36]:


pip install pytesseract==0.3.4


# In[37]:


pyt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# In[38]:


folder = "C:\ChequeImages"


# In[39]:


def clean_text(text):
    if text != ' ' or text != '  ' or text != '':
        text = re.sub('[^A-Za-z0-9-/,.() ]+', '', text)
        text = text.strip()
        text = re.sub(r'\s{2,}', ' ', text)

    return text
def find_bank_name(ifsc):
    bank_data = {
        "HDFC": "HDFC Bank",
        "ICIC": "ICICI Bank",
        "SBI": "State Bank of India",
        "PNB": "Punjab National Bank",
        "AXIS": "Axis Bank",
        "BOM": "Bank of Maharashtra",
        "BOI": "Bank of India",
        "UCO": "UCO Bank",
        "UNI": "Union Bank of India",
        "CAN": "Canara Bank",
        "CBI": "Central Bank of India",
        "BOB": "Bank of Baroda",
        "IOB": "Indian Overseas Bank",
        "VIJ": "Vijaya Bank",
        "SYND": "Syndicate Bank",
        "YES": "Yes Bank",
        "IDBI": "IDBI Bank",
        "KVB": "Karur Vysya Bank",
        "DCB": "DCB Bank",
        "DCCB": "District Co-operative Bank",
        "APMC": "Agricultural and Processed Food Products Export Development Authority",
        "BNCB": "Bharatiya Nagar Co-operative Bank",
        "CSCB": "Chaitanya Godavari Grameena Bank",
        "SVCB": "Shri Veershaiv Co-operative Bank",
        "TJSB": "TJSB Sahakari Bank",
        "IBKL": "IDBI Bank Limited",
        "ORBC": "Oriental Bank of Commerce",
        "ANDB": "Andhra Bank",
        "CPNB": "Capital Small Finance Bank",
        "CSB": "Catholic Syrian Bank",
        "DCBL": "Development Credit Bank Limited",
        "ESAF": "ESAF Small Finance Bank",
        "FBKL": "Federal Bank Limited",
        "FINO": "FINO Payments Bank",
        "ICICI": "ICICI Prudential Life Insurance Company Limited",
        "IDFC": "IDFC First Bank",
        "IDFB": "IDFC First Bank",
        "IDIB": "Indian Bank",
        "INGV": "ING Vysya Bank",
        "JKBN": "Jammu & Kashmir Bank",
        "KKBK": "Kotak Mahindra Bank",
        "KBL": "Kotak Mahindra Bank",
        "LAKA": "Lakshmi Vilas Bank",
        "NBL": "Nainital Bank Limited",
        "RBL": "RBL Bank Limited",
        "SBMY": "State Bank of Mysore",
        "UBIN": "Union Bank of India",
        "IDFR" : "IDFC First Bank",
        "CNRD" :"Canara Bank",
        "CNRB" :"Canara Bank",
        "AUBL" : "AU Small Finance Bank",
        "PUNB" : "Punjab National Bank",
        "BKID": "Bank Of India",
        "UTIB" : "Union Bank of India",
        "INDB" : "IndusInd Bank",
        "SBIN" : "State Bank of India"
        # add more bank data here as needed
    }
    bank_prefix = ifsc[:4]
    return bank_data.get(bank_prefix, "Not found")

def max_digit_element(p):
      max_element = None
      max_digit_count = 0

      for element in p:
        digit_count = len(str(element))
        if digit_count > max_digit_count:
          max_element = element
          max_digit_count = digit_count

      return max_element


# In[40]:


count = 0;
for filename in os.listdir(folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image_path = os.path.join(folder, filename)
        image = Image.open(image_path)
        #image.save(image_path, optimize=True)
        count+= 1
        img = cv2.imread(filename)
        if img is None or img.size == 0:
            print(f"Image {filename} : invalid input image")
        else:
            img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(img, (5, 5), 0)
            T, img2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            text = pyt.image_to_string(img, lang="eng")
            #text = clean_text(text)
            Find = "IFSC"
            Search = text.find(Find)
            IFSC = re.sub(r'\b[a-zA-Z]{4}(.){5}\d{2}\b', lambda match: match.group(0).replace('o', '0').replace('O','0'), text)
            if IFSC is None :
                ifsc = 'Not found'
                bank_name = 'Not found'
            else:
                Ifsc = re.search(r"\b[a-zA-Z]{4}(.){5}\d{2}\b", IFSC)
                if Ifsc is not None:
                    ifsc = Ifsc.group(0)
                    bank_name = find_bank_name(ifsc)
                else:
                    ifsc = 'Not found'
                    bank_name = 'Not found'
            print(f"BANK {filename} :",bank_name)
            print(f"IFSC {filename}:",ifsc)
            p = re.findall(r'\d\w*\d{8,}\w*\d', text)
            max_element = 0
            print(f"Account Number {filename}:",max_digit_element(p))


# In[ ]:




