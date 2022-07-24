import os
import openai
import json
from pathlib import Path
from flask import request, make_response

def gener8(request):
  openai.api_key = os.environ.get("OPENAI_API_KEY", "Specified env var not set")
  model = Path('model/data.yaml').read_text()
  req_prompt = request.data.decode("utf-8") 
  if len(req_prompt) == 0:
    return build_response("Bad request!", 400)
  #print(req_prompt)
  prompt = model + "## " + req_prompt + "\n" 
  # https://beta.openai.com/docs/api-reference/completions/create
  response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0.5,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["---"]
  )
  #print("response", response)
  jsonToPython = json.loads(str(response))
  #print("jsonToPython", jsonToPython)
  result = "# Auto-generated by Gener8 - https://github.com/PrasadG193/Gener8\n" + jsonToPython['choices'][0]['text']
  #print("result", result)
  return build_response(result, 200)

def build_response(result, status_code):
  response = make_response(result, status_code)
  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Headers", "Content-Type")
  return response
