# LLTrainer
A speedcubing web application that helps cubers train last layer algorithms

## Demo

<img src="https://github.com/TN0123/LLTrainer/blob/main/LLTrainerDemo.gif" alt="demo"/>

## Current Features
- Timing and storing of solves
- Deletion of individual times
- Clearing of a session
- Scrambles for PLL cases
- Ranking of fastest times per algorithm

## Installation
1. Clone the Repository
   ```sh
   git clone https://github.com/TN0123/LLTrainer.git
   ```
2. Install Dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Set up database, typing these commands into the python interactive interpreter from the terminal
   ```sh
   from app import app, db
   app.app_context().push()
   db.create_all()
   ```
## Usage
Run the following command in the terminal to start the app 
```sh
python app.py
```
