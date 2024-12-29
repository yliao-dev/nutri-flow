package main

import (
	"nutri-flow/view"
	"nutri-flow/viewmodel"

	"fyne.io/fyne/v2/app"
)

func main() {
	// Create a new app
	myApp := app.New()
	myWindow := myApp.NewWindow("Today's Progress")
	
	progressVM := viewmodel.NewProgressViewModel()
	progressUI := view.CreateProgressUI(progressVM)

	myWindow.SetContent(progressUI)
	myWindow.ShowAndRun()
}