from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
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
        # Aggiornamento selettivo del profilo
        for key in profile.keys():
            if key in data:
                profile[key] = data[key]
            else:
                # Mantiene il valore di default se non fornito
                profile[key] = profile.get(key, None if key == "role" else "" if "name" in key else [])
        print(profile)

        prompt = f"Devi cercare di individuare il livello di innovazione di aziende di medie-piccole imprese SME rispettivamente in 5 diverse macro sotto categorie di innovazione: 1. Business Model Innovation 2. Product/Service Innovation 3. Process/Operations Innovation 4. Customer Experience Innovation 5. Technology Adoption Innovation Ti chiedo di generarmi 5 domande, 1 per categoria per la seguente azienda: {profile['companyName']} che opera nel settore {profile['industries']} con le seguenti info del profilo: Nome: {profile['name']} Ruolo: {profile['role']} Interessi: {profile['interests']} Attitudini all'innovazione: {profile['innovationAttitudes']} Genera 5 domande pertinenti, una per ogni categoria di innovazione, considerando le informazioni fornite sul profilo dell'azienda e del CEO." 
        prompt_formato = 'La risposta deve essere in questo formato: { "queries_inno_profile": [ { "question": "Domanda 1", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 2", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 3", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 4", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] }, { "question": "Domanda 5", "answers": ["Risposta 1", "Risposta 2", "Risposta 3", "Risposta 4"] } ] }'
        prompt = prompt + prompt_formato
        print(prompt)

        # Call GPT API with the prepared prompt
        response = await call_gpt(prompt)

        # Converti la risposta in JSON
        try:
            response_json = json.loads(response)
        except json.JSONDecodeError:
            return JSONResponse(
                {"error": "Formato risposta GPT non valido"},
                status_code=500
            )

        return response_json
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



        # Execute GPT calls asynchronously
        tasks = [call_gpt(prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks)

        return {"responses": vector}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





{
  business: [
    {
      question: "Domanda 1",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    },
    {
      question: "Domanda 2",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 3",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 4",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }

  ],
  product: [
    {
      question: "Domanda 1",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    },
    {
      question: "Domanda 2",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 3",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 4",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }

  ],
  process: [
    {
      question: "Domanda 1",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    },
    {
      question: "Domanda 2",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 3",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 4",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }

  ],
  customer: [
    {
      question: "Domanda 1",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    },
    {
      question: "Domanda 2",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 3",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 4",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }

  ],
  sustainability: [
    {
      question: "Domanda 1",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    },
    {
      question: "Domanda 2",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 3",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }
    ,
    {
      question: "Domanda 4",
      answers: ["Risposta 1", "Risposta 2" , "Risposta 3", "Risposta 4"]
    }

  ]
}