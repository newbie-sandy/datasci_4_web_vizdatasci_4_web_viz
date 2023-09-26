from shiny import App, render,ui
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
def load_data():
    url = "https://raw.githubusercontent.com/newbie-sandy/datasci_4_web_vizdatasci_4_web_viz/subset.csv"
    return pd.read_csv(url)

df = load_data()
# Available counties for selection
states = df['StateAbbr'].unique()

app_ui = ui.page_fluid(
    ui.input_select("State", "Select State",{state: state for state in states}),
    ui.output_text_verbatim("avg_data_value"),
    ui.output_plot("bar_chart")
)

def server(input, output, session):

    @output
    @render.text
    def avg_data_value():
        selected_state = input.state()
        avg_value = df[df['StateAbbr'] == selected_state]['Data_Value'].mean()
        return f"Average Obesity Age-adjusted Prevalence for {selected_state}: {avg_value:.2f}%"

    @output
    @render.plot(alt="Binge Drinking Age-adjusted Prevalence Bar Chart")
    def bar_chart():
        overall_avg = df['Data_Value'].mean()
        selected_state_avg = df[df['StateAbbr'] == input.county()]['Data_Value'].mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(['Selected State', 'Overall Average'], [selected_state_avg, overall_avg], color=['lightcoral', 'dodgerblue'])
        
        ax.set_ylabel('Data Value (Age-adjusted prevalence) - Percent')
        ax.set_ylim(0, 30)
        ax.set_title('Obesity Age-adjusted Prevalence Comparison')
        
        return fig


app = App(app_ui, server)