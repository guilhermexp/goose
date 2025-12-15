#!/usr/bin/env python3
"""
PPPoker Transfer Script - Usando Hybrid Kernel (GPT-4o Vision)

Uso:
    python pppoker_transfer.py --agent-id 13180661 --amount 100
    python pppoker_transfer.py --batch transfers.json
"""

import os
import sys
import time
import subprocess
import json
import base64
import argparse
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# --- CONFIGURATION ---
ADB_PATH = "adb"
MODEL_VISION = "gpt-4o"
DEFAULT_CLUB = "C.P.C. OnLine 2"
MAX_STEPS = 30
WAIT_AFTER_ACTION = 3

# Diretório de logs
SCRIPT_DIR = Path(__file__).parent.absolute()
LOG_DIR = SCRIPT_DIR / "logs"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- LOGGING ---

def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    return LOG_DIR / f"transfers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(message: str, log_file: Path = None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    if log_file:
        with open(log_file, "a") as f:
            f.write(formatted + "\n")

# --- ADB UTILITIES ---

def run_adb(args: List[str], timeout: int = 10) -> str:
    try:
        result = subprocess.run(
            [ADB_PATH] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"  [ADB Error] {e}")
        return ""

def tap(x: int, y: int):
    print(f"  👆 Tap ({x}, {y})")
    run_adb(["shell", "input", "tap", str(x), str(y)])

def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300):
    print(f"  👆 Swipe ({x1},{y1}) -> ({x2},{y2})")
    run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

def type_text(text: str):
    escaped = text.replace(" ", "%s").replace("'", "\\'")
    print(f"  ⌨️ Type: {text}")
    run_adb(["shell", "input", "text", escaped])

def press_key(key: str):
    keycode = {
        "back": "4", "home": "3", "enter": "66",
        "delete": "67", "tab": "61"
    }.get(key.lower(), key)
    print(f"  🔘 Key: {key}")
    run_adb(["shell", "input", "keyevent", keycode])

def start_app(package: str):
    print(f"  📱 Starting: {package}")
    run_adb(["shell", "am", "start", "-n", f"{package}/com.lein.pppoker.ppsdk.app.UnityMainActivity"])

def wait(seconds: int = 3):
    print(f"  ⏳ Waiting {seconds}s...")
    time.sleep(seconds)

def get_screenshot_base64() -> str:
    result = subprocess.run(
        [ADB_PATH, "exec-out", "screencap", "-p"],
        capture_output=True,
        timeout=10
    )
    if result.returncode == 0 and result.stdout:
        return base64.b64encode(result.stdout).decode('utf-8')
    return ""

# --- LLM DECISION ---

def get_transfer_prompt(agent_id: str, amount: int, club_name: str, step_context: str = "") -> str:
    return f"""You are an Android automation agent for PPPoker chip transfers.

CURRENT TASK: Transfer {amount} chips to agent ID {agent_id} in club "{club_name}"

STEP-BY-STEP PROCEDURE:
1. If on home screen with clubs, click on club "{club_name}"
2. Once inside the club, click the "Counter" icon (chip/coin icon) at bottom navigation
3. In Counter modal, click "Search Member" or search field
4. Type agent ID "{agent_id}" in search field
5. Click on the search result showing agent {agent_id}
6. Click "Send" button
7. In Send modal, clear any existing amount and type "{amount}"
8. Click "Confirm" to complete transfer
9. Wait for "Success!" message

{step_context}

SCREEN RESOLUTION: 1080x2400 pixels

Output ONLY a valid JSON object:
- {{"action": "tap", "x": 540, "y": 1200, "reason": "Clicking on..."}}
- {{"action": "type", "text": "123", "reason": "Entering..."}}
- {{"action": "swipe", "x1": 540, "y1": 1800, "x2": 540, "y2": 600, "reason": "Scrolling..."}}
- {{"action": "back", "reason": "Going back"}}
- {{"action": "wait", "seconds": 5, "reason": "Waiting for load"}}
- {{"action": "done", "success": true, "reason": "Transfer completed successfully"}}
- {{"action": "done", "success": false, "reason": "Failed because..."}}

IMPORTANT:
- PPPoker package: com.lein.pppoker.android
- After tapping, ALWAYS wait for UI to update
- Look for "Success" or green confirmation
- Be precise with coordinates based on what you see
"""

def get_llm_decision(goal_prompt: str, screenshot_b64: str) -> Dict[str, Any]:
    messages = [
        {"role": "system", "content": goal_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this screenshot and decide the next action:"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}}
            ]
        }
    ]

    response = client.chat.completions.create(
        model=MODEL_VISION,
        messages=messages,
        response_format={"type": "json_object"},
        max_tokens=500
    )

    return json.loads(response.choices[0].message.content)

# --- ACTION EXECUTION ---

def execute_action(action: Dict[str, Any]) -> tuple[bool, bool]:
    """
    Execute action. Returns (continue_loop, success).
    """
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
    elif act_type == "wait":
        wait(action.get("seconds", 3))
    elif act_type == "start_app":
        start_app(action.get("package", "com.lein.pppoker.android"))
        wait(10)
    elif act_type == "done":
        success = action.get("success", True)
        if success:
            print("\n✅ Transfer completed successfully!")
        else:
            print(f"\n❌ Transfer failed: {reason}")
        return False, success
    else:
        print(f"  ❓ Unknown action: {act_type}")

    return True, None

# --- TRANSFER FUNCTION ---

