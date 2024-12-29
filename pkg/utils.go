package pkg

import "fmt"

// CalculatePercentage takes a value and a goal and returns a formatted percentage string.
func CalculatePercentage(value, goal int) string {
    if goal == 0 { // Avoid division by zero
        return "0.00%"
    }
    return fmt.Sprintf("%.2f%%", (float64(value)/float64(goal))*100)
}