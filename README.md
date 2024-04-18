---
date: 2024-04-18T15:18:31.715522
author: AutoGPT <info@agpt.co>
---

# Cheese Island

A Cheese inspired game based on monkey island

**Features**

- **Character Customization** Allows players to create and customize their own characters within the game, enhancing personalization and engagement.

- **Puzzle Solving** Involves a variety of puzzles that players need to solve to progress through the game, reflecting the intellectual challenge akin to Monkey Island.

- **Narrative and Dialogue** Delivers a compelling story and interactive dialogues with characters, driving the game's plot and player decisions.

- **Quest Systems** Provides a series of quests or missions that players must complete, often intertwined with the main narrative.

- **Inventory and Crafting System** Allows players to collect items and craft new ones, which are crucial for game progression.

- **Multiplayer Elements** Supports interactions between players such as co-op play, competition, or shared quests, increasing replay value.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Cheese Island'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
