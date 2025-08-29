from nicegui import ui
from app.counter_service import get_or_create_counter, increment_counter, reset_counter


def create():
    """Create counter application UI."""

    @ui.page("/counter")
    def counter_page():
        # Get or create the default counter
        counter = get_or_create_counter()

        # Set up modern styling
        ui.add_head_html("""
        <style>
        .counter-display {
            font-size: 4rem;
            font-weight: bold;
            color: #2563eb;
            text-align: center;
            margin: 2rem 0;
        }
        .counter-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        </style>
        """)

        # Main container with modern styling
        with ui.column().classes(
            "items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8"
        ):
            # Title
            ui.label("Simple Counter").classes("text-3xl font-bold text-gray-800 mb-8")

            # Counter display card
            with ui.card().classes("counter-card p-8 rounded-2xl shadow-2xl"):
                count_label = ui.label(str(counter.count)).classes("counter-display")

                # Button container
                with ui.row().classes("gap-4 mt-6 justify-center"):

                    def handle_increment():
                        """Handle increment button click."""
                        updated_counter = increment_counter()
                        count_label.set_text(str(updated_counter.count))
                        ui.notify(f"Count increased to {updated_counter.count}", type="positive")

                    def handle_reset():
                        """Handle reset button click."""
                        reset_counter_result = reset_counter()
                        if reset_counter_result:
                            count_label.set_text("0")
                            ui.notify("Counter reset to 0", type="info")

                    # Increment button with gradient styling
                    ui.button("Increment", on_click=handle_increment).classes(
                        "px-8 py-3 text-lg font-semibold text-white rounded-lg shadow-lg hover:shadow-xl transition-all"
                    ).style("background: linear-gradient(45deg, #3b82f6 0%, #1d4ed8 100%);")

                    # Reset button
                    ui.button("Reset", on_click=handle_reset).classes(
                        "px-6 py-3 text-lg font-semibold border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-all"
                    ).props("outline")

            # Info section
            with ui.column().classes("mt-8 text-center text-gray-600"):
                ui.label('Click "Increment" to increase the counter').classes("text-sm")
                ui.label('Click "Reset" to set counter back to 0').classes("text-sm")

    @ui.page("/")
    def index():
        """Redirect root to counter page."""
        ui.navigate.to("/counter")
