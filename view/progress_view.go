package view

import (
	"nutri-flow/ui/progressscreen" // UI component for progress screen
	"nutri-flow/viewmodel"         // Import the ViewModel package

	"fyne.io/fyne/v2" // Import Fyne
	"fyne.io/fyne/v2/container"
)

// NewProgressView coordinates between the ViewModel and the UI components
func NewProgressView(vm *viewmodel.ProgressViewModel) fyne.CanvasObject {
	progressUI := progressscreen.NewProgressScreenUI(vm)
	return container.NewVBox(progressUI)
}