def transfer_chips(agent_id: str, amount: int, club_name: str = None, log_file: Path = None) -> Dict[str, Any]:
    """
    Execute chip transfer to an agent.

    Returns:
        dict: {success: bool, message: str, details: dict}
    """
    if club_name is None:
        club_name = DEFAULT_CLUB

    log(f"Starting transfer: {amount} chips to agent {agent_id}", log_file)
    log(f"Club: {club_name}", log_file)

    # Ensure PPPoker is open
    log("Opening PPPoker...", log_file)
    start_app("com.lein.pppoker.android")
    wait(12)  # Wait for app to fully load

    step_context = ""
    last_actions = []

    for step in range(1, MAX_STEPS + 1):
        print(f"\n[Step {step}/{MAX_STEPS}]")

        # 1. Screenshot
        print("  📸 Capturing screen...")
        screenshot = get_screenshot_base64()

        if not screenshot:
            print("  ❌ Screenshot failed")
            wait(2)
            continue

        # 2. Build context
        if last_actions:
            step_context = f"PREVIOUS ACTIONS:\n" + "\n".join(last_actions[-3:])

        # 3. Get decision
        print("  🧠 Analyzing...")
        try:
            prompt = get_transfer_prompt(agent_id, amount, club_name, step_context)
            decision = get_llm_decision(prompt, screenshot)
        except Exception as e:
            print(f"  ❌ LLM Error: {e}")
            wait(2)
            continue

        # Track action
        action_desc = f"Step {step}: {decision.get('action')} - {decision.get('reason', '')[:50]}"
        last_actions.append(action_desc)

        # 4. Execute
        continue_loop, success = execute_action(decision)

        if not continue_loop:
            if success:
                return {
                    "success": True,
                    "message": f"Transfer of {amount} chips to {agent_id} completed",
                    "details": {
                        "agent_id": agent_id,
                        "amount": amount,
                        "club": club_name,
                        "steps": step,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            else:
                return {
                    "success": False,
                    "message": decision.get("reason", "Transfer failed"),
                    "details": {
                        "agent_id": agent_id,
                        "amount": amount,
                        "club": club_name,
                        "steps": step
                    }
                }

        wait(WAIT_AFTER_ACTION)

    return {
        "success": False,
        "message": f"Max steps ({MAX_STEPS}) reached without completion",
        "details": {
            "agent_id": agent_id,
            "amount": amount,
            "club": club_name
        }
    }

# --- BATCH TRANSFER ---

def batch_transfer(transfers_file: str, log_file: Path = None) -> List[Dict]:
    with open(transfers_file, "r") as f:
        transfers = json.load(f)

    results = []
    total = len(transfers)

    log(f"Starting batch of {total} transfers", log_file)

    for i, t in enumerate(transfers, 1):
        log(f"\n[{i}/{total}] Processing transfer...", log_file)

        result = transfer_chips(
            agent_id=t["agent_id"],
            amount=t["amount"],
            club_name=t.get("club_name"),
            log_file=log_file
        )
        results.append(result)

        status = "✅" if result["success"] else "❌"
        log(f"[{i}/{total}] {status}: {t['agent_id']} - {t['amount']} chips", log_file)

        # Wait between transfers
        if i < total:
            log("Waiting before next transfer...", log_file)
            wait(5)

    # Summary
    success_count = sum(1 for r in results if r["success"])
    log(f"\n{'='*50}", log_file)
    log(f"SUMMARY: {success_count}/{total} transfers successful", log_file)
    log(f"{'='*50}", log_file)

    return results

# --- MAIN ---

def main():
    parser = argparse.ArgumentParser(description="PPPoker Transfer - Hybrid Kernel (GPT-4o Vision)")

    parser.add_argument("--agent-id", "-a", help="Agent ID (8 digits)")
    parser.add_argument("--amount", "-m", type=int, help="Chip amount to transfer")
    parser.add_argument("--club", "-c", default=DEFAULT_CLUB, help=f"Club name (default: {DEFAULT_CLUB})")
    parser.add_argument("--batch", "-b", help="JSON file with transfer list")
    parser.add_argument("--test", action="store_true", help="Test mode - just open app and describe screen")

    args = parser.parse_args()

    # Check API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    # Setup logging
    log_file = setup_logging()

    # Test mode
    if args.test:
        log("Test mode - opening PPPoker and analyzing screen", log_file)
        start_app("com.lein.pppoker.android")
        wait(12)

        screenshot = get_screenshot_base64()
        if screenshot:
            response = client.chat.completions.create(
                model=MODEL_VISION,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this PPPoker screen. Identify buttons and their approximate positions (1080x2400 resolution)."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot}"}}
                    ]
                }],
                max_tokens=500
            )
            print(f"\n{response.choices[0].message.content}")
        sys.exit(0)

    # Batch transfer
    if args.batch:
        if not os.path.exists(args.batch):
            print(f"ERROR: File {args.batch} not found")
            sys.exit(1)

        results = batch_transfer(args.batch, log_file)

        # Save results
        results_file = LOG_DIR / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to: {results_file}")

        sys.exit(0)

    # Single transfer
    if not args.agent_id or not args.amount:
        parser.print_help()
        print("\nERROR: --agent-id and --amount are required for single transfer")
        sys.exit(1)

    result = transfer_chips(
        agent_id=args.agent_id,
        amount=args.amount,
        club_name=args.club,
        log_file=log_file
    )

    if result["success"]:
        print(f"\n✅ {result['message']}")
        sys.exit(0)
    else:
        print(f"\n❌ FAILED: {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
