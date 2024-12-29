package viewmodel

import (
	"nutri-flow/model"

	"fyne.io/fyne/v2/data/binding"

	"nutri-flow/pkg"
)

// ViewModel for Today's Progress tab

type ProgressViewModel struct {
	Progress             *model.Progress
	CaloriesPercent      binding.Float
	ProteinPercent       binding.Float
	CarbonhydratePercent binding.Float
}

func NewProgressViewModel() *ProgressViewModel {
	progress := &model.Progress{
		GoalCalories:     2000,
		GoalProtein:      200,
		GoalCarbohydrate: 350,
	}
	vm := &ProgressViewModel{
		Progress:             progress,
		CaloriesPercent:      binding.NewFloat(),
		ProteinPercent:       binding.NewFloat(),
		CarbonhydratePercent: binding.NewFloat(),
	}

	// Set initial percentages to 0
	vm.CaloriesPercent.Set(0)
	vm.ProteinPercent.Set(0)
	vm.CarbonhydratePercent.Set(0)

	return vm
}

func (vm *ProgressViewModel) AddProgress(progress model.Progress) {
	vm.Progress.Add(progress)
	vm.CaloriesPercent.Set(pkg.CalculatePercentage(vm.Progress.Calories, vm.Progress.GoalCalories))
	vm.ProteinPercent.Set(pkg.CalculatePercentage(vm.Progress.Protein, vm.Progress.GoalProtein))
	vm.CarbonhydratePercent.Set(pkg.CalculatePercentage(vm.Progress.Carbohydrate, vm.Progress.GoalCarbohydrate))
}
