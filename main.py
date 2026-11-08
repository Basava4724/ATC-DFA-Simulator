
import os
import tkinter as tk
import customtkinter as ctk
import graphviz
import io
import math

# =========================================================
# GRAPHVIZ AUTOMATIC PATH SETUP (Windows)
# =========================================================
# Allows diagrams to render when running `python main.py`
# without manually setting PATH in CMD every time.

GRAPHVIZ_PATHS = [
    r"C:\Program Files\Graphviz\bin",
    r"C:\Program Files (x86)\Graphviz\bin",
]

for graphviz_path in GRAPHVIZ_PATHS:
    if os.path.isdir(graphviz_path):
        current_path = os.environ.get("PATH", "")
        if graphviz_path not in current_path.split(os.pathsep):
            os.environ["PATH"] = graphviz_path + os.pathsep + current_path
        break

from PIL import Image, ImageTk
from dfa_logic import DFA_LIST


# =========================================================
# THEME - SCIENTIFIC VISUALIZER
# =========================================================

ctk.set_appearance_mode("light")

BG = "#F1F5F9"
WHITE = "#FFFFFF"
SIDEBAR = "#F8FAFC"

BORDER = "#E2E8F0"
TEXT = "#1E293B"
SUBTEXT = "#64748B"

BLUE = "#3B82F6"
BLUE_LIGHT = "#DBEAFE"
BLUE_HOVER = "#2563EB"

GREEN = "#16A34A"
GREEN_LIGHT = "#DCFCE7"

RED = "#DC2626"
RED_LIGHT = "#FEE2E2"

ORANGE = "#D97706"


# =========================================================
# MAIN APPLICATION
# =========================================================

class DFASimulatorApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("DFA Simulator | Scientific Visualizer")
        self.geometry("1450x900")
        self.minsize(1150, 750)

        self.configure(fg_color=BG)

        self.selected_dfa = list(DFA_LIST.values())[0]
        self.current_state = self.selected_dfa.start_state

        self.diagram_photo = None
        self.last_path = [self.current_state]

        self.create_header()
        self.create_workspace()

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color=WHITE,
            corner_radius=0,
            height=75,
            border_width=1,
            border_color=BORDER
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(side="left", padx=25)

        ctk.CTkLabel(
            left,
            text="DFA",
            font=("Segoe UI", 25, "bold"),
            text_color=BLUE
        ).pack(side="left")

        ctk.CTkLabel(
            left,
            text="  Simulator & Visualizer",
            font=("Segoe UI", 23, "bold"),
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="AUTOMATA THEORY & COMPUTATION",
            font=("Segoe UI", 12, "bold"),
            text_color=SUBTEXT
        ).pack(side="right", padx=25)

    # =====================================================
    # WORKSPACE
    # =====================================================

    def create_workspace(self):

        workspace = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        workspace.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=4)
        workspace.grid_columnconfigure(2, weight=2)

        workspace.grid_rowconfigure(0, weight=5)
        workspace.grid_rowconfigure(1, weight=2)

        # LEFT SIDEBAR
        self.sidebar = self.create_card(
            workspace,
            "Automaton Configuration",
            0,
            0
        )

        # CENTER DIAGRAM
        self.diagram_card = self.create_card(
            workspace,
            "State Diagram",
            0,
            1
        )

        # RIGHT PANEL
        self.right_panel = self.create_card(
            workspace,
            "Transition Table",
            0,
            2
        )

        # BOTTOM TRACE
        self.trace_card = self.create_card(
            workspace,
            "Execution Trace",
            1,
            0,
            columnspan=3
        )

        self.create_sidebar()
        self.create_diagram()
        self.create_transition_table()
        self.create_simulation_controls()
        self.create_trace()

    # =====================================================
    # CARD
    # =====================================================

    def create_card(
        self,
        parent,
        title,
        row,
        column,
        columnspan=1
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            border_width=1,
            border_color=BORDER,
            corner_radius=12
        )

        card.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="nsew",
            padx=6,
            pady=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=15,
            pady=12
        )

        ctk.CTkFrame(
            card,
            height=1,
            fg_color=BORDER
        ).pack(fill="x")

        return card

    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        card = self.sidebar

        ctk.CTkLabel(
            card,
            text="Select DFA",
            font=("Segoe UI", 13, "bold"),
            text_color=SUBTEXT
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.dfa_selector = ctk.CTkOptionMenu(
            card,
            values=list(DFA_LIST.keys()),
            height=38,
            fg_color=BLUE,
            button_color=BLUE,
            button_hover_color=BLUE_HOVER,
            dropdown_fg_color=WHITE,
            dropdown_text_color=TEXT,
            command=self.change_dfa
        )

        self.dfa_selector.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # Language
        ctk.CTkLabel(
            card,
            text="Language",
            font=("Segoe UI", 13, "bold"),
            text_color=SUBTEXT
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.description_label = ctk.CTkLabel(
            card,
            text="",
            font=("Segoe UI", 13),
            text_color=TEXT,
            wraplength=210,
            justify="left"
        )

        self.description_label.pack(
            anchor="w",
            padx=15,
            pady=5
        )

        # DFA details
        ctk.CTkLabel(
            card,
            text="DFA Properties",
            font=("Segoe UI", 13, "bold"),
            text_color=SUBTEXT
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.details_label = ctk.CTkLabel(
            card,
            text="",
            font=("Consolas", 12),
            text_color=TEXT,
            justify="left",
            wraplength=210
        )

        self.details_label.pack(
            anchor="w",
            padx=15,
            pady=5
        )

        self.update_configuration()

    def update_configuration(self):

        dfa = self.selected_dfa

        self.description_label.configure(
            text=dfa.description
        )

        self.details_label.configure(
            text=(
                f"States:\n{sorted(dfa.states)}\n\n"
                f"Alphabet:\n{sorted(dfa.alphabet)}\n\n"
                f"Start State:\n{dfa.start_state}\n\n"
                f"Final States:\n{sorted(dfa.final_states)}"
            )
        )

    # =====================================================
    # CHANGE DFA
    # =====================================================

    def change_dfa(self, selected_name):

        self.selected_dfa = DFA_LIST[selected_name]

        self.current_state = self.selected_dfa.start_state

        self.last_path = [self.current_state]

        self.update_configuration()
        self.update_transition_table()
        self.draw_diagram()
        self.clear_result()

    # =====================================================
    # DIAGRAM
    # =====================================================

    def create_diagram(self):

        self.canvas = tk.Canvas(
            self.diagram_card,
            bg=WHITE,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.draw_diagram()
        )

    def draw_diagram(self):

        canvas = self.canvas

        canvas.delete("all")

        dfa = self.selected_dfa

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width < 150 or height < 150:
            return

        try:

            graph = graphviz.Digraph(
                name="DFA",
                format="png",
                engine="dot"
            )

            graph.attr(
                rankdir="LR",
                bgcolor=WHITE,
                splines="true",
                nodesep="0.8",
                ranksep="1.0",
                pad="0.4",
                dpi="130"
            )

            # State appearance
            graph.attr(
                "node",
                shape="circle",
                style="filled",
                fillcolor="#F8FAFC",
                color="#94A3B8",
                fontcolor=TEXT,
                fontname="Segoe UI",
                fontsize="14",
                width="0.8",
                height="0.8",
                fixedsize="true",
                penwidth="2"
            )

            # Transition appearance
            graph.attr(
                "edge",
                color="#64748B",
                fontcolor=TEXT,
                fontname="Segoe UI",
                fontsize="12",
                penwidth="1.5",
                arrowsize="0.8"
            )

            state_ids = {
                state: f"state_{index}"
                for index, state in enumerate(
                    sorted(dfa.states)
                )
            }

            # Start point
            graph.node(
                "start_node",
                label="",
                shape="point",
                width="0.12",
                color=BLUE
            )

            graph.edge(
                "start_node",
                state_ids[dfa.start_state],
                color=BLUE
            )

            # Create states
            for state in sorted(dfa.states):

                is_final = state in dfa.final_states
                is_active = state == self.current_state

                shape = (
                    "doublecircle"
                    if is_final
                    else "circle"
                )

                fill_color = (
                    BLUE_LIGHT
                    if is_active
                    else GREEN_LIGHT
                    if is_final
                    else "#F8FAFC"
                )

                border_color = (
                    BLUE
                    if is_active
                    else GREEN
                    if is_final
                    else "#94A3B8"
                )

                graph.node(
                    state_ids[state],
                    label=state,
                    shape=shape,
                    fillcolor=fill_color,
                    color=border_color,
                    fontcolor=TEXT,
                    penwidth="2.5"
                )

            # Group transitions
            grouped = {}

            for (source, symbol), destination in (
                dfa.transitions.items()
            ):

                key = (source, destination)

                if key not in grouped:
                    grouped[key] = []

                grouped[key].append(symbol)

            # Draw transitions
            for (source, destination), symbols in grouped.items():

                label = ", ".join(sorted(symbols))

                graph.edge(
                    state_ids[source],
                    state_ids[destination],
                    label=label
                )

            # Render image
            image_data = graph.pipe(format="png")

            image = Image.open(
                io.BytesIO(image_data)
            )

            image.thumbnail(
                (width - 30, height - 30),
                Image.Resampling.LANCZOS
            )

            self.diagram_photo = ImageTk.PhotoImage(
                image
            )

            canvas.create_image(
                width // 2,
                height // 2,
                image=self.diagram_photo,
                anchor="center"
            )

        except Exception as error:

            canvas.create_text(
                width // 2,
                height // 2,
                text=f"Diagram Error:\n{error}",
                fill=RED,
                font=("Segoe UI", 12)
            )

    # =====================================================
    # TRANSITION TABLE
    # =====================================================

    def create_transition_table(self):

        self.table_frame = ctk.CTkScrollableFrame(
            self.right_panel,
            fg_color="transparent"
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.update_transition_table()

    def update_transition_table(self):

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        dfa = self.selected_dfa

        alphabet = sorted(dfa.alphabet)

        headers = ["State"] + alphabet

        for col, heading in enumerate(headers):

            ctk.CTkLabel(
                self.table_frame,
                text=heading,
                fg_color="#E2E8F0",
                text_color=TEXT,
                font=("Segoe UI", 12, "bold"),
                corner_radius=5,
                height=35
            ).grid(
                row=0,
                column=col,
                sticky="ew",
                padx=2,
                pady=2
            )

        for row, state in enumerate(
            sorted(dfa.states),
            start=1
        ):

            state_color = (
                GREEN_LIGHT
                if state in dfa.final_states
                else BLUE_LIGHT
                if state == dfa.start_state
                else "#F1F5F9"
            )

            ctk.CTkLabel(
                self.table_frame,
                text=state,
                fg_color=state_color,
                text_color=TEXT,
                corner_radius=5,
                height=35
            ).grid(
                row=row,
                column=0,
                sticky="ew",
                padx=2,
                pady=2
            )

            for col, symbol in enumerate(
                alphabet,
                start=1
            ):

                destination = dfa.transitions.get(
                    (state, symbol),
                    "-"
                )

                ctk.CTkLabel(
                    self.table_frame,
                    text=destination,
                    fg_color="#F1F5F9",
                    text_color=TEXT,
                    corner_radius=5,
                    height=35
                ).grid(
                    row=row,
                    column=col,
                    sticky="ew",
                    padx=2,
                    pady=2
                )

    # =====================================================
    # SIMULATION CONTROLS
    # =====================================================

    def create_simulation_controls(self):

        card = self.right_panel

        ctk.CTkLabel(
            card,
            text="Test Input String",
            font=("Segoe UI", 13, "bold"),
            text_color=SUBTEXT
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        self.input_entry = ctk.CTkEntry(
            card,
            height=38,
            placeholder_text="Enter string...",
            font=("Consolas", 16),
            fg_color="#F8FAFC",
            text_color=TEXT,
            border_color=BORDER
        )

        self.input_entry.pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            card,
            text="▶  Run Simulation",
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            height=38,
            font=("Segoe UI", 13, "bold"),
            command=self.simulate
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkButton(
            card,
            text="Clear",
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color=TEXT,
            height=35,
            command=self.clear_result
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

    # =====================================================
    # EXECUTION TRACE
    # =====================================================

    def create_trace(self):

        card = self.trace_card

        self.result_label = ctk.CTkLabel(
            card,
            text="Waiting for simulation...",
            font=("Segoe UI", 17, "bold"),
            text_color=SUBTEXT
        )

        self.result_label.pack(
            anchor="w",
            padx=15,
            pady=10
        )

        self.path_frame = ctk.CTkScrollableFrame(
            card,
            orientation="horizontal",
            height=75,
            fg_color="#F8FAFC"
        )

        self.path_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 12)
        )

    # =====================================================
    # SIMULATE
    # =====================================================

    def simulate(self):

        input_string = self.input_entry.get().strip()

        dfa = self.selected_dfa

        accepted, path, message = dfa.simulate(
            input_string
        )

        self.current_state = path[-1]

        self.last_path = path

        self.draw_diagram()

        if message == "Invalid input symbol":

            self.result_label.configure(
                text="⚠ INVALID INPUT SYMBOL",
                text_color=ORANGE
            )

        elif accepted:

            self.result_label.configure(
                text="✓ STRING ACCEPTED",
                text_color=GREEN
            )

        else:

            self.result_label.configure(
                text="✕ STRING REJECTED",
                text_color=RED
            )

        self.show_path(path)

    # =====================================================
    # PATH DISPLAY
    # =====================================================

    def show_path(self, path):

        for widget in self.path_frame.winfo_children():
            widget.destroy()

        dfa = self.selected_dfa

        for index, state in enumerate(path):

            is_final = (
                index == len(path) - 1
                and state in dfa.final_states
            )

            color = (
                GREEN
                if is_final
                else BLUE
                if index == 0
                else "#64748B"
            )

            ctk.CTkLabel(
                self.path_frame,
                text=state,
                fg_color=color,
                text_color="white",
                corner_radius=7,
                width=60,
                height=35,
                font=("Consolas", 14, "bold")
            ).pack(
                side="left",
                padx=4,
                pady=8
            )

            if index < len(path) - 1:

                ctk.CTkLabel(
                    self.path_frame,
                    text="→",
                    text_color=SUBTEXT,
                    font=("Segoe UI", 18)
                ).pack(side="left")

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_result(self):

        self.input_entry.delete(0, "end")

        self.current_state = self.selected_dfa.start_state

        self.last_path = [self.current_state]

        self.result_label.configure(
            text="Waiting for simulation...",
            text_color=SUBTEXT
        )

        for widget in self.path_frame.winfo_children():
            widget.destroy()

        self.draw_diagram()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app = DFASimulatorApp()
    app.mainloop()
