#!/bin/bash

echo "Starting load test with real URLs..."

# Number of total requests
TOTAL=1000

# Array of real-world complex URLs
REAL_URLS=(
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley&feature=player_embedded"
  "https://www.amazon.com/Apple-MacBook-16-inch-10%E2%80%91core-16%E2%80%91core/dp/B09JQSLL92/ref=sr_1_3"
  "https://www.google.com/maps/place/Taj+Mahal/@27.1751448,78.0395673,17z"
  "https://www.linkedin.com/jobs/search/?currentJobId=3580124697&keywords=software%20engineer"
)

# Run many parallel operations
for i in $(seq 1 $TOTAL); do
  # Generate a complex workload
  (
    # Select a random real URL
    RANDOM_INDEX=$((RANDOM % ${#REAL_URLS[@]}))
    SELECTED_URL="${REAL_URLS[$RANDOM_INDEX]}"
    
    # Create unique long URL
    LONG_URL="${SELECTED_URL}&unique_id=$i&timestamp=$(date +%s%N)"
    
    # Send request
    curl -s -X POST -H "Content-Type: application/json" \
      -d "{\"url\":\"$LONG_URL\"}" \
      http://localhost/shorten > /dev/null
  ) &
  
  # Status update
  if [ $((i % 50)) -eq 0 ]; then
    echo "Started $i requests ($(( i * 100 / TOTAL ))%)..."
  fi
  
  # Control concurrency
  if [ $((i % 100)) -eq 0 ]; then
    wait
  fi
done

wait
echo "Load test completed."
