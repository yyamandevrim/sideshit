from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, SelectionList
from textual.containers import Container
from ideas import get_ideas

class IdeaSelector(App):
    CSS_PATH = None  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ideas = get_ideas()
        self.selected = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Pick your favorite shitty side projects:", id="title")
        yield SelectionList(*[
            (f"{idea['title']} - {idea['desc']}", i)
            for i, idea in enumerate(self.ideas)
        ], id="ideas")
        yield Button("Confirm Selection", id="confirm")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            selection_widget = self.query_one(SelectionList)
            selected_indices = [i for _, i in selection_widget.selected]
            self.selected = [self.ideas[i] for i in selected_indices]
            self.exit()

if __name__ == "__main__":
    app = IdeaSelector()
    app.run()
    
    if app.selected:
        print("\nYou selected:")
        for idea in app.selected:
            print(f"- {idea['title']}")
