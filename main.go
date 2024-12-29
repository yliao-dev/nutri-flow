package main

import (
	"fmt"
	"nutri-flow/ui/components" // Import the DataScreen package

	"nutri-flow/viewmodel"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Create a new Fyne application
	a := app.New()
	w := a.NewWindow("NutriFlow")

	// Initialize ViewModels
	progressViewModel := viewmodel.NewProgressViewModel()
	fmt.Println(progressViewModel.CaloriesPercent)
	// ingredientViewModel := viewmodel.NewIngredientViewModel()
	// dataViewModel := viewmodel.NewDataViewModel()

	tabs := components.NewTabs(progressViewModel)
	w.Resize(fyne.NewSize(800, 600))

	// Set the content of the main window to the tabs
	w.SetContent(container.NewVBox(
		tabs,
		widget.NewButton("Quit", func() {
			a.Quit()
		}),
	))

	// Show the main window
	w.ShowAndRun()
}
