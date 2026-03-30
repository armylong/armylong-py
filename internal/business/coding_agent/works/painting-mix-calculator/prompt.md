You need to build a Flask web application that calculates custom paint color formulations. The paint shop has been using a broken color mixing system, and you need to implement the core calculation engine.

The system receives color specifications and needs to calculate the exact pigment ratios to achieve the desired color. The application should have REST API endpoints for color calculations and a simple web interface.

**Technical Requirements:**
1. Create a Flask application with proper route handling
2. Implement color mixing algorithms that calculate pigment percentages
3. Support RGB input and output precise pigment formulations
4. Handle at least 4 base pigments: Red, Blue, Yellow, White
5. Provide both JSON API endpoints and a basic HTML interface

**Expected Functionality:**
- POST /api/calculate - Accept RGB values and return pigment ratios as JSON
- GET / - Serve a basic HTML form for color input with title "Paint Color Calculator"
- Color calculations should be mathematically sound
- Handle edge cases like pure colors and grayscale

**API Response Schema:**
The POST /api/calculate endpoint must return JSON with this exact structure:
```json
{
  "red": <number>,
  "blue": <number>,
  "yellow": <number>,
  "white": <number>
}
```

**Implementation Files:**
- Create your main application at `/app/app.py`
- Include any additional modules as needed
- Ensure the Flask app runs on host 0.0.0.0 port 5000

The paint shop needs accurate formulations - incorrect ratios waste expensive pigments and frustrate customers.