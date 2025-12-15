#!/usr/bin/env python3
"""
Hybrid Android Kernel - Combines uiautomator + screenshot vision
Works with both normal apps AND Unity apps (like PPPoker)

Usage:
    python hybrid_kernel.py "Abra o PPPoker e entre no clube C.P.C"
    python hybrid_kernel.py --interactive
"""

import os
import sys
import time
import subprocess
import json
import base64
import argparse
from typing import Dict, Any, List, Optional
from openai import OpenAI

# --- CONFIGURATION ---
ADB_PATH = "adb"
MODEL_TEXT = "gpt-4o"  # For uiautomator (text only, cheaper)
MODEL_VISION = "gpt-4o"  # For screenshot (vision, more expensive)
SCREEN_DUMP_PATH = "/sdcard/window_dump.xml"
LOCAL_DUMP_PATH = "/tmp/window_dump.xml"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- ADB UTILITIES ---

def run_adb(args: List[str], timeout: int = 10) -> str:
    """Execute ADB command and return output."""
    try:
        result = subprocess.run(
            [ADB_PATH] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0 and result.stderr:
            print(f"  [ADB Warning] {result.stderr.strip()}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  [ADB Timeout] Command timed out")
        return ""
    except Exception as e:
        print(f"  [ADB Error] {e}")
        return ""

def tap(x: int, y: int):
    """Tap at coordinates."""
    print(f"  👆 Tap ({x}, {y})")
    run_adb(["shell", "input", "tap", str(x), str(y)])

def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300):
    """Swipe gesture."""
    print(f"  👆 Swipe ({x1},{y1}) -> ({x2},{y2})")
    run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

def type_text(text: str):
    """Type text (spaces replaced with %s for ADB)."""
    escaped = text.replace(" ", "%s").replace("'", "\\'")
    print(f"  ⌨️ Type: {text}")
    run_adb(["shell", "input", "text", escaped])

def press_key(key: str):
    """Press a key (BACK, HOME, ENTER, etc)."""
    keycode = {
        "back": "4", "home": "3", "enter": "66",
        "delete": "67", "tab": "61"
    }.get(key.lower(), key)
    print(f"  🔘 Key: {key}")
    run_adb(["shell", "input", "keyevent", keycode])

def start_app(package: str):
    """Start an app by package name."""
    print(f"  📱 Starting: {package}")
    run_adb(["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"])

def wait(seconds: int = 3):
    """Wait for UI to update."""
    print(f"  ⏳ Waiting {seconds}s...")
    time.sleep(seconds)

# --- PERCEPTION ---

