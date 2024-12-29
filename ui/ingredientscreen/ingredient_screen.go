package ingredientscreen

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func NewIngredientScreen() fyne.CanvasObject {
	// Create the main screen container (VBox)
	mainContainer := container.NewVBox()

	// Add ingredients list or favorite ingredients
	mainContainer.Add(widget.NewLabel("Ingredient List and Favorites Here"))

	return mainContainer
}
