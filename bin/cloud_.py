import pyrebase
import os
class firebase:
	def __init__(self):
		self.status = "init"
		self.config = {
	  "apiKey": "AIzaSyCF_uoChp-kmasaxHFYSTFnYAbAVFlFZzw",
	  "authDomain": "quasmobile.firebaseapp.com",
	  "databaseURL": "https://quasmobile.firebaseio.com",
	  "projectId": "quasmobile",
	  "storageBucket": "quasmobile.appspot.com",
	  "messagingSenderId": "974611045201",
	  "appId": "1:974611045201:web:4e3274cb45c2c55fa2d170",
	  "measurementId": "G-D9GGE1JM2R"
}
		self.firebase = pyrebase.initialize_app(self.config)
		self.storage = self.firebase.storage()
		#self.auth = self.firebase.auth()
	def upload(self,file_):
		self.storage.child("/resim.png").put(file_)
	def download(self,downloads):
		self.storage.child("/resim.png").download(os.path.join(downloads,"resim.png"))
	#----------------------------------------------AUTH SECTION---------------------------------------------
	def register(self,email,password):
		self.auth.create_user_with_email_and_password(email=email,password=password)
	def sign(self,email,password):
		self.auth.sign_in_with_email_and_password(email=email,password=password)

class waterbase:
    def __init__(self):
        self.pf = None
        self.status = "okay"
        self.admin_info = ""
        self.version = 0
        self.firebase = None
        self.storage = None
        self.auth = None
    def upload(self, *args,**kwargs):
        return
    def download(self, *args,**kwargs):
        return
    def version_control(self):
        with open(pf.version, "r") as vers:
            self.version = int(vers.readlines()[0].split("=")[-1]) #FETCH VERSION DATA
        return
    def update(self,*args,**kwargs):
        return
    def compile_scripts(self, *args,**kwargs):
        return
    # ----------------------------------------------AUTH SECTION---------------------------------------------
    def register(self,*args,**kwargs):
        return
    def sign(self,*args,**kwargs):
        return