def get_uiautomator_dump() -> Optional[str]:
    """Get UI hierarchy via uiautomator dump. Returns None if fails or empty."""
    run_adb(["shell", "uiautomator", "dump", SCREEN_DUMP_PATH])
    run_adb(["pull", SCREEN_DUMP_PATH, LOCAL_DUMP_PATH])

    if not os.path.exists(LOCAL_DUMP_PATH):
        return None

    with open(LOCAL_DUMP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if it has useful content
    if len(content) < 500 or content.count("clickable=\"true\"") < 2:
        return None  # Probably a Unity app or empty screen

    return content

def parse_ui_elements(xml_content: str) -> List[Dict]:
    """Parse XML and extract interactive elements with coordinates."""
    import re
    elements = []

    # Find all nodes with bounds
    pattern = r'<node[^>]*text="([^"]*)"[^>]*resource-id="([^"]*)"[^>]*class="([^"]*)"[^>]*clickable="([^"]*)"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"'

    for match in re.finditer(pattern, xml_content):
        text, resource_id, class_name, clickable, x1, y1, x2, y2 = match.groups()

        # Calculate center
        cx = (int(x1) + int(x2)) // 2
        cy = (int(y1) + int(y2)) // 2

        if text or resource_id:  # Only include elements with some identifier
            elements.append({
                "text": text,
                "id": resource_id.split("/")[-1] if "/" in resource_id else resource_id,
                "class": class_name.split(".")[-1],
                "clickable": clickable == "true",
                "center": [cx, cy]
            })

    return elements

def get_screenshot_base64() -> str:
    """Capture screenshot and return as base64."""
    result = subprocess.run(
        [ADB_PATH, "exec-out", "screencap", "-p"],
        capture_output=True,
        timeout=10
    )

    if result.returncode == 0 and result.stdout:
        return base64.b64encode(result.stdout).decode('utf-8')
    return ""

def get_screen_state() -> tuple[str, bool]:
    """
    Get screen state. Returns (context_string, is_screenshot).
    Tries uiautomator first, falls back to screenshot.
    """
    # Try uiautomator first (faster, cheaper)
    xml = get_uiautomator_dump()

    if xml:
        elements = parse_ui_elements(xml)
        if elements:
            context = json.dumps(elements, indent=2, ensure_ascii=False)
            return context, False

    # Fallback to screenshot (for Unity apps)
    print("  📸 Using screenshot (Unity/game app detected)")
    b64 = get_screenshot_base64()

    if b64:
        return b64, True

    return "Error: Could not get screen state", False

# --- LLM DECISION ---

SYSTEM_PROMPT_TEXT = """
You are an Android automation agent. Your job is to achieve the user's goal by navigating the UI.

You receive a JSON list of interactive UI elements with their center coordinates.

Output ONLY a valid JSON object with your next action:
- {"action": "tap", "x": 540, "y": 1200, "reason": "Clicking button X"}
- {"action": "type", "text": "Hello", "reason": "Entering text"}
- {"action": "swipe", "x1": 540, "y1": 1500, "x2": 540, "y2": 500, "reason": "Scrolling down"}
- {"action": "back", "reason": "Going back"}
- {"action": "home", "reason": "Going to home"}
- {"action": "wait", "seconds": 3, "reason": "Waiting for load"}
- {"action": "start_app", "package": "com.example.app", "reason": "Opening app"}
- {"action": "done", "reason": "Task completed"}

Be precise with coordinates. Always explain your reasoning.
"""

SYSTEM_PROMPT_VISION = """
You are an Android automation agent with VISION. You can see screenshots of the screen.

Your job is to achieve the user's goal by looking at the screen and deciding what to tap/type.

The screen resolution is approximately 1080x2400 pixels. Estimate coordinates based on visual position.

Output ONLY a valid JSON object with your next action:
- {"action": "tap", "x": 540, "y": 1200, "reason": "Clicking the blue button in center"}
- {"action": "type", "text": "Hello", "reason": "Entering text in the field"}
- {"action": "swipe", "x1": 540, "y1": 1800, "x2": 540, "y2": 600, "reason": "Scrolling up"}
- {"action": "back", "reason": "Going back"}
- {"action": "wait", "seconds": 10, "reason": "Waiting for app to load"}
- {"action": "start_app", "package": "com.lein.pppoker.android", "reason": "Opening PPPoker"}
- {"action": "done", "reason": "Task completed"}

CRITICAL APP PACKAGE NAMES (use EXACTLY these):
- PPPoker: com.lein.pppoker.android
- Settings: com.android.settings
- Chrome: com.android.chrome

IMPORTANT for PPPoker:
- Package name is EXACTLY: com.lein.pppoker.android (NOT com.pppoker or anything else!)
- After opening, ALWAYS wait 10+ seconds for it to load completely
- This is a Unity game - it loads slowly!
- Look for "Club" button/icon to enter a club
- "Counter" is at the bottom (chip icon) for sending chips
- Club name: C.P.C. OnLine 2 (ID: 3330646)
- Test agent ID: 13180661

Be precise with coordinates based on what you SEE. Always explain your reasoning.
"""

def get_llm_decision(goal: str, context: str, is_screenshot: bool) -> Dict[str, Any]:
    """Ask LLM for next action."""

    if is_screenshot:
        # Vision model with image
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_VISION},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"GOAL: {goal}\n\nAnalyze this screenshot and decide the next action:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{context}"}}
                ]
            }
        ]
        model = MODEL_VISION
    else:
        # Text model with UI elements
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_TEXT},
            {"role": "user", "content": f"GOAL: {goal}\n\nUI ELEMENTS:\n{context}"}
        ]
        model = MODEL_TEXT

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        max_tokens=500
    )

    return json.loads(response.choices[0].message.content)

