package components

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func NewTabs() fyne.CanvasObject {
	// Create individual tab items
	tab1 := widget.NewLabel("Today's progress details here...")
	tab2 := widget.NewLabel("List of ingredients here...")
	tab3 := widget.NewLabel("History data here...")

	// Create the tabs container using container.Tabs
	tabs := container.NewAppTabs(
		container.NewTabItem("Today's Progress", tab1),
		container.NewTabItem("Ingredients", tab2),
		container.NewTabItem("History", tab3),
	)

	// Return the tabs as a container
	return tabs
}
