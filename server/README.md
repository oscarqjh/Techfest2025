## Running the FastAPI server

#### To create a virtual environemnt for the backend, change to backend directory:
```sh 
cd backend
```

#### Create the venv folder:
```sh
# macOS/Linux
python3 -m venv venv  

# Windows
python -m venv venv
To activate venv:
```

#### Activate the venv:
```sh
# macOS/Linux
source venv/bin/activate  

# Windows (CMD)
venv\Scripts\activate  

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

#### Install required dependencies
```sh
pip install -r requirements.txt
```

#### To run the FastAPI server:

```sh
# Method 1
uvicorn main:app --reload

# Method 2
fastapi dev main.py
```
