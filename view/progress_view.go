package view

import (
	"nutri-flow/model"
	"nutri-flow/viewmodel"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

// UI for Today's Progress

func CreateProgressUI(vm *viewmodel.ProgessViewModel) fyne.CanvasObject {
	caloriesLabel := widget.NewLabelWithData(vm.CaloriesPercent)
    proteinLabel := widget.NewLabelWithData(vm.ProteinPercent)
    carbsLabel := widget.NewLabelWithData(vm.CarbonhydratePercent)
	progressData := model.Progress {
		Calories:       100,
    	Protein:        40,
    	Carbohydrate:   80,
	}
	addButton := widget.NewButton("Add Ingredient", func() {
        vm.AddProgress(progressData) // Example values to add
    })

	return container.NewVBox(
 		widget.NewLabel("Today's Progress"),
        widget.NewLabel("Calories:"),
        caloriesLabel,
        widget.NewLabel("Protein:"),
        proteinLabel,
        widget.NewLabel("Carbs:"),
        carbsLabel,
        addButton,

	)
}