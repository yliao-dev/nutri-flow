package pkg

import (
	"strconv"
	"strings"
)

// CalculatePercentage takes a value and a goal and returns a formatted percentage string.
func CalculatePercentage(value, goal int) float64 {
	if goal == 0 { // Avoid division by zero
		return 0.00
	}
	return (float64(value) / float64(goal)) * 100
}

func ParsePercentage(percent string) float64 {
	percent = strings.TrimSuffix(percent, "%")
	value, err := strconv.ParseFloat(percent, 64)
	if err != nil {
		return 0
	}
	return value
}
