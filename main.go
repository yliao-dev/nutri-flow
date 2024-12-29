package main

import (
	"nutri-flow/ui/datascreen"       // Import the DataScreen package
	"nutri-flow/ui/ingredientscreen" // Import the IngredientScreen package
	"nutri-flow/ui/progressscreen"   // Import the ProgressScreen package
	"nutri-flow/viewmodel"           // Import the ViewModel package

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Create a new Fyne application
	myApp := app.New()
	myWindow := myApp.NewWindow("NutriFlow")

	// Initialize ViewModels
	progressViewModel := viewmodel.NewProgressViewModel()
	// ingredientViewModel := viewmodel.NewIngredientViewModel()
	// dataViewModel := viewmodel.NewDataViewModel()

	// Create individual screens
	progressScreen := progressscreen.NewProgressScreen(progressViewModel)
	ingredientScreen := ingredientscreen.NewIngredientScreen()
	dataScreen := datascreen.NewDataScreen()

	// Create tabs for navigation
	tabs := container.NewAppTabs(
		container.NewTabItem("Progress", progressScreen),
		container.NewTabItem("Ingredients", ingredientScreen),
		container.NewTabItem("Data", dataScreen),
	)

	// Set the content of the main window to the tabs
	myWindow.SetContent(container.NewVBox(
		tabs,
		widget.NewButton("Quit", func() {
			myApp.Quit()
		}),
	))

	// Show the main window
	myWindow.ShowAndRun()
}