# --- ACTION EXECUTION ---

def execute_action(action: Dict[str, Any]) -> bool:
    """Execute an action. Returns False if 'done'."""
    act_type = action.get("action", "")
    reason = action.get("reason", "")

    print(f"  💡 {reason}")

    if act_type == "tap":
        tap(action.get("x", 0), action.get("y", 0))
    elif act_type == "type":
        type_text(action.get("text", ""))
    elif act_type == "swipe":
        swipe(
            action.get("x1", 540), action.get("y1", 1500),
            action.get("x2", 540), action.get("y2", 500)
        )
    elif act_type == "back":
        press_key("back")
    elif act_type == "home":
        press_key("home")
    elif act_type == "wait":
        wait(action.get("seconds", 3))
    elif act_type == "start_app":
        start_app(action.get("package", ""))
        wait(5)  # Always wait after starting app
    elif act_type == "done":
        print("\n✅ Goal achieved!")
        return False
    else:
        print(f"  ❓ Unknown action: {act_type}")

    return True

# --- MAIN AGENT LOOP ---

def run_agent(goal: str, max_steps: int = 20):
    """Run the agent loop."""
    print(f"\n🚀 Hybrid Android Kernel")
    print(f"📋 Goal: {goal}")
    print("-" * 50)

    # Force screenshot mode for Unity/game apps
    force_screenshot = any(x in goal.lower() for x in ["pppoker", "poker", "game", "unity", "casino"])
    if force_screenshot:
        print("🎮 Detected game/Unity app - forcing screenshot mode")

    for step in range(1, max_steps + 1):
        print(f"\n[Step {step}/{max_steps}]")

        # 1. Perception
        print("  👀 Scanning screen...")

        if force_screenshot:
            # Skip uiautomator for games
            b64 = get_screenshot_base64()
            context, is_screenshot = (b64, True) if b64 else ("Error: Screenshot failed", False)
        else:
            context, is_screenshot = get_screen_state()

        if "Error" in context:
            print(f"  ❌ {context}")
            wait(2)
            continue

        mode = "📸 Vision" if is_screenshot else "📝 UIAutomator"
        print(f"  {mode} mode")

        # 2. Reasoning
        print("  🧠 Thinking...")
        try:
            decision = get_llm_decision(goal, context, is_screenshot)
        except Exception as e:
            print(f"  ❌ LLM Error: {e}")
            wait(2)
            continue

        # 3. Action
        if not execute_action(decision):
            break

        # Wait for UI to update
        wait(2)

    print("\n🏁 Agent finished")

def interactive_mode():
    """Interactive mode - enter commands one at a time."""
    print("\n🎮 Interactive Mode")
    print("Commands: tap X Y | type TEXT | swipe | back | home | screenshot | goal GOAL | quit")
    print("-" * 50)

    while True:
        try:
            cmd = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if action == "quit" or action == "exit":
            break
        elif action == "tap" and args:
            coords = args.split()
            if len(coords) >= 2:
                tap(int(coords[0]), int(coords[1]))
        elif action == "type" and args:
            type_text(args)
        elif action == "swipe":
            # Default scroll down
            swipe(540, 1500, 540, 500)
        elif action == "back":
            press_key("back")
        elif action == "home":
            press_key("home")
        elif action == "screenshot":
            print("  📸 Capturing...")
            b64 = get_screenshot_base64()
            print(f"  ✅ Got {len(b64)} bytes")
        elif action == "start" and args:
            start_app(args)
        elif action == "wait":
            wait(int(args) if args else 3)
        elif action == "goal" and args:
            run_agent(args)
        elif action == "scan":
            context, is_screenshot = get_screen_state()
            if is_screenshot:
                print("  📸 Screenshot mode (Unity app)")
            else:
                print(context[:500] + "..." if len(context) > 500 else context)
        else:
            print(f"  ❓ Unknown: {cmd}")

# --- MAIN ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hybrid Android Kernel")
    parser.add_argument("goal", nargs="?", help="Goal to achieve")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--max-steps", "-n", type=int, default=20, help="Max steps")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.goal:
        run_agent(args.goal, args.max_steps)
    else:
        # Default: interactive
        interactive_mode()
