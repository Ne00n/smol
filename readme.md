<p align="center">
  <img src="https://smolenv.com/smol-sand-a.webp" width="350" height="146" alt="smol agents in a sandbox">
</p>

# smol

smol is an agent.

smol is smol.

smol is so smol you can understand it in an afternoon.

smol is fewer tokens.

smol is fewer dependencies.

smol is easy to adapt.

```go
package main
import("bufio";"bytes";"crypto/rand";"encoding/json";"fmt";"net/http";"os";"os/exec")
type M=map[string]any
func main(){
 u:=os.Args[1];k:=rand.Text();h:=[]any{};s:=bufio.NewScanner(os.Stdin)
 for fmt.Print("> ");s.Scan();fmt.Print("> "){
  if len(bytes.TrimSpace(s.Bytes()))==0{continue}
  h=append(h,M{"role":"user","content":s.Text()})
  for{
   b,_:=json.Marshal(M{"model":"gpt-5.6-sol","input":h,"prompt_cache_key":k,"tools":[]M{{"type":"custom","name":"sh"}}})
   r,_:=http.Post(u,"application/json",bytes.NewReader(b));var x M
   json.NewDecoder(r.Body).Decode(&x);r.Body.Close();o:=x["output"].([]any);h=append(h,o...);c:=false
   for _,v:=range o{m:=v.(M);if m["type"]=="custom_tool_call"{
    c=true;p:=exec.Command("/bin/sh","-c",m["input"].(string));q,_:=p.CombinedOutput();n:=p.ProcessState.ExitCode()
    h=append(h,M{"type":"custom_tool_call_output","call_id":m["call_id"],"output":fmt.Sprintf("exit %d\n%s",n,q)})
   }}
   if !c{t:=o[len(o)-1].(M)["content"].([]any)[0].(M)["text"]
    z:=x["usage"].(M)["total_tokens"].(float64)*100/1_050_000;fmt.Printf("%s\n[%06.3f%%]\n",t,z);break}
  }
 }
}
```

## Run

Pass URL of an endpoint that is compatible with the OpenAI Responses API

```sh
go run smol.go http://127.0.0.1:8787/v1/responses
```

- Enter prompts at `>`
- History persists
- Shell calls run locally
- Ctrl-D exits

Optional quality of life: rlwrap for line editing and persistent history

```sh
rlwrap -H ~/.smol_history go run smol.go http://127.0.0.1:8787/v1/responses
```

`smol` does not add credentials to requests.

Run `smol` in an appropriate environment that has access to an API endpoint `smol` can reach

e.g. you can run a small proxy that handles your API key or ChatGPT/Codex session and forwards the requests

## FAQ

Paste the `smol` implementation into your favorite agent and ask away.

> this is `smol`, a minimal agent implementation.

Here are some prompts to get you going.

> What does smol do from a high level point of view?

> What makes this interesting?

> What is the advantage of a minimal agent like `smol` that has no 3rd party dependencies?
> How does this compare to Pi, OpenCode, Codex, Hermes, Claude Code?

> Why is it a bit counter-intuitive but actually a good idea that `smol` by default has no system prompt and only one tool?
> Why is the context window precious?
> Compare the system prompts and other context injections of Pi, OpenCode, Codex, Hermes, Claude Code to what `smol` does.

> Why does it make sense to outsource access rights, credentials, available tools and so on to the env instead of handling it in the agent process?

> Compare `smol` with Pi, OpenCode, Codex, Hermes, Claude Code and highlight key pros and cons.
> Audit the code of all of them and tell me how confident you are that you found all potential issues of `smol` vs the other agent implementations?

> I would like to run `smol` in its own environment (e.g. an ubuntu 26.04 docker image) in a way that `smol` does not need access to the OpenAI credentials
> Can you help me create a minimal standard-library-only proxy that handles my OpenAI API or a ChatGPT/Codex session key and is outside of the agent environemt?
> Walk me through this step by step so I can understand the why and how and trade-offs.

> Set up a virtual environment to benchmark `smol` using GPT 5.6 Sol medium compared to other harnesses like Pi, OpenCode, Codex, Hermes, Claude Code.
> Use an ubuntu 26.04 server image, give the vm test environment access to an endpoint that proxies to an OpenAI Responses compatible endpoint.
> Use the proxy to log traces of requests and responses so we can later analyze tokens usage, token caching, number of requests, number of tool calls
> as well as system prompts, context that was injected and helps us better understand what happened.
> I'm also interested in wall clock time and a hand-ful of agentic tasks so I can compare the harnesses in a fair way.
> Let's discuss what kind of tasks we want to bench and how we can grade them.
> Let's discuss how many runs each harness should do per task so we are confident about the results.
> Let's do this step by step so we don't waste a lot of tokens for harness bench runs before we are confident the setup works and is fair for each harness.
> Come up with an easy to use review ui that has summary tables across various dimensions but also ability to drill down and view every trace
> and easily compare traces of runs side by side. We can do all of this without any npm packages. HTML and Vanilla JS is good. Python and Go are good. Stdlib is good.

> Explain `smol.go` line by line and highlight all potential problems you can identify.
> How can we make it more robust while keeping it simple?

> Give me a few feature ideas that we could add to smol.go while staying with the existing philosophy of minimalism and stdlib-only.

Requires Go 1.24+.
