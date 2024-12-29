package components

import (
	"nutri-flow/ui/datascreen"       // Import the DataScreen package
	"nutri-flow/ui/ingredientscreen" // Import the IngredientScreen package
	"nutri-flow/ui/progressscreen"   // Import the ProgressScreen package
	"nutri-flow/viewmodel"           // Import the ViewModel package

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
)

// NewTabs creates and returns the tab UI
func NewTabs(progressViewModel *viewmodel.ProgressViewModel) fyne.CanvasObject {
	// Create individual screens
	progressScreen := progressscreen.NewProgressScreenUI(progressViewModel)
	ingredientScreen := ingredientscreen.NewIngredientScreen()
	dataScreen := datascreen.NewDataScreen()

	// Create tabs for navigation
	tabs := container.NewAppTabs(
		container.NewTabItem("Progress", progressScreen),
		container.NewTabItem("Ingredients", ingredientScreen),
		container.NewTabItem("Data", dataScreen),
	)

	// Return the tabs container
	return tabs
}
