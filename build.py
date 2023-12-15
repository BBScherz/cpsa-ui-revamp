import subprocess

def main():
    builder = ['pyinstaller', '--onefile', '--icon=assets\icon.ico', '--windowed', '--clean', '--noconsole', '--name', 'GCPSA', 'app.py']
    try:
        subprocess.run(builder)
    except:
        print('Build failed!')

if __name__ == '__main__':
    main()
