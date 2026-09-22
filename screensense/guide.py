"""Guide Mode: The Patient "Show, Don't Do" On-Device Screen Tutor.

Empowers 40+ and senior users to master everyday desktop software:
- Microsoft Word, PowerPoint, Excel
- Windows 11 system shortcuts and settings
- Web browsers, email attachment, and video calls
- Government, tax, and health portal forms

Philosophy:
1. Never run commands autonomously (preserves human control).
2. Highlight the exact button with a glowing box (reduces visual fatigue).
3. One step at a time with plain-English instructions.
"""

from typing import Dict, Any, List, Optional
import time
from .inference_engine import default_engine


class GuideAction:
    def __init__(
        self,
        intent_keywords: List[str],
        app_context: str,
        step_title: str,
        instruction: str,
        highlight_target: str,
        bounding_box_pct: Dict[str, float],
        shortcut: Optional[str] = None,
        copy_text: Optional[str] = None
    ):
        self.intent_keywords = intent_keywords
        self.app_context = app_context
        self.step_title = step_title
        self.instruction = instruction
        self.highlight_target = highlight_target
        # Bounding box as percentages of window: {x, y, width, height}
        self.bounding_box_pct = bounding_box_pct
        self.shortcut = shortcut
        self.copy_text = copy_text


# Pre-mapped knowledge base for popular productivity apps
# Combined with Windows UI Automation (UIA) tree simulation
GUIDE_KNOWLEDGE_BASE: List[GuideAction] = [
    # --- MICROSOFT WORD ---
    GuideAction(
        intent_keywords=["page number", "add page numbers", "number my pages"],
        app_context="Microsoft Word",
        step_title="Adding Page Numbers in Word",
        instruction="Click the 'Insert' tab at the top, then click 'Page Number'. You can choose whether you want numbers at the top or bottom of your page.",
        highlight_target="Ribbon: Insert -> Page Number",
        bounding_box_pct={"x": 0.28, "y": 0.08, "width": 0.09, "height": 0.05},
        shortcut="Alt + N, N, U"
    ),
    GuideAction(
        intent_keywords=["table", "insert table", "add table", "make a grid"],
        app_context="Microsoft Word",
        step_title="Inserting a Table in Word",
        instruction="Click the 'Insert' tab, then click 'Table'. Move your mouse over the grid to select how many rows and columns you need.",
        highlight_target="Ribbon: Insert -> Table",
        bounding_box_pct={"x": 0.18, "y": 0.08, "width": 0.07, "height": 0.05},
        shortcut="Alt + N, T"
    ),
    GuideAction(
        intent_keywords=["save as pdf", "convert to pdf", "export pdf", "make pdf"],
        app_context="Microsoft Word",
        step_title="Saving Your Document as a PDF",
        instruction="Click 'File' in the top-left corner, select 'Save As', and in the file type dropdown choose 'PDF (*.pdf)'.",
        highlight_target="Menu: File -> Save As -> PDF",
        bounding_box_pct={"x": 0.02, "y": 0.04, "width": 0.08, "height": 0.04},
        shortcut="F12 (opens Save As dialog)"
    ),
    GuideAction(
        intent_keywords=["bold", "make text bold", "darken text"],
        app_context="Microsoft Word",
        step_title="Making Text Bold",
        instruction="Select the text with your mouse, then click the 'B' button on the Home toolbar.",
        highlight_target="Toolbar: Home -> Bold (B)",
        bounding_box_pct={"x": 0.14, "y": 0.08, "width": 0.03, "height": 0.04},
        shortcut="Ctrl + B"
    ),

    # --- MICROSOFT POWERPOINT ---
    GuideAction(
        intent_keywords=["add picture", "insert photo", "put image", "insert picture"],
        app_context="Microsoft PowerPoint",
        step_title="Adding a Picture to Your Slide",
        instruction="Click the 'Insert' tab, click 'Pictures', and choose 'This Device' to select a photo saved on your computer.",
        highlight_target="Ribbon: Insert -> Pictures",
        bounding_box_pct={"x": 0.22, "y": 0.08, "width": 0.08, "height": 0.05},
        shortcut="Alt + N, P, D"
    ),
    GuideAction(
        intent_keywords=["new slide", "add slide", "another slide"],
        app_context="Microsoft PowerPoint",
        step_title="Adding a New Slide",
        instruction="Click the 'New Slide' button on the Home tab, or press Ctrl+M on your keyboard.",
        highlight_target="Ribbon: Home -> New Slide",
        bounding_box_pct={"x": 0.10, "y": 0.08, "width": 0.08, "height": 0.05},
        shortcut="Ctrl + M"
    ),
    GuideAction(
        intent_keywords=["present", "slideshow", "start presentation", "full screen"],
        app_context="Microsoft PowerPoint",
        step_title="Starting Full-Screen Presentation",
        instruction="Press the F5 key on your keyboard to start the presentation from the beginning, or click the small projector icon in the top toolbar.",
        highlight_target="Toolbar: Slide Show -> From Beginning",
        bounding_box_pct={"x": 0.35, "y": 0.08, "width": 0.10, "height": 0.05},
        shortcut="F5 (From Start) or Shift + F5 (From Current Slide)"
    ),

    # --- MICROSOFT EXCEL ---
    GuideAction(
        intent_keywords=["add up a column", "add up column", "add column", "sum", "total", "sum numbers"],
        app_context="Microsoft Excel",
        step_title="Calculating the Sum of a Column",
        instruction="Click the empty cell below your numbers, type '=SUM(' then drag your mouse over the numbers, and press Enter.",
        highlight_target="Formula Bar / AutoSum Button",
        bounding_box_pct={"x": 0.75, "y": 0.08, "width": 0.07, "height": 0.04},
        shortcut="Alt + = (AutoSum shortcut)",
        copy_text="=SUM(A1:A10)"
    ),
    GuideAction(
        intent_keywords=["freeze row", "freeze panes", "keep top row visible"],
        app_context="Microsoft Excel",
        step_title="Freezing the Top Row Header",
        instruction="Click the 'View' tab at the top, click 'Freeze Panes', and select 'Freeze Top Row'. This keeps your headers visible when scrolling down.",
        highlight_target="Ribbon: View -> Freeze Panes -> Freeze Top Row",
        bounding_box_pct={"x": 0.58, "y": 0.08, "width": 0.09, "height": 0.05}
    ),
    GuideAction(
        intent_keywords=["ref error", "value error", "#ref!", "#value!"],
        app_context="Microsoft Excel",
        step_title="Fixing #REF! or #VALUE! Errors",
        instruction="A #REF! error happens when a column or cell was deleted that your formula was looking for. Press Ctrl+Z to undo your last deletion, or click the formula to update the cell reference.",
        highlight_target="Error Cell Indicator",
        bounding_box_pct={"x": 0.30, "y": 0.25, "width": 0.12, "height": 0.04}
    ),

    # --- WINDOWS 11 CORE ---
    GuideAction(
        intent_keywords=["screenshot", "screen capture", "snip"],
        app_context="Windows",
        step_title="Taking a Screenshot in Windows",
        instruction="Press Windows Key + Shift + S together. Your screen will dim, and you can drag your mouse across any area you want to save.",
        highlight_target="Windows Snipping Tool Bar",
        bounding_box_pct={"x": 0.40, "y": 0.02, "width": 0.20, "height": 0.06},
        shortcut="Win + Shift + S"
    ),
    GuideAction(
        intent_keywords=["downloads", "where did my file go", "find download"],
        app_context="Windows",
        step_title="Finding Downloaded Files",
        instruction="Open File Explorer (the yellow folder icon on your taskbar), then click 'Downloads' in the left-hand menu.",
        highlight_target="Taskbar: File Explorer Icon",
        bounding_box_pct={"x": 0.25, "y": 0.94, "width": 0.04, "height": 0.05},
        shortcut="Ctrl + J (in any web browser)"
    ),
    GuideAction(
        intent_keywords=["make text bigger", "scale", "zoom screen", "larger fonts"],
        app_context="Windows",
        step_title="Making Screen Text Easier to Read",
        instruction="Right-click on your empty desktop screen, click 'Display settings', and choose 125% or 150% under 'Scale'.",
        highlight_target="Settings: Display -> Scale",
        bounding_box_pct={"x": 0.50, "y": 0.35, "width": 0.25, "height": 0.08}
    ),

    # --- EMAIL & COLLABORATION ---
    GuideAction(
        intent_keywords=["attach file", "send attachment", "attach document", "paperclip"],
        app_context="Email / Gmail",
        step_title="Attaching a File to an Email",
        instruction="Click the small paperclip icon at the bottom of your message window. A window will open where you can select the file to send.",
        highlight_target="Compose Window: Paperclip Icon",
        bounding_box_pct={"x": 0.28, "y": 0.88, "width": 0.04, "height": 0.04}
    ),
    GuideAction(
        intent_keywords=["share screen", "present in teams", "show my screen"],
        app_context="Microsoft Teams",
        step_title="Sharing Your Screen in Teams",
        instruction="Click the 'Share' icon (a rectangle with an up arrow) at the top of the Teams meeting window, then click 'Window' or 'Screen 1'.",
        highlight_target="Teams Meeting Bar: Share Button",
        bounding_box_pct={"x": 0.72, "y": 0.04, "width": 0.06, "height": 0.04},
        shortcut="Ctrl + Shift + E"
    ),
    # --- DEVELOPER & VS CODE WORKFLOWS ---
    GuideAction(
        intent_keywords=["connect vs code to github", "connect vscode to github", "login to github in vs code", "sign in to github in vs code", "github in vs code", "connect github", "link github"],
        app_context="VS Code & GitHub",
        step_title="Connecting VS Code to Your GitHub Account",
        instruction="Click the 'Accounts' icon (the person silhouette) in the bottom-left corner of VS Code, and click 'Sign in with GitHub'. A browser window will open asking you to authorize.",
        highlight_target="Activity Bar: Accounts Icon (Bottom-Left) -> Sign In",
        bounding_box_pct={"x": 0.01, "y": 0.94, "width": 0.03, "height": 0.04},
        shortcut="Ctrl + Shift + P -> Type 'GitHub: Sign In'",
        copy_text=None
    ),
    GuideAction(
        intent_keywords=["git username", "git email", "set my git username", "configure git"],
        app_context="Git / Terminal",
        step_title="Setting Your Git Name and Email",
        instruction="Paste these commands into your terminal to set your identity for commits. Safe: this does not modify or delete any files.",
        highlight_target="Terminal: Command Prompt",
        bounding_box_pct={"x": 0.10, "y": 0.75, "width": 0.80, "height": 0.20},
        shortcut="Ctrl + ` (Toggles Terminal in VS Code)",
        copy_text='git config --global user.name "Your Name" && git config --global user.email "you@example.com"'
    ),
    GuideAction(
        intent_keywords=["preview markdown", "preview .md", "preview md", "markdown preview"],
        app_context="VS Code",
        step_title="Previewing Markdown (.md) in VS Code",
        instruction="With your .md file open, click the split-screen 'Open Preview to the Side' icon in the top-right corner of the editor, or press Ctrl+Shift+V.",
        highlight_target="Editor Tab Bar (Top-Right): Open Preview Icon",
        bounding_box_pct={"x": 0.94, "y": 0.08, "width": 0.04, "height": 0.04},
        shortcut="Ctrl + Shift + V (or Ctrl + K, V for side-by-side)"
    ),
    GuideAction(
        intent_keywords=["clone repo", "clone github", "download repository", "git clone"],
        app_context="VS Code & Git",
        step_title="Cloning a GitHub Repository in VS Code",
        instruction="Press Ctrl+Shift+P, type 'Git: Clone', paste your repository link (e.g., https://github.com/...), and pick a local folder to save it.",
        highlight_target="Command Palette (Top Center)",
        bounding_box_pct={"x": 0.25, "y": 0.02, "width": 0.50, "height": 0.06},
        shortcut="Ctrl + Shift + P -> 'Git: Clone'"
    ),
    GuideAction(
        intent_keywords=["git push", "push to github", "push code", "upload to github", "how to git push"],
        app_context="Git / VS Code",
        step_title="Pushing Your Code to GitHub",
        instruction="In VS Code, click the Source Control icon (the branch graph) on the left sidebar and click 'Sync Changes' (or 'Push'). Or paste this command into your terminal to upload your latest commits:",
        highlight_target="Activity Bar: Source Control (Left Sidebar) -> Push",
        bounding_box_pct={"x": 0.01, "y": 0.20, "width": 0.03, "height": 0.04},
        shortcut="Ctrl + Shift + G (Opens Source Control in VS Code)",
        copy_text="git push -u origin main"
    ),
    GuideAction(
        intent_keywords=["commit message", "what should my commit message be", "suggest commit message"],
        app_context="Git / GitHub",
        step_title="Crafting a Clear Commit Message",
        instruction="Write a clear, concise summary in the imperative mood. For example: 'Fix authentication error and add error handling'.",
        highlight_target="Source Control Tab: Commit Message Box",
        bounding_box_pct={"x": 0.04, "y": 0.15, "width": 0.18, "height": 0.08},
        copy_text='Add feature update and error handling'
    )
]


