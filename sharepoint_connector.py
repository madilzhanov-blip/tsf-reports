# -*- coding: utf-8 -*-
import msal
import requests
import json
from datetime import datetime

class SharePointConnector:
    def __init__(self, tenant_id, client_id, client_secret, site_url):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.site_url = site_url
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        
    def get_access_token(self):
        """Getting access token for Microsoft Graph"""
        try:
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret
            )
            
            scopes = ["https://graph.microsoft.com/.default"]
            result = app.acquire_token_for_client(scopes=scopes)
            
            if "access_token" in result:
                print("✅ Token received successfully")
                return result['access_token']
            else:
                print(f"❌ Token error: {result.get('error_description')}")
                return None
                
        except Exception as e:
            print(f"❌ Authorization error: {str(e)}")
            return None
    
    def test_connection(self):
        """Testing SharePoint connection"""
        print("🔄 Testing SharePoint connection...")
        
        token = self.get_access_token()
        if not token:
            return False, "Could not get token"
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            url = f"https://graph.microsoft.com/v1.0/sites/{self.site_url}"
            
            print(f"🌐 Request to: {url}")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                site_info = response.json()
                site_name = site_info.get('displayName', 'Unknown')
                print(f"✅ Connection successful! Site: {site_name}")
                return True, f"Connection successful! Site: {site_name}"
            else:
                print(f"❌ Connection error: {response.status_code}")
                print(f"Response: {response.text}")
                return False, f"Connection error: {response.status_code}"
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False, f"Error: {str(e)}"
    
    def upload_file(self, folder_path, filename, file_data):
        """Upload file to SharePoint"""
        token = self.get_access_token()
        if not token:
            return False, "Authorization error"
        
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/octet-stream'
            }
            
            url = f"https://graph.microsoft.com/v1.0/sites/{self.site_url}/drive/root:/{folder_path}/{filename}:/content"
            
            response = requests.put(url, headers=headers, data=file_data)
            
            if response.status_code in [200, 201]:
                return True, "File uploaded successfully"
            else:
                return False, f"Upload error: {response.status_code}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"

def test_libraries():
    """Test libraries without SharePoint connection"""
    print("📚 Testing libraries...")
    
    try:
        import msal
        print("✅ MSAL imported")
        
        import requests
        print("✅ Requests imported")
        
        # Test MSAL app creation with dummy data
        try:
            app = msal.ConfidentialClientApplication(
                "test-client-id",
                authority="https://login.microsoftonline.com/test-tenant",
                client_credential="test-secret"
            )
            print("✅ MSAL application created (test)")
        except Exception as e:
            print(f"⚠️ MSAL app creation error: {e}")
        
        print("🎉 All libraries working!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    # Run basic test
    test_libraries()