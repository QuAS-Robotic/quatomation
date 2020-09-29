import os
import sys
import subprocess
packages = ['pyqt5','opencv-python','numpy','matplotlib']
for pack in packages:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pack])
    except:
        print("HATA ! '",pack,"' isimli modül yüklenemedi")
print("done")
#os.system("pip install pyqt5 opencv-python numpy json matplotlib")
