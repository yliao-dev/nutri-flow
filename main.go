package main

import (
	"fmt"
	"strconv"

	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	// Create a new app
	myApp := app.New()
	myWindow := myApp.NewWindow("NutriFlow")

	// Create input fields for food details
	foodName := widget.NewEntry()
	foodProtein := widget.NewEntry()
	foodCarbs := widget.NewEntry()
	foodCalories := widget.NewEntry()

	// Input field for body weight
	bodyWeight := widget.NewEntry()

	// Display recommended nutrition
	recommendationLabel := widget.NewLabel("123")

	// Button to calculate recommended protein intake
	calculateButton := widget.NewButton("Calculate Nutrition", func() {
		weight, err := strconv.ParseFloat(bodyWeight.Text, 64)
		if err != nil {
			recommendationLabel.SetText("Please enter a valid weight.")
			return
		}
		// Calculate protein recommendation (1.6g per kg of body weight)
		proteinRecommendation := weight * 1.6
		recommendationLabel.SetText(fmt.Sprintf("Recommended Protein: %.2f grams", proteinRecommendation))
	})

	// Create button to save food item
	saveButton := widget.NewButton("Save Food", func() {
		// Print input details to the console (for now)
		println("Food Name:", foodName.Text)
		println("Protein:", foodProtein.Text)
		println("Carbs:", foodCarbs.Text)
		println("Calories:", foodCalories.Text)
	})

	// Set up the window content with input fields, buttons, and recommendation label
	myWindow.SetContent(container.NewVBox(
		widget.NewLabel("Enter Body Weight:"),
		bodyWeight,
		calculateButton,
		recommendationLabel,
		widget.NewLabel("Enter Food Details:"),
		foodName,
		foodProtein,
		foodCarbs,
		foodCalories,
		saveButton,
	))

	// Show and run the app
	myWindow.ShowAndRun()
}