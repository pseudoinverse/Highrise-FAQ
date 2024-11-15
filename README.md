# Highrise FAQ Chatbot

## Prerequisites
The code has been tested in the following environment:

- MacOS 15.1
- Python 3.11

Run the following command to install required packages:

```bash
pip3 install -r requirements.txt
```

Set [OpenAI API key](https://openai.com/index/openai-api/) in environment variable `OPENAI_API_KEY`. 

```bash
export OPENAI_API_KEY=<API_KEY>
```

## Usage

### Chatbot

To run the chatbot locally, run the following command:

```bash
cd src
python3 main.py
```

The chatbot will be accessible at `http://localhost:8000`, where you can interact with the chatbot interface. 
Note that the first user message may take longer to process as the chatbot loads the spaCy NLP model.

Additionally, you can find logs by indexing `http://localhost:8000/chat_message/{index}`.

### Scrape the latest FAQ data

FAQ data is scraped from the [Highrise FAQ page](https://support.highrise.game/en/) and stored in `data/faq.json`.
To scrape the latest FAQ data, run the following command:

```bash
cd src
python3 scrape.py
```

### Logging

Logs are automatically stored in `data/logs.txt` when the chatbot is running, 
with each user message and chatbot response stored in a new line.

## Reference
Chatbot interface is built using FastHTML template from [fasthtml-example](https://github.com/AnswerDotAI/fasthtml-example/tree/main/02_chatbot)
