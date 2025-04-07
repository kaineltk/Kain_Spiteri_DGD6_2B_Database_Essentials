# Kain_Spiteri_DGD6_2B_Database_Essentials
 A repository for my home assignment for Database Essentials

Setup:
Install VSCode
Install latest python version and Setup Environment Variables

Navigate to Repository Location in VSCode Command Prompt and then run the following commands
python -m venv env
env\Scripts\activate
pip install fastapi
pip install uvicorn
pip install motor
pip install pydantic
pip install python-dotenv
pip install requests
pip install python-multipart
pip freeze > requirements.txt

Then create a main.py file outside of the env folder

Then to launch the application run 
uvicorn main:app --reload

