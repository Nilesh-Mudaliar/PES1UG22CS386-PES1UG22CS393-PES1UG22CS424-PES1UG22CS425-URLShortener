#!/bin/bash

# Number of requests and concurrency level
REQUESTS=1000
CONCURRENCY=50

echo "Starting intensive load test with $REQUESTS requests, $CONCURRENCY concurrent..."

# URL to test
URL="http://localhost/shorten"

# Function to generate CPU-intensive work (run in background)
generate_load() {
  echo "Generating CPU load..."
  for i in {1..10}; do
    # Start background processes doing CPU-intensive calculations
    (
      end=$((SECONDS+15))  # Run for 15 seconds
      while [ $SECONDS -lt $end ]; do
        # Create random data and calculate sha256sum, very CPU intensive
        head -c 50000 /dev/urandom | sha256sum > /dev/null
      done
    ) &
  done
}

# Generate initial CPU load
generate_load

# Array of real URLs
REAL_URLS=(
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley&feature=player_embedded"
  "https://www.amazon.com/Apple-MacBook-16-inch-10%E2%80%91core-16%E2%80%91core/dp/B09JQSLL92"
  "https://www.google.com/maps/place/Taj+Mahal/@27.1751448,78.0395673,17z"
)

# Send a burst of requests to create significant load
for i in $(seq 1 $REQUESTS); do
  # Generate additional load periodically
  if [ $((i % 100)) -eq 0 ]; then
    generate_load
  fi
  
  # Randomly select one of the URLs
  RANDOM_INDEX=$((RANDOM % ${#REAL_URLS[@]}))
  SELECTED_URL="${REAL_URLS[$RANDOM_INDEX]}"
  
  # Add complexity by generating a large random parameter
  RANDOM_DATA=$(head -c 1000 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 500)
  UNIQUE_URL="${SELECTED_URL}&data=${RANDOM_DATA}&id=$i"
  
  curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"url\":\"$UNIQUE_URL\"}" \
    $URL &
  
  # Control concurrency
  if [ $((i % CONCURRENCY)) -eq 0 ]; then
    wait
    echo "Sent $i requests..."
  fi
  
  # Short delay to maintain continuous pressure
  sleep 0.01
done

wait
echo "Load test completed. Sent $REQUESTS requests."