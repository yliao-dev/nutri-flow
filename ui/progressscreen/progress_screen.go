package progressscreen

import (
	"nutri-flow/model"
	"nutri-flow/viewmodel"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/data/binding"
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
	// Progress bars bound to data
	caloriesProgress := widget.NewProgressBarWithData(vm.CaloriesPercent)
	proteinProgress := widget.NewProgressBarWithData(vm.ProteinPercent)
	carbsProgress := widget.NewProgressBarWithData(vm.CarbonhydratePercent)

	// Labels bound to data
	caloriesLabel := widget.NewLabelWithData(binding.FloatToStringWithFormat(vm.CaloriesPercent, "%.2f"))
	proteinLabel := widget.NewLabelWithData(binding.FloatToStringWithFormat(vm.ProteinPercent, "%.2f"))
	carbsLabel := widget.NewLabelWithData(binding.FloatToStringWithFormat(vm.CarbonhydratePercent, "%.2f"))

	// Layout them vertically
	return container.NewVBox(
		widget.NewLabel("Calories:"),
		caloriesLabel,
		caloriesProgress,
		widget.NewLabel("Protein:"),
		proteinLabel,
		proteinProgress,
		widget.NewLabel("Carbs:"),
		carbsLabel,
		carbsProgress,
	)
}
