# jina_hack_2020_search_stories

## Screenshots
<img src="/images/logo_hack.png" alt="alt text" width="50" >

<img src="/images/Search_Stories_Chatbot_1.png" alt="alt text" width="600" >
<img src="/images/Search_Stories_Chatbot_2.png" alt="alt text" width="600" >
<img src="/images/jina_box.png" alt="alt text" width="600" >

<img src="/images/jina_ai_code.png" alt="alt text" width="200" >
<img src="/images/search_console.png" alt="alt text" width="200" >


## How to run the projects

### Jina
```bash
cd search_stories
python app.py search
```

### Rasa
```bash
cd rasa
```

Action Server
```bash
python -m rasa run actions 
```

Rasa Core Server
```bash
rasa run -p 5007 --cors "*" --debug
```

### Flask Test Webpage
```bash
cd rasa
python app.py
```

## More details on Jina and Rasa

### Jina

```bash
python3 -m venv env/search_story_env
source env/search_story_env/bin/activate

pip install -U cookiecutter && cookiecutter gh:jina-ai/cookiecutter-jina
```

For the hack Search Stories, how the project was created:

project_name: Search Stories (non-default)
jina_version: 0.5.5
project_slug: search_stories
task_type: nlp (non-default)
index_type: strings (non-default)
public_port: 65482

After running cookiecutter, run:

cd search_stories
ls

```bash
pip install -r requirements.txt
```

kaggle datasets download -d shubchat/1002-short-stories-from-project-guttenberg

General Kaggle Info
To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. Then go to the 'Account' tab of your user profile (https://www.kaggle.com/<username>/account) and select 'Create API Token'. This will trigger the download of kaggle.json, a file containing your API credentials. Place this file in the location ~/.kaggle/kaggle.json (on Windows in the location C:\Users\<Windows-username>\.kaggle\kaggle.json - you can check the exact location, sans drive, with echo %HOMEPATH%). You can define a shell environment variable KAGGLE_CONFIG_DIR to change this location to $KAGGLE_CONFIG_DIR/kaggle.json (on Windows it will be %KAGGLE_CONFIG_DIR%\kaggle.json).


```source ../get_data.sh```

****************

Index and run the App

```python app.py index

Optional:
export $MAX_DOCS=50000

python app.py search```

****************

### Rasa

Creating Rasa project 

```python3 -m venv env/rasa_env
source env/rasa_env/bin/activate
mkdir rasa
cd rasa 

pip install -r requirements.txt

rasa init --no-prompt
rasa train
rasa run -p 5007 --cors "*" --debug
python -m rasa run actions```

Modify the rasa data and action server for integrating with Jina apis


******************

