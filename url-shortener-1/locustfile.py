from locust import HttpUser, task, between
import random
import string
import time
import json

class URLShortenerUser(HttpUser):
    wait_time = between(0.05, 0.15)  # Very aggressive timing for high load
    
    def random_string(self, length=10):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(length))
    
    @task(3)
    def shorten_url(self):
        # Real-world complex URLs
        base_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley&feature=player_embedded",
            "https://www.amazon.com/Apple-MacBook-16-inch-10%E2%80%91core-16%E2%80%91core/dp/B09JQSLL92/ref=sr_1_3?crid=2SZNONBHUM8R3",
            "https://www.google.com/maps/place/Taj+Mahal/@27.1751448,78.0395673,17z/data=!3m1!4b1!4m5!3m4!1s0x39747121d702ff6d:0xdd2ae4803f767dde",
            "https://www.linkedin.com/jobs/search/?currentJobId=3580124697&keywords=software%20engineer&location=Worldwide&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON"
        ]
        
        # Create complex URL with many parameters
        base_url = random.choice(base_urls)
        params = "&".join([f"param{i}={self.random_string(20)}" for i in range(15)])
        timestamp = int(time.time() * 1000)
        unique_id = self.random_string(30)
        
        # Build a very long URL that requires significant processing
        long_url = f"{base_url}&{params}&timestamp={timestamp}&unique_id={unique_id}"
        
        # Add artificial CPU work by adding a large nested JSON payload
        payload = {
            "url": long_url,
            "metadata": {
                "user": {
                    "id": self.random_string(10),
                    "session": self.random_string(32),
                    "preferences": {k: self.random_string(5) for k in range(10)}
                },
                "device": {
                    "type": random.choice(["mobile", "desktop", "tablet"]),
                    "os": random.choice(["ios", "android", "windows", "macos"]),
                    "browser": random.choice(["chrome", "safari", "firefox", "edge"]),
                    "version": f"{random.randint(1, 20)}.{random.randint(0, 99)}.{random.randint(0, 999)}"
                },
                "tracking": {
                    "referrer": random.choice([
                        "google.com", 
                        "facebook.com", 
                        "twitter.com", 
                        "linkedin.com",
                        "instagram.com"
                    ]),
                    "campaign": self.random_string(8),
                    "parameters": {k: self.random_string(5) for k in range(5)}
                }
            }
        }
        
        # Make the request with the complex payload
        response = self.client.post(
            "/shorten", 
            json=payload,
            headers={"X-Custom-Header": self.random_string(50)}
        )
        
        # Store successful short URLs for later access
        if response.status_code == 200:
            try:
                data = response.json()
                short_url = data.get("short_url", "")
                if short_url:
                    # Extract just the code part
                    code = short_url.split("/")[-1]
                    if not hasattr(self, "short_codes"):
                        self.short_codes = []
                    self.short_codes.append(code)
                    # Limit stored codes to prevent memory issues
                    if len(self.short_codes) > 200:
                        self.short_codes = self.short_codes[-200:]
            except json.JSONDecodeError:
                pass
    
    @task(1)
    def access_shortened_url(self):
        # Use a previously created short code or generate random one
        if hasattr(self, "short_codes") and self.short_codes:
            short_code = random.choice(self.short_codes)
        else:
            short_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        
        # Access the shortened URL with custom headers to add variety
        self.client.get(
            f"/{short_code}", 
            allow_redirects=False,
            headers={
                "User-Agent": f"LocustTesting/{self.random_string(10)}",
                "Accept-Language": random.choice(["en-US", "fr-FR", "de-DE", "ja-JP", "es-ES"])
            }
        )