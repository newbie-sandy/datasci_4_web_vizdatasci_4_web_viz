ggplot,dplyr and shiny are not installed by default. That's a tiny bit inconvinient
## New stuff in R
df <- reactive({})
## Troubleshooting 
The URL is copy-pasted. It should be correct. The git repo is public. 
![image](https://github.com/newbie-sandy/datasci_4_web_vizdatasci_4_web_viz/assets/143536852/6c23508f-052f-4a65-a7da-b659d70a72cb)

## Problems met
 - install shiny in R: install.packages("shiny")
 - The app.r worked in first shot. GOOD! But the dropdown is empty. EWWWW
 - Close the HTML before running again

## CODE:
library(shiny)
library(ggplot2)
library(dplyr)

 ### UI for the Shiny app
ui <- fluidPage(
  titlePanel("Obesity Over 18 Years Old Age-adjusted Prevalence in NY, TX or CA state"),
  sidebarLayout(
    sidebarPanel(
      selectInput("state", "Choose a state:", choices = NULL)
    ),
    mainPanel(
      plotOutput("barPlot")
    )
  )
)

### Server logic
server <- function(input, output, session) {
  
 ### Load the dataset
  df <- reactive({
    url <- "https://github.com/newbie-sandy/datasci_4_web_vizdatasci_4_web_viz.git/subset.csv"
    read.csv(url)
  })
  
  
  ### Update state choices dynamically based on dataset
  observe({
    obesity_data <- df()
    updateSelectInput(session, "state", choices = sort(unique(obesity_data$StateAbbr)))
  })
  
  ### Render the bar plot
  output$barPlot <- renderPlot({
    obesity_data <- df()
    state_data <- df[obesity_data$StateAbbr == input$state, ]
    avg_value <- mean(obesity_data$Data_Value, na.rm = TRUE)
    
    ggplot() +
      geom_bar(data = state_data, aes(x = StateAbbr, y = Data_Value, fill = StateAbbr), stat = "identity") +
      geom_hline(aes(yintercept = avg_value), linetype = "dashed", color = "dodgerblue") +
      labs(title = 'Obesity over 18 years old Age-adjusted Prevalence',
           y = 'Data Value (Age-adjusted prevalence) - Percent',
           x = 'State') +
      theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
      ylim(0, 30) +
      scale_fill_manual(values = c("lightcoral", "dodgerblue"))
  })
  
}

### Run the Shiny app
shinyApp(ui, server)


