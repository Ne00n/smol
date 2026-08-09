import json,sys,os;from subprocess import getoutput;from urllib.request import Request,urlopen;from uuid import uuid4
url=sys.argv[1];task=" ".join(sys.argv[2:]);h=[];H={"Content-Type":"application/json","session_id":uuid4().hex}
PLAN_MODEL="Qwen3.5-27B-UD-Q6_K_XL:THINKING";EXEC_MODEL="Qwen3.6-35B-A3B-UD-Q6_K_XL:THINKING"
b=dict(model=EXEC_MODEL,input=h,tools=[dict(type="function",name="sh",description="Run a shell command and return its output.",parameters=dict(type="object",properties=dict(command=dict(type="string")),required=["command"]))])
def step(p,model=EXEC_MODEL):
  global h
  b["model"]=model;h+=[dict(role="user",content=p)]
  while True:
    r=json.load(urlopen(Request(url,json.dumps(b).encode(),H)));o=r["output"];h+=o;c=[i for i in o if i["type"]=="function_call"]
    if not c:t=o[-1]["content"][0]["text"];print(t,f'\n[{r["usage"]["total_tokens"]/10500:05.2f}%]');return t
    h+=[dict(type="function_call_output",call_id=i["call_id"],output=getoutput(json.loads(i["arguments"])["command"])) for i in c]
if not os.path.exists("plan.md"):
  step(f"Task: {task}\nWrite a clear step by step plan to accomplish this task and save it to plan.md using the sh tool. Then reply with just OK.",PLAN_MODEL)
else:
  step(f"Resume this task. Here is the existing plan.md:\n{open('plan.md').read()}\n\nHere is changes.md so far:\n{open('changes.md').read() if os.path.exists('changes.md') else '(empty)'}\n\nContinue from where you left off.")
while "DONE" not in step("Continue working through plan.md one step at a time. After making changes this turn, append a short summary of what you changed to changes.md using the sh tool. If the entire plan is now complete, reply with exactly DONE instead."):pass