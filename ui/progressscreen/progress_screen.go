package progressscreen

import (
	"nutri-flow/viewmodel" // Import the ViewModel package

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
)

func NewProgressScreen(progressViewModel *viewmodel.ProgressViewModel) fyne.CanvasObject {
	// Create the main screen container (VBox)
	mainContainer := container.NewVBox()

	// Add Tabs (Today's Progress, Ingredients, History) from components
	return mainContainer
}