class ScreenGuide:
    """Intelligent guide matching user intent to actionable, patient steps."""

    def __init__(self, engine=None):
        self.engine = engine or default_engine

    def resolve_guide_request(self, user_query: str, current_app: str = "auto") -> Dict[str, Any]:
        """Resolves natural language questions into visual guidance with exact coordinates."""
        start_time = time.perf_counter()
        query_lower = user_query.lower()

        # Match intent against knowledge base
        best_match: Optional[GuideAction] = None
        for action in GUIDE_KNOWLEDGE_BASE:
            for kw in action.intent_keywords:
                if kw in query_lower:
                    best_match = action
                    break
            if best_match:
                break

        # Simulate NPU latency telemetry
        npu_stats = self.engine.run_fast_sentiment_ocr(user_query)

        if best_match:
            return {
                "found": True,
                "app": best_match.app_context,
                "step_title": best_match.step_title,
                "instruction": best_match.instruction,
                "highlight_target": best_match.highlight_target,
                "bounding_box_pct": best_match.bounding_box_pct,
                "shortcut": best_match.shortcut,
                "copy_text": best_match.copy_text,
                "npu_latency_ms": npu_stats["latency_ms"],
                "philosophy": "Show, Don't Do. The user retains complete control."
            }

        # Fallback guidance for unrecognized query
        return {
            "found": False,
            "app": current_app if current_app != "auto" else "Any Desktop App",
            "step_title": "Let's Find It Together",
            "instruction": f"I see you want to: '{user_query}'. Try looking at the top menu bar or press the Alt key to see shortcut letters on every button.",
            "highlight_target": "Main Menu Bar",
            "bounding_box_pct": {"x": 0.10, "y": 0.04, "width": 0.80, "height": 0.05},
            "shortcut": "Press Alt key for button shortcuts",
            "copy_text": None,
            "npu_latency_ms": npu_stats["latency_ms"],
            "philosophy": "Show, Don't Do."
        }


# Global guide instance
guide = ScreenGuide()
