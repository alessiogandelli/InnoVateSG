import asyncio 
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from langchain_openai import OpenAI
import json
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access the API key
api_key  = os.getenv("OPENAI_API_KEY ")

aclient = AsyncOpenAI(api_key=api_key)  # Pass API key explicitly

# Initialize FastAPI
app = FastAPI()

# Initialize OpenAI clients with API key
llm = OpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=api_key   # Use the loaded API key
)

# Ottimizza questa struttura dati

profile = {
    "name": "",
    "role": None,
    "interests": [],
    "innovationLevel": None,
    "onboardingComplete": False,
    "companyName": "",
    "industries": [],
    "innovationAttitudes": []
}

async def call_gpt(prompt: str):
    response = await aclient.chat.completions.create(  # Nota .chat.completions
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# POST endpoint for onboarding
@app.post("/onboarding")
async def onboarding(request: Request):
    try:
        # Parse JSON from the request body
        data = await request.json()

        # Update the profile dictionary with the provided data
        profile = {
            "name": data.get("name", ""),
            "role": data.get("role", None),
            "interests": data.get("interests", []),
            "innovationLevel": data.get("innovationLevel", None),
            "onboardingComplete": data.get("onboardingComplete", False),
            "companyName": data.get("companyName", ""),
            "industries": data.get("industries", []),
            "innovationAttitudes": data.get("innovationAttitudes", [])
        }

        # Prepare the GPT prompt using the profile information
        '''
        prompt = """Devi cercare di individuare il livello di innovazione di aziende di medie-piccole imprese SME rispettivamente in 5 diverse macro sotto categorie di innovazione:

1. Business Model Innovation
2. Product/Service Innovation
3. Process/Operations Innovation
4. Customer Experience Innovation
5. Technology Adoption Innovation

Ti chiedo di generarmi 5 domande, 1 per categoria per la seguente azienda: {companyName} che opera nel settore {industries} con le seguenti info del profilo:

Nome: {name}
Ruolo: {role}
Interessi: {interests}
Attitudini all'innovazione: {innovationAttitudes}

Genera 5 domande pertinenti, una per ogni categoria di innovazione, considerando le informazioni fornite sul profilo dell'azienda e del CEO.
La risposta deve essere in questo formato:

{
  "queries_inno_profile": [
    {
      "question": "Domanda 1",
      "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
    },
    {
      "question": "Domanda 2",
      "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
    },
    {
      "question": "Domanda 3",
      "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
    },
    {
      "question": "Domanda 4",
      "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
    },
    {
      "question": "Domanda 5",
      "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
    }
  ]
}"""

        prompt = prompt.format(
            companyName=profile['companyName'],
            industries=', '.join(profile['industries']),
            name=profile['name'],
            role=profile['role'],
            interests=', '.join(profile['interests']),
            innovationAttitudes=', '.join(profile['innovationAttitudes'])
        )
        print(prompt)'
        
        prompt = 'Devi cercare di individuare il livello di innovazione di aziende di medie-piccole imprese SME rispettivamente in 5 diverse macro sotto categorie di innovazione: 1. Business Model Innovation 2. Product/Service Innovation 3. Process/Operations Innovation 4. Customer Experience Innovation 5. Technology Adoption Innovation Ti chiedo di generarmi 5 domande, 1 per categoria per la seguente azienda: {companyName} che opera nel settore', profile[], 'con le seguenti info del profilo: Nome: {name} Ruolo: {role} Interessi: {interests} Attitudini all innovazione: {innovationAttitudes} Genera 5 domande pertinenti, una per ogni categoria di innovazione, considerando le informazioni fornite sul profilo dell azienda e del CEO. La risposta deve essere in questo formato: { "queries_inno_profile": [ { "question": "Domanda 1", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 2", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 3", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 4", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 5", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] } ] }'
        prompt = prompt.format(
            companyName=profile['companyName'],
            industries=', '.join(profile['industries']),
            name=profile['name'],
            role=profile['role'],
            interests=', '.join(profile['interests']),
            innovationAttitudes=', '.join(profile['innovationAttitudes'])
        )'
        '''
        json_data = {
        "queries_inno_profile": [
            {
            "question": "Domanda 1",
            "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
            },
            {
            "question": "Domanda 2",
            "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
            },
            {
            "question": "Domanda 3",
            "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
            },
            {
            "question": "Domanda 4",
            "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
            },
            {
            "question": "Domanda 5",
            "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"]
            }
        ]
        }

        # Se vuoi convertire la variabile in una stringa JSON:
        json_string = json.dumps(json_data, ensure_ascii=False, indent=2)

        # Call GPT API with the prepared prompt
        #response = await call_gpt(prompt)

        return {"responses": json_string}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/plan_businessModel")
async def plan_businessModel(request: Request):  # Use Request type for the parameter
    try:
        # Load JSON from request body
        data = await request.json()  # Use .json() to parse 

        print(data)

        # Extract formatted text for each category
        vector = [
            "\n".join([f"{item['question']} {item['answer']}" for item in data.get(category, [])])
            for category in data
        ]

        print(vector)
        print(vector[0])

        """
        # Prepare 5 distinct GPT prompts
        prompts = [
            f"Analyze the following business model practices:\n{vector[0]}",
            f"Evaluate our product innovation approach:\n{vector[1]}",
            f"Review our process innovation strategies:\n{vector[2]}",
            f"Assess our customer experience management:\n{vector[3]}",
            f"Provide insights on our technology adoption (if any data is available):\n{vector[4]}"
        ]"
        """

        # Execute GPT calls asynchronously
        #tasks = [call_gpt(prompt) for prompt in prompts]
        #responses = await asyncio.gather(*tasks)

        return {"responses": vector}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

