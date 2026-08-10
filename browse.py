#!/usr/bin/env python3
import json
import sys
import base64
from playwright.sync_api import sync_playwright

STATE_FILE = "/tmp/browser_state.json"

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"url": "about:blank"}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_visible_elements(page):
    """Return a numbered list of interactive elements the LLM can act on."""
    elements = page.query_selector_all(
        "a, button, input, textarea, select, [role='button'], [onclick]"
    )
    visible = []
    for i, el in enumerate(elements[:50]):  # cap at 50 to save context
        try:
            if not el.is_visible():
                continue
            tag = el.evaluate("el => el.tagName.toLowerCase()")
            text = (el.inner_text() or el.get_attribute("value") or "").strip()[:80]
            placeholder = el.get_attribute("placeholder") or ""
            href = el.get_attribute("href") or ""
            elem_id = el.get_attribute("id") or ""
            elem_type = el.get_attribute("type") or ""
            
            desc = f"[{i}] <{tag}"
            if elem_id: desc += f" id='{elem_id}'"
            if elem_type: desc += f" type='{elem_type}'"
            desc += f"> {text}"
            if placeholder: desc += f" (placeholder: {placeholder})"
            if href: desc += f" -> {href}"
            desc += "</" + tag + ">"
            
            visible.append({
                "index": i,
                "description": desc,
                "selector": f"nth-match({tag}, {i+1})"  # simple fallback
            })
        except:
            continue
    return visible

def get_page_content(page):
    """Extract main text content, not raw HTML."""
    # Remove script/style/nav/footer before extracting text
    page.evaluate("""
        () => {
            const toRemove = document.querySelectorAll('script, style, nav, footer, aside, .advertisement');
            toRemove.forEach(el => el.remove());
        }
    """)
    # Get main content if available, else body text
    main = page.query_selector("main, article, [role='main'], #content, .content")
    if main:
        text = main.inner_text()
    else:
        text = page.inner_text("body")
    # Truncate aggressively
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return "\n".join(lines[:100])  # ~100 lines max

def take_screenshot(page, path="/tmp/browser_screenshot.png"):
    page.screenshot(path=path, full_page=False)
    return path

def run_command(cmd):
    state = load_state()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        # Restore last URL if we're not navigating
        if cmd.get("action") != "navigate" and state.get("url"):
            try:
                page.goto(state["url"], wait_until="domcontentloaded", timeout=10000)
            except:
                pass
        
        action = cmd.get("action")
        
        if action == "navigate":
            url = cmd["url"]
            if not url.startswith("http"):
                url = "https://" + url
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            state["url"] = page.url
            
        elif action == "click":
            # Click by text or index
            idx = cmd.get("index")
            if idx is not None:
                elements = page.query_selector_all("a, button, input, [role='button']")
                count = 0
                for el in elements:
                    if el.is_visible():
                        if count == idx:
                            el.click()
                            page.wait_for_load_state("networkidle", timeout=5000)
                            break
                        count += 1
            else:
                page.get_by_text(cmd["text"]).first.click()
            state["url"] = page.url
            
        elif action == "type":
            idx = cmd.get("index")
            text = cmd["text"]
            if idx is not None:
                elements = page.query_selector_all("input, textarea")
                count = 0
                for el in elements:
                    if el.is_visible():
                        if count == idx:
                            el.fill(text)
                            break
                        count += 1
            else:
                page.get_by_placeholder(cmd.get("placeholder") or "").fill(text)
                
        elif action == "screenshot":
            path = take_screenshot(page)
            state["screenshot"] = path
            
        elif action == "scroll":
            direction = cmd.get("direction", "down")
            amount = cmd.get("amount", 800)
            if direction == "down":
                page.evaluate(f"window.scrollBy(0, {amount})")
            else:
                page.evaluate(f"window.scrollBy(0, -{amount})")
        
        # Build observation
        observation = {
            "url": page.url,
            "title": page.title(),
            "elements": get_visible_elements(page),
            "content": get_page_content(page)[:4000],  # hard cap
        }
        
        if cmd.get("action") == "screenshot":
            with open(state["screenshot"], "rb") as f:
                observation["screenshot_b64"] = base64.b64encode(f.read()).decode()
        
        save_state(state)
        browser.close()
        return observation

if __name__ == "__main__":
    cmd = json.loads(sys.argv[1])
    result = run_command(cmd)
    print(json.dumps(result, indent=2))