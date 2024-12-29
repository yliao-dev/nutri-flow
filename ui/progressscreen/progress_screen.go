package progressscreen

import (
	"fmt"
	"nutri-flow/model"
	"nutri-flow/viewmodel"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func NewProgressScreenUI(vm *viewmodel.ProgressViewModel) fyne.CanvasObject {
	mainContainer := container.NewVBox(
		widget.NewLabel("Today's Progress"),
		createProgressCircles(vm),
		widget.NewButton("Add Progress", func() {
			progressData := model.Progress{
				Calories:     100,
				Protein:      40,
				Carbohydrate: 80,
			}
			// Call the AddProgress method to update the progress
			vm.AddProgress(progressData)
		}),
	)
	return mainContainer
}

func createProgressCircles(vm *viewmodel.ProgressViewModel) fyne.CanvasObject {
	// Get values from binding
	caloriesValue, _ := vm.CaloriesPercent.Get()
	proteinValue, _ := vm.ProteinPercent.Get()
	carbonhydrateValue, _ := vm.CarbonhydratePercent.Get()

	// Ensure progress bars are bound to the correct percentage values
	caloriesProgress := widget.NewProgressBarWithData(vm.CaloriesPercent)
	proteinProgress := widget.NewProgressBarWithData(vm.ProteinPercent)
	carbsProgress := widget.NewProgressBarWithData(vm.CarbonhydratePercent)

	// Create labels for the percentages
	caloriesLabel := widget.NewLabel("Calories: " + fmt.Sprintf("%.2f", caloriesValue))
	proteinLabel := widget.NewLabel("Protein: " + fmt.Sprintf("%.2f", proteinValue))
	carbsLabel := widget.NewLabel("Carbs: " + fmt.Sprintf("%.2f", carbonhydrateValue))

	// Layout them vertically with their progress bars
	return container.NewVBox(
		caloriesLabel,
		caloriesProgress,
		proteinLabel,
		proteinProgress,
		carbsLabel,
		carbsProgress,
	)
}
