package datascreen

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func NewDataScreen() fyne.CanvasObject {
	// Create the main screen container (VBox)
	mainContainer := container.NewVBox()

	// Add data labels or graphs (for demonstration purposes, using a placeholder)
	mainContainer.Add(widget.NewLabel("History Data and Report Here"))

	return mainContainer
}
