# GCPSA

For those that have used the Cryptographic protocol Shapes Analyzer, or may be seeing the tool for the first time, the tedium of message matching takes longer than expected.  The goal of this tool is to assist in the creation of protocol specification. 

GCPSA eases the learning curve and provides quality of life features.  This is not a replacement for the base version of CPSA.  GCPSA is an application that acts as a top level controller of CPSA.  

In its current state, GCPSA offers the following features:

- Automatic project directory initialization
- Customizable herald definition
- Automatic role definitions for as many parties as you need
- Automatic message assignment for senders


### Building the Application

Run `pip3 install -r requirements.txt` to make sure your Python environment has everything to install GCPSA.  Once everything is ready, run the included `build.py` file to build GCPSA.  The app will work on any UNIX based OS, as well as Windows.  Note: the application will not function unless a valid CPSA installation is installed on your system.

### Next Steps

Future updates and patches will aim to provide additional functionality, such as security assumption declaration settings and variable recognition.
