package model

// Progress model (e.g., calories, protein, carbs)

type Progress struct {
	Calories int
	Protein int
	Carbohydrate int
	GoalCalories int
	GoalProtein int
	GoalCarbohydrate int
}

func (p *Progress) Add(progress Progress) {
	p.Calories += progress.Calories
	p.Protein += progress.Protein
	p.Carbohydrate += progress.Carbohydrate
}

