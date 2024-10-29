from rich.console import Console
from rich.progress import track
from enum import Enum
import time
import pyfiglet

console = Console()
total_track_desc_len = 25

class OutputType(Enum):
    WARNING = "yellow"
    ERROR = "red"
    INFO = "green"
    DEBUG = "blue"
    
def title(text: str, verbose: bool = True):
    if verbose:
        text = pyfiglet.figlet_format(text, font="slant")
        console.print(f"[cyan]{text}[/]") 

def output(text: str, output_type: OutputType = OutputType.INFO, verbose: bool = True):
    if verbose:
        title = output_type.name
        console.print(f"[{output_type.value}]{title}[/][white]:{' ' * (9 - len(title))}[{time.strftime('%d-%m-%y')} {time.strftime('%H:%M:%S')}] {text}[/]")
 
def inp(text: str):
    console.print(f"[red]{text}[/]", end="")
    return input("")
 
def track_desc_gen(text: str):
    return f"{text}{' ' * (total_track_desc_len - len(text))}"

def progress_bar(tracked, description: str):
    for i in track(tracked, description=description):
        time.sleep(0.1)

if __name__ == "__main__":
    progress_bar(range(100), "Progress bar test")
    output("This is a test warning", OutputType.WARNING)
    output("This is a test error", OutputType.ERROR)
    output("This is a test info", OutputType.INFO)
    output("This is a test debug", OutputType.DEBUG)