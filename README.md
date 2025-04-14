# Pact-Tracker

A Python-based Slack bot that helps track and manage your pacts and commitments.

## Features

- Automated tracking of pacts and commitments
- Slack integration for easy updates and notifications
- Report generation capability

## Prerequisites

- Python 3.9
- Slack Workspace with admin privileges
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:

git clone https://github.com/RanaAashish/Pact-Tracker.git
cd pact-tracker

2. Install dependencies:

bash
pip install -r requirements.txt

3. Create a `.env` file in the root directory with your Slack credentials:

bash
SLACK_BOT_TOKEN=your_bot_token
SLACK_APP_TOKEN=your_app_token

## Usage

1. Start the Slack bot:

bash
python slack_bot.py

2. Add the bot to your Slack workspace and invite it to channels where you want to track pacts.

## Commands

- `/start`: Initialize the pact tracking system

## Configuration

- Edit the `slack_bot.py` file to customize the bot's behavior.
- Configure the `.env` file with your Slack credentials.

## Reporting

- The bot generates a monthly report in the `monthly_report.txt` file.
- You can customize the report generation in the `generate_report.py` file.
