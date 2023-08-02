# rp_chatbot

A lightweight role-playing chatbot powered by OpenAI's GPT, using the Gradio interface.

## Features

* **Conversational AI:** Uses OpenAI's GPT chat models to generate human-like text based on the user's input and the ongoing conversation.
* **Role Playing:** Allows the user to interact with different characters. Each character has a set of predefined prompts, describing their personality, and scenarios.
* **History Management:** Maintains conversation history and ensures it doesn't exceed the model's maximum token limit.
* **Error Handling:** Provides basic error handling and logging for API calls and user interactions.

## Setup & Installation

1. Make sure you have Python 3.7 or higher installed.

2. Clone this repository:

```
git clone https://github.com/petersonpp/rp_chatbot.git
```

3. Install the necessary packages:

```
pip install -r requirements.txt
```

4. Update the **.env** file in the root directory with your OpenAI API key, your organization ID (if you are using one) and the name of the model you will be using:

```
OPENAI_API_KEY=foo # your openai API key
YOUR_ORG_ID=foo # your organization ID
OPENAI_MODEL=gpt-3.5-turbo # the model name as provided in the openai api documentation
```

5. Run the chatbot:

```
python rp_chatbot.py
```

## Usage
**IMPORTANT: This program requires a valid OpenAI API key, it will not work by itself.**

After starting the chatbot, select a character from the dropdown menu. This will set the scenario.
You can then start chatting by typing in the textbox and pressing "Submit" or the Enter key. 
Use the provided character (Aileen Moonveil) to test, or create your own!

## Adding Custom Characters
In the **./characters** folder:

1. Create a new .json file using the same structure provided in the example **Ailee.json** file. Name it using the convention **CharacterFirstName.json**, without any spaces in the file.
2. Create a square (512x512 recommended size) .png file for the character's avatar, using the same naming convention **CharacterFirstName.png**, without any spaces in the file.
3. The new characters will be available on the top right dropdown.

## Contributing
Contributions are welcome. Please create an issue to discuss the proposed changes or create a pull request.
For a fully-featured roleplaying interface designed to run locally, check [SillyTavern](https://github.com/SillyTavern/SillyTavern). This is much smaller in scope, designed for online integration and easy maintenance.

## License
GNU Affero General Public License v3.0
