from dotenv import load_dotenv
from crewai import Crew
from tasks import PrepTasks
from agents import PrepAgents
import os

# Standard library imports
import re
import os
import json
from typing import Union

#import fastapi modules
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import copy
from fastapi import APIRouter, Request, Response, Form

gdata =[]

router = APIRouter()

def answer_query_with_prompt_engineering(ques):
    load_dotenv()
    
    print("## Welcome to the Crypyo Crew")
    print('-------------------------------')
    
    query = ques

    
    conversation = copy.deepcopy(gdata)
    chat_history = ""

    for conv in conversation:
        if conv["role"] == "user":
            chat_history += "\nUser: "
            chat_history += str(conv["content"])
        else:
            chat_history += "\nExpert: "
            chat_history += str(conv["content"])

        # print("DEBUG: chat_history:", chat_history)

    tasks =  PrepTasks()
    agents = PrepAgents()
    
    # create agents
    prompt_agent = agents.prompt_agent()

    

    # create tasks
    prompt_task = tasks.prompt_task(prompt_agent, query, chat_history)
    

    crew = Crew(
      agents=[
        prompt_agent
      ],
      tasks=[
        prompt_task
      ]
    )
    
    result = crew.kickoff()
    
    return result
    

data = []
@router.post("/chat_response_qa")
async def chat_response(request: Request, prompt: str = Form(...)):
    ques = str(prompt)
    global gdata, data
    # print(ques)
    answer = answer_query_with_prompt_engineering(ques)
    user_json = {
        "role": "user",
        "content": ques
    }
    assistant_json = {
        "role": "assistant",
        "content": answer
    }
    data.append(user_json)
    data.append(assistant_json)
    gdata = data
    with open("data.json", "w") as json_file:
      json.dump(data, json_file, indent=2)
    print("Updated Data:")
    print(json.dumps(data, indent=2))
    response_data = jsonable_encoder(json.dumps({"answer": answer}))
    res = Response(response_data)
    return res
  


  
