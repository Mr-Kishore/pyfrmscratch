from google import genai
from google.genai import types

def generate():
    client = genai.Client(
        vertexai=True,
        project="peerless-summit-454811-d7",
        location="us-central1",
    )

    prompt = types.Part.from_text(text="""Could you please generate detailed documentation for the following Python code? I need a one-paragraph summary of the overall purpose of the code at the beginning and a thorough explanation of each function below it.

```python
import tkinter as tk
import time

def start_timer():
    global running
    if not running:
        update_timer()
        running = True

def stop_timer():
    global running
    if running:
        root.after_cancel(update_time)
        running = False

def reset_timer():
    global running, elapsed_time
    if running:
        root.after_cancel(update_time)
        running = False
    elapsed_time = 0
    timer_label.config(text="00:00:00")

def update_timer():
    global elapsed_time, update_time
    elapsed_time += 1
    timer_label.config(text=time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))
    update_time = root.after(1000, update_timer)

root = tk.Tk()
root.title("Stopwatch")

running = False
elapsed_time = 0

timer_label = tk.Label(root, text="00:00:00", font=("Arial", 30))
timer_label.pack(pady=20)

start_button = tk.Button(root, text="Start", command=start_timer, font=("Arial", 14))
start_button.pack(side="left", padx=20)

stop_button = tk.Button(root, text="Stop", command=stop_timer, font=("Arial", 14))
stop_button.pack(side="left", padx=20)

reset_button = tk.Button(root, text="Reset", command=reset_timer, font=("Arial", 14))
reset_button.pack(side="left", padx=20)

root.mainloop()
```""")

    contents = [
        types.Content(role="user", parts=[prompt])
    ]

    config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.95,
        max_output_tokens=2048,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        response_mime_type="text/plain",
        system_instruction=[types.Part.from_text(text="You are a student programmer.")],
    )

    full_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.0-flash-001",
        contents=contents,
        config=config,
    ):
        full_text += chunk.text

    # Save to local file (in current directory)
    output_file = "gemini_output.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Gemini documentation written to: {output_file}")

if __name__ == "__main__":
    generate()
